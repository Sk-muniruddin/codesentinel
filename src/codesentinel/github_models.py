from pydantic import BaseModel, Field


class PullRequestContext(BaseModel):
    owner: str = Field(min_length=1)
    repository: str = Field(min_length=1)
    pull_number: int = Field(gt=0)
    action: str = Field(min_length=1)
    installation_id: int = Field(gt=0)