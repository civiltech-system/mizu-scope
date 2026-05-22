import { defineStore } from "pinia";

export type WaterTypeFilter = "all" | "soft" | "medium" | "hard" | "very_hard";

export const useMapStore = defineStore("map", {
  state: () => ({
    viewport: { lat: 36.5, lng: 136.5, zoom: 5 },
    filter: {
      waterType: "all" as WaterTypeFilter,
      drinkable: null as boolean | null,
    },
  }),
  actions: {
    setViewport(lat: number, lng: number, zoom: number) {
      this.viewport = { lat, lng, zoom };
    },
    setWaterTypeFilter(type: WaterTypeFilter) {
      this.filter.waterType = type;
    },
  },
});
