from pydantic import BaseModel

class RegionResponse(BaseModel):
    id: int
    name: str
    nb_habitants: int
    language: str