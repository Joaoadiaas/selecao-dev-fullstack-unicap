import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.schemas.prediction import AnalysisOutput, AnalysisResult
from app.services.lang_utils import inject_pt_lexicon, preprocess_for_vader, detect_lang

analyzer = SentimentIntensityAnalyzer()
inject_pt_lexicon(analyzer)

class AIService:
    async def analyze_sentiment_local(self, text: str, lang: str = "auto") -> AnalysisOutput:
        start = time.time()

        effective_lang = detect_lang(text) if (lang == "auto") else lang
        prep = preprocess_for_vader(text, "pt" if effective_lang == "pt" else "en")

        scores = analyzer.polarity_scores(prep)

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
            elapsed_ms=(time.time() - start) * 1000.0,
        )

ai_service = AIService()


