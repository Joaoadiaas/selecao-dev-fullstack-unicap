import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.schemas.prediction import AnalysisOutput, AnalysisResult

analyzer = SentimentIntensityAnalyzer()

class AIService:
    async def analyze_sentiment_local(self, text: str) -> AnalysisOutput:
        start = time.time()
        scores = analyzer.polarity_scores(text)
        label = "NEUTRAL"
        prob = scores["neu"]
        if scores["compound"] >= 0.05:
            label, prob = "POSITIVE", scores["pos"]
        elif scores["compound"] <= -0.05:
            label, prob = "NEGATIVE", scores["neg"]
        return AnalysisOutput(
            task="sentiment",
            engine="local:vader",
            result=AnalysisResult(label=label, score=float(prob)),
            elapsed_ms=(time.time()-start)*1000
        )

ai_service = AIService()
