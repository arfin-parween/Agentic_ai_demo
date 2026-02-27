const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export async function askBackend(message) {
  const res = await fetch(`${BACKEND_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend error: ${res.status} ${text}`);
  }

  return await res.json();
}