const API_BASE = import.meta.env.DEV
  ? "http://127.0.0.1:5000"
  : "https://drp-04.herokuapp.com/";

function newAPIRequest(route: String): Request {
  // Include credentials for the cookie to be included
  return new Request(`${API_BASE}/api/${route}`, { credentials: "include" });
}

export async function get(route: string): Promise<any> {
  const response = await fetch(newAPIRequest(route));
  return await response.json();
}

export async function post(route: string, value: any): Promise<Response> {
  const body = JSON.stringify(value);
  const response = await fetch(newAPIRequest(route), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body,
  });
  return response;
}
