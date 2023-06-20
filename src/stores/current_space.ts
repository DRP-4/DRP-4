import { spidSocket } from "@/api";
import { isInSession } from "@/api/session";
import { type SpaceID, getDisplayName, joinSpace } from "@/api/spaces";
import { reactive } from "vue";

import { store as tasksStore } from "./tasks";
import { store as sessionStore } from "./session";

function getSpaceIDFromURL(): string | undefined {
  const href = window.location.href;
  const url = new URL(href);
  const res = url.searchParams.get("spid");
  return res === null ? undefined : res;
}

export const store = reactive({
  inSession: false,
  spaceId: undefined as string | undefined,
  displayName: undefined as string | undefined,

  async init() {
    this.inSession = await isInSession();
    if (this.spaceId !== undefined) {
      this.displayName = await getDisplayName();
    }
  },

  async fullOnReload() {
    this.inSession = await isInSession();
    if (this.inSession) {
      await sessionStore.loadFromDB();
    }
    await tasksStore.loadFromDB();
  },

  async switchTo(spaceId: SpaceID | undefined) {
    if (spaceId == this.spaceId) {
      return;
    }

    spidSocket.emit("space-move", { spid: spaceId });
    this.spaceId = spaceId;

    const url = new URL(window.location.origin);
    for (const key of url.searchParams.keys()) {
      url.searchParams.delete(key);
    }
    if (spaceId !== undefined) {
      this.displayName = await getDisplayName();
      url.searchParams.set("spid", spaceId);
    } else {
      this.displayName = undefined;
    }

    window.history.pushState("", "", url);
    await this.fullOnReload();
  },
});

window.addEventListener("popstate", () => {
  store.switchTo(getSpaceIDFromURL());
});

setTimeout(async () => {
  const url = new URL(window.location.href);
  const join = url.searchParams.get("join");
  const spid = url.searchParams.get("spid");
  if (join !== null) {
    url.searchParams.delete("join");
    url.searchParams.set("spid", join);
    window.history.replaceState("", "", url);
    await joinSpace(join);
    await store.switchTo(join);
  } else if (spid !== null) {
    await store.switchTo(spid);
  }
});
