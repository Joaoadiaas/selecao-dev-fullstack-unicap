const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export async function analyzeSentiment({ text, useExternal = false, lang = "pt" }) {
  const body = {
    task: "sentiment",
    input_text: text,
    use_external: useExternal,
    options: { lang }
  };

  const res = await fetch(`${baseURL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const msg = err?.detail || `Erro HTTP ${res.status}`;
    throw new Error(msg);
  }

  return res.json();
}
