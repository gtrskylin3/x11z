from pydantic import BaseModel, Field, ConfigDict

class Word(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    word: str
    translate: str
    context: str | None 
    

class CreateWord(BaseModel):
    word: str
    translate: str | None = Field(default=None, examples=[None])
    context: str | None = Field(default=None, examples=[None])
    
class UpdateWord(BaseModel):
    word: str | None = Field(None, examples=[None])
    translate: str | None = Field(None, examples=[None])
    context: str | None = Field(None, examples=[None])
