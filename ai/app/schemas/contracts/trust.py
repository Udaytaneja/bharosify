from typing import Optional
from pydantic import BaseModel, Field


class TrustFactorDTO(BaseModel):
    """Canonical contract DTO for Trust Profile Factors."""
    trust_profile_id: str = Field(description="Trust profile identifier")
    name: str = Field(description="Factor human-readable name")
    impact: str = Field(description="Impact direction e.g. positive, negative, neutral")
    value: str = Field(description="Formatted feature value")
    description: str = Field(description="Auditable description of factor impact")
    weight: float = Field(default=1.0, description="Factor weighting score")
    confidence: float = Field(default=0.95, description="Confidence in factor assessment")
