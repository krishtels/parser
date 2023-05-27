from datetime import date, datetime

from pydantic import BaseModel, Field


class Stream(BaseModel):
    user_login: str
    game_name: str
    type: str
    title: str
    viewer_count: int
    language: str
    is_mature: bool
    created: date = Field(default_factory=datetime.today)
