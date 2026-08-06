"""Pydantic models for the AI Knowledge Quiz backend."""

from pydantic import BaseModel, Field
from typing import Optional


class TopicInfo(BaseModel):
    """A single topic from the heatmap."""
    name: str
    domain: str
    level: int = Field(ge=1, le=4, description="Current score 1-4")


class EvaluateRequest(BaseModel):
    """Request to evaluate a user's explanation for a topic."""
    target_topic: str = Field(description="The topic the user is answering about")
    target_domain: str = Field(description="The domain the target topic belongs to")
    explanation: str = Field(
        min_length=10,
        max_length=5000,
        description="User's free-text explanation of their knowledge"
    )
    remaining_topics: list[TopicInfo] = Field(
        default_factory=list,
        description="All topics still pending evaluation (for cross-topic credit detection)"
    )
    session_id: str = Field(description="Unique session identifier")


class StruckTopic(BaseModel):
    """A topic that was auto-evaluated via cross-topic credit."""
    name: str
    domain: str
    score: int = Field(ge=1, le=4)
    reason: str = Field(description="Why this topic was struck (what the user said that covered it)")


class EvaluateResponse(BaseModel):
    """Response from the LLM evaluator."""
    target_score: int = Field(ge=1, le=4, description="Score for the target topic (1-4)")
    target_reasoning: str = Field(description="Why this score was assigned")
    struck_topics: list[StruckTopic] = Field(
        default_factory=list,
        description="Topics that were auto-evaluated via cross-topic credit"
    )
    tokens_used: int = Field(default=0, description="LLM tokens consumed")


class SessionSummary(BaseModel):
    """Summary of a completed quiz session."""
    session_id: str
    topics_evaluated: int
    topics_struck: int
    domain_scores: dict[str, dict] = Field(
        default_factory=dict,
        description="Per-domain: {count, L1, L2, L3, L4 counts}"
    )


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    ollama_available: bool
    model: str
