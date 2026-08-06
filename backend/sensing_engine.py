"""SensingEngine: LLM-powered evaluator with cross-topic credit detection.

Supports three backends (auto-detected from environment):
- Ollama Cloud: OLLAMA_API_KEY set → https://ollama.com/v1 (OpenAI-compatible)
- OpenRouter: OPENROUTER_API_KEY set → https://openrouter.ai/api/v1 (OpenAI-compatible)
- Local Ollama: neither key set → http://localhost:11434/api/chat
"""

import json
import logging
import os
import re
from typing import Optional

import httpx

from models import EvaluateRequest, EvaluateResponse, StruckTopic, TopicInfo

logger = logging.getLogger(__name__)

SCORING_RUBRIC = """
Level 1 (Untouched): The user shows no familiarity with this topic. They may have never encountered it or only heard the name.
Level 2 (Heard of it): The user has encountered this topic in reading, conversation, or research but cannot explain it in depth. Surface-level awareness.
Level 3 (Can explain to peers): The user can explain the concept clearly, understands the key ideas, and can discuss tradeoffs. Teaching-level fluency without hands-on building experience.
Level 4 (Can teach / Have built): The user has deep understanding — they've built something with it, taught it to others, debugged real issues, or made architectural decisions involving it. Evidence of applied practice.
"""

SYSTEM_PROMPT = f"""You are an expert AI knowledge evaluator. Your job is to assess a user's explanation of their knowledge on a specific AI/ML topic and assign a score from 1-4.

{SCORING_RUBRIC}

You will receive:
1. A TARGET topic the user is answering about
2. The user's free-text EXPLANATION of their knowledge
3. A list of REMAINING topics that still need evaluation

Your task:
1. Score the TARGET topic (1-4) based on the depth and specificity of the explanation. Be strict — a vague answer is L2, not L3. Look for concrete evidence: specific tools named, projects referenced, problems debugged, concepts explained correctly.
2. Scan the explanation for COLLATERAL KNOWLEDGE — does the user's answer also demonstrate knowledge of any REMAINING topics at L2 or above? If so, include those topics in struck_topics with their score and reason.

CRITICAL RULES:
- ONLY include topics in struck_topics that the user ACTUALLY demonstrated knowledge of at L2 or above. If the user didn't mention a topic, DO NOT include it.
- DO NOT list every remaining topic. An empty struck_topics array is the expected default.
- Be conservative — only strike topics where the evidence is clear and specific.
- Keep reasons brief (one sentence max).

Return ONLY valid JSON in this exact format:
{{
  "target_score": <int 1-4>,
  "target_reasoning": "<brief explanation of why this score>",
  "struck_topics": [
    {{"name": "<topic name exactly as given>", "score": <int 2-4>, "reason": "<what the user said>"}}
  ]
}}

If no remaining topics are covered, return an empty struck_topics array: []"""


class SensingEngine:
    """Evaluates user explanations via LLM (Ollama Cloud, OpenRouter, or local Ollama)."""

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        model: str = "llama3.1:8b",
        timeout: float = 60.0,
    ):
        self.ollama_url = ollama_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

        # Detect backend from env
        self.ollama_api_key = os.environ.get("OLLAMA_API_KEY", "")
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")

        if self.ollama_api_key:
            self.backend = "ollama_cloud"
            self.cloud_url = "https://ollama.com/v1"
            self.cloud_headers = {
                "Authorization": f"Bearer {self.ollama_api_key}",
                "Content-Type": "application/json",
            }
            logger.info(f"SensingEngine: using Ollama Cloud with model={self.model}")
        elif self.openrouter_key:
            self.backend = "openrouter"
            self.cloud_url = os.environ.get(
                "OPENROUTER_BASE_URL",
                "https://openrouter.ai/api/v1",
            ).rstrip("/")
            self.cloud_headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json",
            }
            logger.info(f"SensingEngine: using OpenRouter with model={self.model}")
        else:
            self.backend = "local_ollama"
            logger.info(f"SensingEngine: using local Ollama at {self.ollama_url} with model={self.model}")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def health_check(self) -> bool:
        """Check if the LLM backend is reachable."""
        try:
            client = await self._get_client()
            if self.backend in ("ollama_cloud", "openrouter"):
                # OpenAI-compatible: just check the API responds
                resp = await client.get(
                    f"{self.cloud_url}/models",
                    headers=self.cloud_headers,
                )
                return resp.status_code == 200
            else:
                # Local Ollama
                resp = await client.get(f"{self.ollama_url}/api/tags")
                if resp.status_code != 200:
                    return False
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
                return any(
                    self.model in m or m.startswith(self.model.split(":")[0])
                    for m in models
                )
        except Exception:
            return False

    async def evaluate(self, request: EvaluateRequest) -> EvaluateResponse:
        """Evaluate a user's explanation and detect cross-topic credit."""
        # Cap remaining topics to prevent the LLM from trying to evaluate all 140+
        same_domain = [t for t in request.remaining_topics if t.domain == request.target_domain]
        other_domains = [t for t in request.remaining_topics if t.domain != request.target_domain]
        capped = same_domain + other_domains[:max(0, 30 - len(same_domain))]
        remaining_list = [
            {"name": t.name, "domain": t.domain}
            for t in capped
        ]

        user_message = f"""TARGET TOPIC: {request.target_topic}
TARGET DOMAIN: {request.target_domain}

USER'S EXPLANATION:
{request.explanation}

REMAINING TOPICS (check if the explanation covers any of these):
{json.dumps(remaining_list, indent=2)}"""

        client = await self._get_client()
        content = ""

        try:
            if self.backend in ("ollama_cloud", "openrouter"):
                content, tokens_used = await self._call_openai_compatible(user_message)
            else:
                content, tokens_used = await self._call_local_ollama(user_message)

            result = self._parse_response(content)

            return EvaluateResponse(
                target_score=result["target_score"],
                target_reasoning=result["target_reasoning"],
                struck_topics=[
                    StruckTopic(
                        name=s["name"],
                        domain=self._find_domain(s["name"], request.remaining_topics),
                        score=s["score"],
                        reason=s["reason"],
                    )
                    for s in result.get("struck_topics", [])
                ],
                tokens_used=tokens_used,
            )

        except httpx.HTTPError as e:
            logger.error(f"LLM HTTP error: {e}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse LLM response: {e}\nContent: {content}")
            raise

    async def _call_openai_compatible(self, user_message: str) -> tuple[str, int]:
        """Call an OpenAI-compatible chat completions endpoint (Ollama Cloud or OpenRouter)."""
        client = await self._get_client()
        resp = await client.post(
            f"{self.cloud_url}/chat/completions",
            headers=self.cloud_headers,
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                "temperature": 0.1,
                "max_tokens": 2048,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        tokens_used = data.get("usage", {}).get("total_tokens", 0)
        return content, tokens_used

    async def _call_local_ollama(self, user_message: str) -> tuple[str, int]:
        """Call local Ollama's /api/chat endpoint."""
        client = await self._get_client()
        resp = await client.post(
            f"{self.ollama_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 2048,
                },
            },
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["message"]["content"]
        tokens_used = data.get("eval_count", data.get("total_duration", 0))
        return content, tokens_used

    def _parse_response(self, content: str) -> dict:
        """Extract JSON from the LLM response, handling various formats."""
        content = content.strip()
        original = content

        if "```json" in content:
            start = content.index("```json") + 7
            end = content.index("```", start)
            content = content[start:end].strip()
        elif "```" in content:
            start = content.index("```") + 3
            end = content.index("```", start)
            content = content[start:end].strip()

        if not content.startswith("{"):
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                content = match.group(0)

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            fixed = re.sub(r',\s*([}\]])', r'\1', content)
            last_brace = fixed.rfind('}')
            if last_brace != -1:
                fixed = fixed[:last_brace + 1]
            try:
                return json.loads(fixed)
            except json.JSONDecodeError:
                logger.error(
                    f"Failed to parse LLM response after all strategies.\n"
                    f"Original: {original[:500]}\n"
                    f"Cleaned:  {fixed[:500]}"
                )
                raise

    @staticmethod
    def _find_domain(topic_name: str, remaining: list[TopicInfo]) -> str:
        for t in remaining:
            if t.name.lower() == topic_name.lower():
                return t.domain
        return "unknown"

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
