import { reactive } from "vue";
import {
  spaces,
  createNewSpace,
  deleteSpace,
  leaveSpace,
  type SpaceID,
  Space,
} from "@/api/spaces";

import { spidGoneSocket } from "@/api/index";
import { store as currentSpaceStore } from "@/stores/current_space";

export const store = reactive({
  spaces: new Map<SpaceID, Space>(),

  async resubscribe() {
    const ids = [...this.spaces.keys()];
    spidGoneSocket.emit("callback-on-term", { ids });
  },

  async loadFromDB() {
    this.spaces = await spaces();

    // Subscribe to removal notifications
    await this.resubscribe();
  },

  async add(displayName: string) {
    const id = await createNewSpace(displayName);
    this.spaces.set(id, new Space(id, displayName, true));
    await this.resubscribe();
  },

  async remove(id: SpaceID, method?: "del" | "leave") {
    if (!this.spaces.has(id)) {
      return;
    }
    if (currentSpaceStore.spaceId == id) {
      // Preventively switch to home
      currentSpaceStore.switchTo(undefined);
    }
    this.spaces.delete(id);
    if (method === "del") {
      await deleteSpace(id);
    } else if (method == "leave") {
      await leaveSpace(id);
    }
  },

  sortedSpacesList(): Space[] {
    return [...this.spaces.values()].sort((l, r) =>
      l.displayName.localeCompare(r.displayName)
    );
  },
});

spidGoneSocket.on("space-removal", async (body) => {
  if (body.id == currentSpaceStore.spaceId) {
    // Switch to home
    await currentSpaceStore.switchTo(undefined);
  }
  // Remove the ID
  await store.remove(body.id);
});
