
**Camadas**  
- **API**: `app/api/v1/endpoints.py`  
- **Contratos**: `app/schemas/prediction.py`  
- **Serviço de IA**: `app/services/ai_service.py`  
- **Utilidades de idioma**: `app/services/lang_utils.py` (léxico PT/EN expandido)  
- **Frontend**: `src/App.jsx` (seletor de produto + histórico)  

---

## Funcionalidades

- **PT/EN autodetectado** com pré-processamento.  
- **Léxico PT customizado** cobre:
  - **Privacidade**: “vazaram dados”, “violação”, “seguro”, “transparente”  
  - **SAC**: “atendimento excelente”, “fila de espera”, “não resolveu”  
  - **Portal**: “portal claro”, “difícil acesso”, “erro no portal”  
  - **App**: “adorei a atualização”, “instável”, “confuso”, “travando”  
- **Frontend contextualizado**:
  - Dropdown de **Produto** (Portal, Política de Privacidade, SAC, App).  
  - **Histórico local** (últimos 5 feedbacks por produto).  
  - Tema escuro estilizado, badges coloridas (POSITIVE/NEGATIVE/NEUTRAL).  

---

## Como rodar localmente

### Requisitos
- **Python 3.10+** e **pip**
- **Node 18+** e **npm**


### BACKEND

cd backend
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --port 8000

Testes rápidos:
http://localhost:8000/api/v1/healthz → {"status":"ok"}

http://localhost:8000/api/v1/ping → {"ok": true}

Docs Swagger: http://localhost:8000/docs

### FRONTEND
Crie o arquivo .env dentro de frontend/ com:
VITE_API_BASE_URL=http://localhost:8000/api/v1
Depois rode:
cd frontend
npm install
npm run dev

# abra http://localhost:5173

Endpoints principais

-GET /api/v1/healthz
{"status":"ok"}

-GET /api/v1/ping
{"ok":true}
POST /api/v1/analyze

EX: Request (JSON)

{
  "task": "sentiment",
  "input_text": "O atendimento foi excelente!",
  "use_external": false,
  "options": { "lang": "auto" }
}


EX: Response (JSON)

{
  "id": "uuid",
  "task": "sentiment",
  "engine": "local:vader",
  "result": { "label": "POSITIVE", "score": 0.98 },
  "elapsed_ms": 15.2,
  "received_at": "2025-09-20T00:00:00Z"
}

