🚀 Analisador de Sentimento (PT/EN) – Fullstack

Aplicação fullstack desenvolvida como desafio técnico.
Integra FastAPI (backend) e React + Vite (frontend) para análise de sentimentos em Português e Inglês, com suporte a vocabulário expandido em domínios específicos (Privacidade, SAC, Portal, Aplicativo).

📌 Arquitetura
desafio/
│── backend/
│   ├── app/
│   │   ├── api/v1/endpoints.py   # Endpoints REST
│   │   ├── schemas/prediction.py # Modelos de request/response
│   │   ├── services/ai_service.py # Serviço de análise
│   │   └── services/lang_utils.py # Utilidades de idioma (PT/EN)
│── frontend/
│   └── src/App.jsx               # UI principal (formulário + histórico)

⚙️ Funcionalidades

Análise de Sentimento (PT/EN) com detecção automática de idioma.

Vocabulário customizado (PT):

Privacidade: “vazaram dados”, “violação”, “seguro”, “transparente”.

SAC: “atendimento excelente”, “fila de espera”, “não resolveu”.

Portal: “portal claro”, “difícil acesso”, “erro no portal”.

App: “adorei a atualização”, “instável”, “travando”.

Frontend contextualizado:

Dropdown de Produto (Portal, Política de Privacidade, SAC, App).

Histórico de últimos 5 feedbacks por produto.

Tema escuro estilizado e badges coloridas (POSITIVO/NEGATIVO/NEUTRO).

API REST estruturada:

GET /api/v1/healthz → health check.

GET /api/v1/ping → resposta rápida {ok: true}.

POST /api/v1/analyze → análise de texto.

▶️ Como rodar localmente
🔹 Requisitos

Python 3.10+

Node.js 18+

npm

🔹 Backend
cd backend
python -m venv venv


Ativar ambiente virtual:

Windows (PowerShell):

.\venv\Scripts\Activate.ps1


Linux/Mac:

source venv/bin/activate


Instalar dependências e rodar servidor:

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000


Testes rápidos:

http://localhost:8000/api/v1/healthz
 → {"status":"ok"}

http://localhost:8000/api/v1/ping
 → {"ok":true}

Swagger: http://localhost:8000/docs

🔹 Frontend

Crie um arquivo .env dentro de frontend/ com:

VITE_API_BASE_URL=http://localhost:8000/api/v1


Rodar:

cd frontend
npm install
npm run dev


Abrir no navegador:
👉 http://localhost:5173

📡 Exemplo de Requisição/Resposta

Request (POST /api/v1/analyze):

{
  "task": "sentiment",
  "input_text": "O atendimento foi excelente!",
  "use_external": false,
  "options": { "lang": "auto" }
}


Response:

{
  "id": "uuid",
  "task": "sentiment",
  "engine": "local:vader",
  "result": { "label": "POSITIVE", "score": 0.98 },
  "elapsed_ms": 15.2,
  "received_at": "2025-09-20T00:00:00Z"
}

✅ Checklist atendido

 Backend em FastAPI com endpoints /analyze, /healthz, /ping.

 Processamento real (não mockado) em PT/EN.

 Frontend em React consumindo API.

 Estados de loading e erro implementados.

 Layout estilizado com feedback visual claro.

 Código modular (API → Service → Schema).

 README explicativo e exemplo de execução.
