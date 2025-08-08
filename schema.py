from pydantic import BaseModel
from typing import Optional
class Entity(BaseModel):
    document_section: str
    condition: Optional[str] = None

class ParsedQuery(BaseModel):
    entity: Entity

