"""SensingEngine: LLM-powered evaluator with cross-topic credit detection.

Sends a user's explanation to Ollama and asks it to:
1. Score the target topic (L1-L4)
2. Detect collateral knowledge about other pending topics
3. Auto-strike topics that were sufficiently covered
"""

import json
import logging
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
    """Evaluates user explanations via Ollama LLM."""

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

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def health_check(self) -> bool:
        """Check if Ollama is reachable and the model is available."""
        try:
            client = await self._get_client()
            resp = await client.get(f"{self.ollama_url}/api/tags")
            if resp.status_code != 200:
                return False
            data = resp.json()
            models = [m["name"] for m in data.get("models", [])]
            # Check if our model (or a prefix match) exists
            return any(self.model in m or m.startswith(self.model.split(":")[0]) for m in models)
        except Exception:
            return False

    async def evaluate(self, request: EvaluateRequest) -> EvaluateResponse:
        """Evaluate a user's explanation and detect cross-topic credit."""
        # Cap remaining topics to prevent the LLM from trying to evaluate all 140+
        # Only send topics in the same domain + a sample from other domains
        same_domain = [t for t in request.remaining_topics if t.domain == request.target_domain]
        other_domains = [t for t in request.remaining_topics if t.domain != request.target_domain]
        # Take all same-domain topics + up to 20 from other domains
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
                        "temperature": 0.1,  # Low temp for consistent scoring
                        "num_predict": 2048,
                    },
                },
            )
            resp.raise_for_status()
            data = resp.json()

            # Extract the assistant's response
            content = data["message"]["content"]
            tokens_used = data.get("eval_count", data.get("total_duration", 0))

            # Parse the JSON from the response
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
            logger.error(f"Ollama HTTP error: {e}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse Ollama response: {e}\nContent: {content}")
            raise

    def _parse_response(self, content: str) -> dict:
        """Extract JSON from the LLM response, handling various formats."""
        import re

        content = content.strip()
        original = content  # keep for error logging

        # Strategy 1: extract from ```json ... ``` block
        if "```json" in content:
            start = content.index("```json") + 7
            end = content.index("```", start)
            content = content[start:end].strip()
        # Strategy 2: extract from ``` ... ``` block
        elif "```" in content:
            start = content.index("```") + 3
            end = content.index("```", start)
            content = content[start:end].strip()

        # Strategy 3: find the outermost { ... } pair
        if not content.startswith("{"):
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                content = match.group(0)

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Strategy 4: try to fix common LLM JSON issues
            # Remove trailing commas before closing braces/brackets
            fixed = re.sub(r',\s*([}\]])', r'\1', content)
            # Remove any text after the final closing brace
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
        """Find the domain for a topic name from the remaining list."""
        for t in remaining:
            if t.name.lower() == topic_name.lower():
                return t.domain
        return "unknown"

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
