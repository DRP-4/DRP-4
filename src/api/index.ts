const API_BASE = import.meta.env.DEV
  ? "http://127.0.0.1:5000"
  : "https://drp-04.herokuapp.com/";


export async function get(route: string): Promise<any> {
  const response = await fetch(`${API_BASE}/api/${route}`);
  return await response.json();
}

export async function post(route: string, value: any): Promise<Response> {
  const body = JSON.stringify(value);
  const response = await fetch(`${API_BASE}/api/${route}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body,
  });
  return response;
}
