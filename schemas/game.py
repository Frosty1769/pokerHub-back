from pydantic import BaseModel

class MyBaseModel(BaseModel):
    class Config:
        pass
        # extra: 'forbid'

class Game(MyBaseModel):
    id: str
    name: str
    description: str
    deposit: int
    max_players: int

    