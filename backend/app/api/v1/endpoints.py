from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import AnalysisInput, AnalysisOutput, AnalysisResult
import time

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"ok": True}

@router.post("/analyze", response_model=AnalysisOutput)
async def analyze(input_data: AnalysisInput):
    start = time.time()

    if input_data.task != "sentiment":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tarefa '{input_data.task}' não suportada ainda."
        )
    if not input_data.input_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="input_text é obrigatório para análise de sentimento."
        )

    result = AnalysisResult(label="NEUTRAL", score=0.0)
    elapsed = (time.time() - start) * 1000

    return AnalysisOutput(
        task="sentiment",
        engine="local:pending",
        result=result,
        elapsed_ms=elapsed
    )


