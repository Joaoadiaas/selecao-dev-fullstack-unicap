import re
import unicodedata
from typing import Literal

def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

# --------------------
# POSITIVAS
# --------------------
POS = {
    # gerais
    "excelente": 3.2, "maravilhoso": 3.2, "ótimo": 3.0, "otimo": 3.0,
    "bom": 2.4, "gostei": 2.2, "amei": 3.0, "adorei": 2.8, "perfeito": 3.2,
    "incrível": 3.0, "incrivel": 3.0, "fantástico": 3.2, "fantastico": 3.2,
    "satisfatório": 2.2, "satisfatorio": 2.2, "recomendo": 2.6,
    "eficiente": 2.0, "rápido": 1.8, "rapido": 1.8, "feliz": 1.8,

    # privacidade/segurança
    "seguro": 2.0, "segura": 2.0, "segurança": 1.8, "seguranca": 1.8,
    "transparente": 2.0, "conforme": 1.8, "conformidade": 1.8,

    # app/ux
    "intuitivo": 2.0, "estável": 1.8, "estavel": 1.8,

    # atendimento SAC
    "rápido atendimento": 2.4, "atendimento excelente": 3.0, "suporte ágil": 2.6,
    "suporte agil": 2.6, "ajuda imediata": 2.6, "cordial": 2.0, "educado": 2.0,
    "prestativo": 2.2, "resolutivo": 2.2,

    # portal/titular
    "fácil acesso": 2.2, "facil acesso": 2.2, "autoatendimento": 2.0,
    "portal claro": 2.0, "transparente no portal": 2.2,
}

# --------------------
# NEGATIVAS
# --------------------
NEG = {
    # gerais
    "horrível": -3.2, "horrivel": -3.2, "péssimo": -3.2, "pessimo": -3.2,
    "terrível": -3.0, "terrivel": -3.0, "ruim": -2.4, "odiei": -2.8,
    "detestei": -2.8, "pior": -2.6, "atraso": -1.8, "demorado": -1.8,
    "caro": -1.5, "enganoso": -2.4, "bugado": -2.4, "quebrou": -2.6,
    "defeito": -2.6, "horrendo": -3.0, "medonho": -3.0,
    "nunca": -1.5, "jamais": -1.5, "não": -1.2, "nao": -1.2,

    # privacidade/segurança
    "vazaram": -3.0, "vazamento": -3.0, "vazou": -3.0,
    "exposição": -2.6, "exposicao": -2.6, "incidente": -2.2,
    "multa": -2.0, "condenação": -2.4, "condenacao": -2.4,
    "violação": -2.8, "violacao": -2.8, "quebra de dados": -3.0,

    # app/ux
    "instável": -2.2, "instavel": -2.2, "travando": -2.6, "lento": -2.0,
    "bug": -2.4, "travou": -2.4, "confuso": -2.0, "complicado": -1.8,

    # atendimento SAC
    "atendimento demorado": -2.4, "fila de espera": -2.6,
    "não resolveu": -2.8, "nao resolveu": -2.8, "pouco prestativo": -2.2,
    "arrogante": -2.4, "mal educado": -2.6, "suporte ruim": -2.8,

    # portal/titular
    "difícil acesso": -2.2, "dificil acesso": -2.2, "confuso no portal": -2.0,
    "portal travando": -2.4, "erro no portal": -2.6,
}

# --------------------
# NEUTRAS
# --------------------
NEU = {
    "ok": 0.0, "normal": 0.0, "mediano": 0.0, "razoável": 0.0, "razoavel": 0.0,
    "regular": 0.0, "mudanças": 0.0, "mudancas": 0.0,
    "atualização": 0.0, "atualizacao": 0.0,
    "privacidade": 0.0, "dados": 0.0, "política": 0.0, "politica": 0.0,
    "portal": 0.0, "sac": 0.0,
}

# --------------------
# FUNÇÕES DE SUPORTE
# --------------------
def build_pt_lexicon() -> dict[str, float]:
    lex = {}
    for d in (POS, NEG, NEU):
        for k, v in d.items():
            lex[k] = v
            lex[_strip_accents(k)] = v
    lex["nunca mais"] = -2.8
    return lex

def inject_pt_lexicon(analyzer) -> None:
    analyzer.lexicon.update(build_pt_lexicon())

PT_MARKERS = (
    "não","nao","nunca","jamais",
    "ótimo","otimo","péssimo","pessimo",
    "horrível","horrivel","incrível","incrivel",
    "sac","portal","dados","política","politica",
    "ç","ã","õ","á","é","í","ó","ú"
)

def detect_lang(text: str) -> Literal["pt","en"]:
    if not text:
        return "en"
    tl = text.lower()
    return "pt" if any(m in tl for m in PT_MARKERS) else "en"

def preprocess_for_vader(text: str, lang: Literal["pt","en"] = "pt") -> str:
    if not text or lang != "pt":
        return text
    t = text.lower()
    t = re.sub(r"\bnão\b", " not ", t)
    t = re.sub(r"\bnao\b", " not ", t)
    t = re.sub(r"\bnunca mais\b", " never again ", t)
    return t