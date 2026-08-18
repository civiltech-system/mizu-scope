<template>
  <div class="max-w-5xl mx-auto px-4 py-10">
    <Head>
      <Title>水質比較 — 水道水と市販水を比べる</Title>
      <Meta name="description" content="全国の水道水と市販ミネラルウォーターを横断比較。硬度・pH・コーヒー適性を並べて確認。" />
    </Head>

    <h1 class="text-3xl font-bold text-gray-900 mb-2">水質比較</h1>
    <p class="text-gray-500 mb-8">水道水と市販ミネラルウォーターを横断比較できます。</p>

    <!-- 比較テーブル -->
    <div v-if="allItems.length" class="overflow-x-auto mb-8">
      <table class="text-sm border-collapse">
        <thead>
          <tr class="border-b-2 border-gray-200">
            <th class="sticky left-0 z-10 bg-white text-left px-4 py-3 text-gray-500 font-medium w-40 min-w-[160px]">項目</th>
            <th
              v-for="item in allItems"
              :key="item.key"
              class="text-center px-4 py-3 font-semibold text-gray-800 min-w-[140px]"
            >
              <span class="block text-xs font-normal text-gray-400">{{ item.type }}</span>
              {{ item.name }}
              <HardnessBadge :water-type="item.water_type" class="mt-1" />
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <CompareRow label="硬度 (mg/L)" :values="allItems.map((i) => i.hardness)" highlight="min" />
          <CompareRow label="pH"           :values="allItems.map((i) => i.ph)" />
          <CompareRow label="Ca (mg/L)"    :values="allItems.map((i) => i.calcium)" />
          <CompareRow label="Mg (mg/L)"    :values="allItems.map((i) => i.magnesium)" />
          <CompareRow label="Na (mg/L)"    :values="allItems.map((i) => i.sodium)" />
          <CompareRow label="TDS (mg/L)"   :values="allItems.map((i) => i.tds)" highlight="min" />
          <tr class="hover:bg-gray-50">
            <td class="sticky left-0 z-10 bg-white px-4 py-3 text-gray-500">コーヒー適性</td>
            <td v-for="item in allItems" :key="item.key" class="px-4 py-3 text-center">
              <span v-for="i in 5" :key="i" class="text-base" :class="i <= (item.coffee_score ?? 0) ? 'opacity-100' : 'opacity-20'">☕</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!allItems.length" class="text-center py-20 text-gray-400">データを読み込み中...</div>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, h, computed as vComputed } from "vue";

definePageMeta({ layout: "default" });

const config = useRuntimeConfig();

const { data: regions } = await useAsyncData("compare-regions", () =>
  $fetch<{ type: string; features: any[] }>(`${config.public.apiBase}/api/v1/regions`)
);
const { data: commercialWaters } = await useAsyncData("compare-commercial", () =>
  $fetch<any[]>(`${config.public.apiBase}/api/v1/commercial-water`)
);

// 地域 (最初の5件) + 市販水 全件を横並びに
const allItems = computed(() => {
  const regionItems = (regions.value?.features ?? []).slice(0, 5).map((f: any) => ({
    key: `region-${f.properties.id}`,
    name: f.properties.name,
    type: "水道水",
    water_type: f.properties.water_type,
    hardness: f.properties.hardness,
    ph: null as number | null,
    calcium: null as number | null,
    magnesium: null as number | null,
    sodium: null as number | null,
    tds: null as number | null,
    coffee_score: f.properties.coffee_score,
  }));

  const commercialItems = (commercialWaters.value ?? []).map((w: any) => ({
    key: `commercial-${w.id}`,
    name: w.name,
    type: "市販水",
    water_type: w.water_type,
    hardness: w.hardness,
    ph: w.ph,
    calcium: w.calcium,
    magnesium: w.magnesium,
    sodium: w.sodium,
    tds: w.tds,
    coffee_score: w.coffee_score,
  }));

  return [...regionItems, ...commercialItems];
});

// ─── Inline CompareRow component ─────────────────────────────────────────────
type HighlightMode = "min" | "max" | null;
const CompareRow = defineComponent({
  props: {
    label: String,
    values: Array as () => (number | null)[],
    highlight: { type: String as () => HighlightMode, default: null },
  },
  setup(props) {
    const nums = vComputed(() => (props.values ?? []).filter((v): v is number => v != null));
    const minVal = vComputed(() => (nums.value.length ? Math.min(...nums.value) : null));
    const maxVal = vComputed(() => (nums.value.length ? Math.max(...nums.value) : null));

    return () =>
      h("tr", { class: "hover:bg-gray-50" }, [
        h("td", { class: "sticky left-0 z-10 bg-white px-4 py-3 text-gray-500" }, props.label),
        ...(props.values ?? []).map((v, i) => {
          const isHighlight =
            v != null &&
            ((props.highlight === "min" && v === minVal.value) ||
              (props.highlight === "max" && v === maxVal.value));
          return h(
            "td",
            {
              key: i,
              class: `px-4 py-3 text-center font-medium ${isHighlight ? "text-blue-600 font-bold" : "text-gray-700"}`,
            },
            v != null ? String(v) : "—"
          );
        }),
      ]);
  },
});
</script>
