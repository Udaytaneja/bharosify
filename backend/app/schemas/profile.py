from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    name: str
    email: EmailStr
    phone: str | None = None
    language: str
    profile_status: str = "complete"


class UserProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    phone: str | None = Field(default=None, max_length=30)
    language: str | None = Field(default=None, max_length=5)
