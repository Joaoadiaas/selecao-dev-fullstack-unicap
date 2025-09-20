import { useMemo, useState } from "react";
import { analyzeSentiment } from "./api/client";

const PRODUCTS = [
  "Portal do Titular",
  "Política de Privacidade",
  "Atendimento SAC",
  "App Mobile",
];

export default function App() {
  const [product, setProduct] = useState(PRODUCTS[0]);
  const [text, setText] = useState("");
  const [useExternal, setUseExternal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  // histórico por produto: { [produto]: Array<{text,label,score,at}> }
  const [history, setHistory] = useState({});
  const currentHistory = useMemo(() => history[product] ?? [], [history, product]);

  async function onSubmit(e) {
    e?.preventDefault?.();
    setError("");
    setResult(null);

    const value = text.trim();
    if (!value) { setError("Digite um texto para analisar."); return; }
    if (value.length > 5000) { setError("Texto acima de 5000 caracteres."); return; }

    try {
      setLoading(true);
      const data = await analyzeSentiment({ text: value, useExternal });
      setResult(data);

      // atualiza histórico deste produto (máx 5)
      setHistory(prev => {
        const prevList = prev[product] ?? [];
        const entry = {
          text: value,
          label: data?.result?.label ?? "-",
          score: Number(data?.result?.score ?? 0),
          at: new Date().toISOString(),
        };
        const next = [entry, ...prevList].slice(0, 5);
        return { ...prev, [product]: next };
      });
    } catch (err) {
      setError(err.message || "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!loading) onSubmit(e);
    }
  }

  const label = result?.result?.label || "";
  const labelClass =
    label === "POSITIVE" ? "badge-label pos" :
    label === "NEGATIVE" ? "badge-label neg" : "badge-label neu";

  return (
    <div className="container">
      <h1 className="title">Analisador de Sentimento</h1>

      <div className="card">
        <form className="form" onSubmit={onSubmit}>
          {/* Produto */}
          <div className="row" style={{ gap: 8 }}>
            <span className="small">Produto:</span>
            <select
              value={product}
              onChange={(e) => setProduct(e.target.value)}
              style={{
                background: "#0b0d14",
                color: "var(--text)",
                border: "1px solid var(--border)",
                borderRadius: 8,
                padding: "8px 10px"
              }}
            >
              {PRODUCTS.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
            <span className="small" style={{ marginLeft: 8 }}>
              (Enter = analisar • Shift+Enter = nova linha)
            </span>
          </div>

          <textarea
            className="textarea"
            placeholder="Cole aqui o feedback do cliente para este produto..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            maxLength={5000}
          />

          <label className="row">
            <input
              type="checkbox"
              checked={useExternal}
              onChange={(e)=>setUseExternal(e.target.checked)}
            />
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
            <span>Produto:</span><strong>{product}</strong>
            <span>Engine:</span><strong>{result.engine}</strong>
            <span>Label:</span><span className={labelClass}>{label}</span>
            <span>Score:</span><strong>{Number(result.result?.score).toFixed(3)}</strong>
            <span>Tempo:</span><span>{Number(result.elapsed_ms).toFixed(2)} ms</span>
          </div>
          <pre className="small">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {/* Histórico deste produto */}
      <div className="card result">
        <div className="meta"><strong>Histórico (últimos 5) — {product}</strong></div>
        {currentHistory.length === 0 ? (
          <div className="small" style={{ padding: "0 16px 12px" }}>
            Sem análises para este produto ainda.
          </div>
        ) : (
          <ul style={{ listStyle: "none", padding: "0 16px 16px", margin: 0 }}>
            {currentHistory.map((h, i) => (
              <li key={i} style={{ padding: "10px 0", borderBottom: "1px solid var(--border)" }}>
                <div className="row" style={{ gap: 10 }}>
                  <span className={
                    h.label === "POSITIVE" ? "badge-label pos" :
                    h.label === "NEGATIVE" ? "badge-label neg" : "badge-label neu"
                  }>
                    {h.label}
                  </span>
                  <span className="small">score {h.score.toFixed(3)}</span>
                  <span className="small">em {new Date(h.at).toLocaleString()}</span>
                </div>
                <div className="small" style={{ marginTop: 6, color: "var(--text)" }}>
                  {h.text}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}



