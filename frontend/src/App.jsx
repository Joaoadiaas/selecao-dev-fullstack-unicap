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

    if (!text.trim()) {
      setError("Digite um texto para analisar.");
      return;
    }

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

  return (
    <div style={{ maxWidth: 720, margin: "40px auto", fontFamily: "Inter, system-ui, Arial", padding: 16 }}>
      <h1 style={{ marginBottom: 8 }}>Analisador de Sentimento</h1>
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12, marginTop: 16 }}>
        <textarea
          rows={5}
          placeholder="Ex: O atendimento foi excelente, recomendo muito!"
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{ padding: 12, fontSize: 16, borderRadius: 8, border: "1px solid #ddd" }}
        />
        <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <input
            type="checkbox"
            checked={useExternal}
            onChange={(e) => setUseExternal(e.target.checked)}
          />
          Usar IA Externa (desmarcado = local)
        </label>
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "10px 16px",
            fontSize: 16,
            borderRadius: 8,
            border: "1px solid #111",
            background: loading ? "#eee" : "#111",
            color: loading ? "#111" : "#fff",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Analisando..." : "Analisar"}
        </button>
      </form>

      {error && (
        <div style={{ marginTop: 16, padding: 12, border: "1px solid #e00", borderRadius: 8, color: "#900", background: "#fee" }}>
          Erro: {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: 16, padding: 16, border: "1px solid #ddd", borderRadius: 12 }}>
          <div style={{ display: "flex", gap: 8, alignItems: "baseline", marginBottom: 8 }}>
            <span style={{ fontSize: 14, color: "#666" }}>Engine:</span>
            <strong>{result.engine}</strong>
          </div>
          <div style={{ display: "flex", gap: 8, alignItems: "baseline", marginBottom: 8 }}>
            <span style={{ fontSize: 14, color: "#666" }}>Label:</span>
            <strong>{result.result?.label}</strong>
            <span style={{ fontSize: 14, color: "#666" }}>Score:</span>
            <strong>{Number(result.result?.score).toFixed(3)}</strong>
          </div>
          <pre style={{ background: "#f7f7f8", padding: 12, borderRadius: 8, overflowX: "auto" }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
