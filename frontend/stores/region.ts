import { defineStore } from "pinia";

export interface RegionData {
  id: number;
  slug: string;
  prefecture: string | null;
  city: string | null;
  water_type: string | null;
  coffee_score: number | null;
  quality: Record<string, unknown> | null;
  [key: string]: unknown;
}

export const useRegionStore = defineStore("region", {
  state: () => ({
    cache: {} as Record<string, RegionData>,
  }),
  actions: {
    set(slug: string, data: RegionData) {
      this.cache[slug] = data;
    },
    get(slug: string): RegionData | null {
      return this.cache[slug] ?? null;
    },
  },
});
