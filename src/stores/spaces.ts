import { reactive } from "vue";
import {
  spaces,
  createNewSpace,
  deleteSpace,
  type SpaceID,
  Space,
} from "@/api/spaces";

export const store = reactive({
  spaces: new Map<SpaceID, Space>(),

  async loadFromDB() {
    this.spaces = await spaces();
  },

  async add(displayName: string) {
    const id = await createNewSpace(displayName);
    this.spaces.set(id, new Space(id, displayName));
  },

  async remove(id: SpaceID) {
    this.spaces.delete(id);
    await deleteSpace(id);
  },

  sortedSpacesList(): Space[] {
    return [...this.spaces.values()].sort((l, r) =>
      l.displayName.localeCompare(r.displayName)
    );
  },
});
