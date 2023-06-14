import { reactive } from "vue";
import { type Session, getSession, endSession } from "@/api/session";

export const store = reactive({
  session: undefined as undefined | Session,

  async loadFromDB() {
    this.session = await getSession();
  },

  async endSession() {
    if (this.session !== undefined) {
      await endSession();
    }
    this.session = undefined;
  },
});
