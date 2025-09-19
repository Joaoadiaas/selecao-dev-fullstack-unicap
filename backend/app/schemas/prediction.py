from typing import Optional, Literal
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class InputOptions(BaseModel):
    lang: Optional[str] = "pt"

class AnalysisInput(BaseModel):
    task: Literal["sentiment","ner","ocr","caption","custom"] = "sentiment"
    input_text: Optional[str] = None
    use_external: Optional[bool] = None
    options: Optional[InputOptions] = InputOptions()

class AnalysisResult(BaseModel):
    label: str
    score: float

class AnalysisOutput(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    task: Literal["sentiment","ner","ocr","caption","custom"]
    engine: str
    result: AnalysisResult
    elapsed_ms: float
    received_at: datetime = Field(default_factory=datetime.utcnow)
