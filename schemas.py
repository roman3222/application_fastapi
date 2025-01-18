from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ApplicationBase(BaseModel):
    user_name: str
    description: str

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True
    )