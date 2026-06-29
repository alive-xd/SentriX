from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str

class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None
