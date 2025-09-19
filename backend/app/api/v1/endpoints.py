from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import AnalysisInput, AnalysisOutput
from app.services.ai_service import ai_service

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"ok": True}

@router.post("/analyze", response_model=AnalysisOutput)
async def analyze(input_data: AnalysisInput):
    if input_data.task != "sentiment":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Tarefa '{input_data.task}' não suportada ainda.")
    if not input_data.input_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="input_text é obrigatório para análise de sentimento.")
    lang = (input_data.options.lang if input_data.options and input_data.options.lang else "auto")
    return await ai_service.analyze_sentiment_local(input_data.input_text, lang)




