import { io } from "socket.io-client";
import { store as currentSpaceStore } from "@/stores/current_space";

const API_BASE = import.meta.env.DEV
  ? "http://127.0.0.1:5000"
  : "https://drp-04.herokuapp.com";

export const socket = io(API_BASE, { withCredentials: true });
export const spidSocket = io(`${API_BASE}/spid`, { withCredentials: true });
export const spidGoneSocket = io(`${API_BASE}/spid/gone`, {
  withCredentials: true,
});

function newAPIRequest(route: String): Request {
  const url = new URL(`${API_BASE}/api/${route}`);
  if (currentSpaceStore.spaceId !== undefined) {
    url.searchParams.append("spid", currentSpaceStore.spaceId);
  }
  return new Request(url, { credentials: "include" });
}

spidSocket.on("space-update", async (body) => {
  if (body.id != currentSpaceStore.spaceId) {
    // Wrong space identifier
    return;
  }
  await currentSpaceStore.fullOnReload();
});

export async function get(route: string): Promise<any> {
  const response = await fetch(newAPIRequest(route));
  return await response.json();
}

export async function post(route: string, value: any): Promise<Response> {
  const body = JSON.stringify({ ...value, exclude_sid: socket.id });
  const response = await fetch(newAPIRequest(route), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body,
  });
  return response;
}

export async function del(route: string, value: any): Promise<Response> {
  const body = JSON.stringify({ ...value, exclude_sid: socket.id });
  const response = await fetch(newAPIRequest(route), {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body,
  });
  return response;
}

export async function put(route: string, value: any): Promise<Response> {
  const body = JSON.stringify({ ...value, exclude_sid: socket.id });
  const response = await fetch(newAPIRequest(route), {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body,
  });
  return response;
}
