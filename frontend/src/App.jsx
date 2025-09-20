import { useState } from "react";
import { analyzeSentiment } from "./api/client";

export default function App() {
  const [text, setText] = useState("");
  const [useExternal, setUseExternal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    if (!text.trim()) { setError("Digite um texto para analisar."); return; }
    try {
      setLoading(true);
      const data = await analyzeSentiment({ text, useExternal });
      setResult(data);
    } catch (err) {
      setError(err.message || "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }

  const label = result?.result?.label || "";
  const labelClass = label === "POSITIVE" ? "badge-label pos" : label === "NEGATIVE" ? "badge-label neg" : "badge-label neu";

  return (
    <div className="container">
      <h1 className="title">Analisador de Sentimento</h1>

      <div className="card">
        <form className="form" onSubmit={onSubmit}>
          <textarea
            className="textarea"
            placeholder="Ex: O atendimento foi excelente, recomendo muito!"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <label className="row">
            <input type="checkbox" checked={useExternal} onChange={(e)=>setUseExternal(e.target.checked)} />
            Usar IA Externa (desmarcado = local)
          </label>
          <button className="btn" type="submit" disabled={loading}>
            {loading ? "Analisando..." : "Analisar"}
          </button>
        </form>
      </div>

      {error && <div className="alert">Erro: {error}</div>}

      {result && (
        <div className="card result">
          <div className="meta">
            <span>Engine:</span><strong>{result.engine}</strong>
            <span>Label:</span><span className={labelClass}>{label}</span>
            <span>Score:</span><strong>{Number(result.result?.score).toFixed(3)}</strong>
            <span>Tempo:</span><span>{Number(result.elapsed_ms).toFixed(2)} ms</span>
          </div>

          {/* Se um dia voltarmos a enviar tokens, basta descomentar a UI abaixo
          {Array.isArray(result?.result?.tokens) && result.result.tokens.length > 0 && (
            <>
              <div className="small">Palavras que influenciaram:</div>
              <div className="chips">
                {result.result.tokens.map((t, i) => (
                  <span key={i} className={`chip ${t.category === "positive" ? "pos" : t.category === "negative" ? "neg" : ""}`}>
                    <strong>{t.token}</strong>
                    <span className="small">{(Math.abs(t.weight)).toFixed(1)}</span>
                  </span>
                ))}
              </div>
            </>
          )}
          */}

          <pre className="small">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

