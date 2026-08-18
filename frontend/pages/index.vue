<template>
  <div>
    <Head>
      <Title>水質マップ — 日本全国の水道水 硬度・pH・飲用可否</Title>
      <Meta
        name="description"
        content="日本全国の水道水の硬度・pH・飲用可否をインタラクティブな地図で確認。コーヒーに適した水や市販ミネラルウォーターとの比較も。"
      />
    </Head>

    <!-- Map area -->
    <div class="relative" style="height: calc(100vh - 64px)">
      <!-- Filter bar -->
      <div class="absolute top-3 left-1/2 -translate-x-1/2 z-20 flex gap-2">
        <button
          v-for="opt in filterOptions"
          :key="opt.value"
          class="px-3 py-1.5 rounded-full text-xs font-medium shadow-sm border transition-colors"
          :class="
            activeFilter === opt.value
              ? 'bg-blue-600 text-white border-blue-600'
              : 'bg-white text-gray-600 border-gray-200 hover:border-blue-400'
          "
          @click="activeFilter = opt.value"
        >
          {{ opt.label }}
        </button>
      </div>

      <!-- Map (client only — MapLibre requires browser APIs) -->
      <ClientOnly>
        <WaterMap
          v-if="filteredGeoJson"
          :regions="filteredGeoJson"
          class="absolute inset-0"
        />
        <template #fallback>
          <div class="absolute inset-0 flex items-center justify-center bg-blue-50">
            <p class="text-gray-500">地図を読み込み中...</p>
          </div>
        </template>
      </ClientOnly>

      <!-- Loading spinner -->
      <div
        v-if="pending"
        class="absolute inset-0 flex items-center justify-center bg-white/60 z-30"
      >
        <div
          class="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"
        />
      </div>

      <!-- Legend -->
      <div class="absolute bottom-8 left-4 bg-white rounded-xl shadow-lg p-4 text-sm z-10">
        <p class="font-semibold text-gray-700 mb-2">硬度（mg/L）</p>
        <div class="space-y-1.5">
          <LegendRow color="bg-blue-500"   label="軟水（〜60）" />
          <LegendRow color="bg-green-500"  label="中硬水（61〜120）" />
          <LegendRow color="bg-yellow-500" label="硬水（121〜180）" />
          <LegendRow color="bg-red-500"    label="超硬水（181〜）" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, h } from "vue";
import WaterMap from "~/components/map/WaterMap.vue";

definePageMeta({ layout: "default" });

const LegendRow = defineComponent({
  props: { color: String, label: String },
  setup(props) {
    return () =>
      h("div", { class: "flex items-center gap-2" }, [
        h("span", { class: `w-3.5 h-3.5 rounded-full ${props.color} inline-block` }),
        h("span", { class: "text-gray-600 text-xs" }, props.label),
      ]);
  },
});

const config = useRuntimeConfig();

const { data: geojson, pending } = await useAsyncData("regions-geojson", () => {
  const base = import.meta.server ? config.apiBase : config.public.apiBase;
  return $fetch<{ type: string; features: unknown[] }>(`${base}/api/v1/regions`);
});

type FilterValue = "all" | "soft" | "medium" | "hard" | "very_hard";
const activeFilter = ref<FilterValue>("all");

const filterOptions: { label: string; value: FilterValue }[] = [
  { label: "すべて",   value: "all" },
  { label: "軟水",     value: "soft" },
  { label: "中硬水",   value: "medium" },
  { label: "硬水",     value: "hard" },
  { label: "超硬水",   value: "very_hard" },
];

const filteredGeoJson = computed(() => {
  if (!geojson.value) return null;
  if (activeFilter.value === "all") return geojson.value;
  return {
    ...geojson.value,
    features: (geojson.value.features as any[]).filter(
      (f) => f.properties.water_type === activeFilter.value
    ),
  };
});
</script>

