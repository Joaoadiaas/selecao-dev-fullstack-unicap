import re
import unicodedata
from typing import Literal

def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

POS = {
    "excelente": 3.2, "maravilhoso": 3.2, "ótimo": 3.0, "otimo": 3.0,
    "bom": 2.4, "gostei": 2.2, "amei": 3.0, "adorei": 2.8, "perfeito": 3.2,
    "incrível": 3.0, "incrivel": 3.0, "fantástico": 3.2, "fantastico": 3.2,
    "satisfatório": 2.2, "satisfatorio": 2.2, "recomendo": 2.6,
    "eficiente": 2.0, "rápido": 1.8, "rapido": 1.8, "feliz": 1.8
}
NEG = {
    "horrível": -3.2, "horrivel": -3.2, "péssimo": -3.2, "pessimo": -3.2,
    "terrível": -3.0, "terrivel": -3.0, "ruim": -2.4, "odiei": -2.8,
    "detestei": -2.8, "pior": -2.6, "atraso": -1.8, "demorado": -1.8,
    "caro": -1.5, "enganoso": -2.4, "bugado": -2.4, "quebrou": -2.6,
    "defeito": -2.6, "horrendo": -3.0, "medonho": -3.0, "nunca": -1.5,
    "jamais": -1.5, "não": -1.2, "nao": -1.2
}
NEU = { "ok": 0.0, "normal": 0.0, "mediano": 0.0, "razoável": 0.0, "razoavel": 0.0, "regular": 0.0 }

def build_pt_lexicon() -> dict[str, float]:
    lex = {}
    for d in (POS, NEG, NEU):
        for k, v in d.items():
            lex[k] = v
            nk = _strip_accents(k)
            lex[nk] = v
    lex["nunca mais"] = -2.8
    return lex

def inject_pt_lexicon(analyzer) -> None:
    analyzer.lexicon.update(build_pt_lexicon())

def preprocess_for_vader(text: str, lang: Literal["pt","en"] = "pt") -> str:
    if not text or lang != "pt":
        return text
    t = text.lower()
    t = re.sub(r"\bnão\b", " not ", t)
    t = re.sub(r"\bnao\b", " not ", t)
    t = re.sub(r"\bnunca mais\b", " never again ", t)
    return t

PT_MARKERS = ("não","nao","nunca","jamais","ótimo","otimo","péssimo","pessimo","horrível","horrivel","incrível","incrivel","ç","ã","õ","á","é","í","ó","ú")

def detect_lang(text: str) -> Literal["pt","en"]:
    if not text:
        return "en"
    tl = text.lower()
    if any(m in tl for m in PT_MARKERS):
        return "pt"
    return "en"

def extract_evidence_generic(text: str, analyzer) -> list[dict]:
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:\s+mais)?", text.lower())
    ev = []
    for tok in tokens:
        w = analyzer.lexicon.get(tok)
        if w is None:
            w = analyzer.lexicon.get(_strip_accents(tok))
        if w is None:
            continue
        cat = "neutral" if w == 0 else ("positive" if w > 0 else "negative")
        ev.append({"token": tok, "category": cat, "weight": float(w)})
    return ev
