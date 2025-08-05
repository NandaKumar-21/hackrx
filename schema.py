from pydantic import BaseModel

class Entity(BaseModel):
    condition: str
    document_section: str

class ParsedQuery(BaseModel):
    intent: str
    entity: Entity
