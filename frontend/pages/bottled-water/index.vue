<template>
  <div class="max-w-5xl mx-auto px-4 py-10">
    <Head>
      <Title>市販ミネラルウォーター水質一覧</Title>
      <Meta
        name="description"
        content="エビアン・南アルプス・ヴォルビックなど市販ミネラルウォーターの硬度・pH・コーヒー適性を比較。水道水との違いも確認できます。"
      />
    </Head>

    <h1 class="text-3xl font-bold text-gray-900 mb-2">市販ミネラルウォーター 水質データ</h1>
    <p class="text-gray-500 mb-6">硬度・pH・コーヒー適性で各商品を比較できます。</p>

    <!-- フィルター -->
    <div class="flex gap-2 mb-6 flex-wrap">
      <button
        v-for="opt in filterOptions"
        :key="opt.value"
        class="px-3 py-1.5 rounded-full text-sm font-medium border transition-colors"
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

    <!-- カード一覧 -->
    <div v-if="filtered?.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <NuxtLink
        v-for="w in filtered"
        :key="w.id"
        :to="`/bottled-water/${w.id}`"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:border-blue-300 transition-colors block"
      >
        <div class="flex justify-between items-start mb-2">
          <div>
            <p class="font-bold text-gray-900">{{ w.name }}</p>
            <p class="text-xs text-gray-400">{{ w.brand }} / {{ countryLabel(w.country_code) }}</p>
          </div>
          <HardnessBadge :water-type="w.water_type" />
        </div>
        <div class="grid grid-cols-2 gap-1 text-sm text-gray-600 mb-3">
          <p>硬度: <span class="font-medium">{{ w.hardness }} mg/L</span></p>
          <p>pH: <span class="font-medium">{{ w.ph }}</span></p>
          <p>Ca: <span class="font-medium">{{ w.calcium }} mg/L</span></p>
          <p>Mg: <span class="font-medium">{{ w.magnesium }} mg/L</span></p>
        </div>
        <div class="flex items-center gap-1 text-amber-600">
          <span v-for="i in 5" :key="i" class="text-sm" :class="i <= (w.coffee_score ?? 0) ? 'opacity-100' : 'opacity-20'">☕</span>
          <span class="text-xs text-gray-500 ml-1">コーヒー適性</span>
        </div>
      </NuxtLink>
    </div>

    <div v-else class="text-center py-20 text-gray-400">データを読み込み中...</div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "default" });

const config = useRuntimeConfig();
const { data: waters } = await useAsyncData("commercial-waters", () =>
  $fetch<Record<string, any>[]>(`${config.public.apiBase}/api/v1/commercial-water`)
);

type FilterValue = "all" | "soft" | "medium" | "hard" | "very_hard";
const activeFilter = ref<FilterValue>("all");

const filterOptions: { label: string; value: FilterValue }[] = [
  { label: "すべて",   value: "all" },
  { label: "軟水",     value: "soft" },
  { label: "中硬水",   value: "medium" },
  { label: "硬水",     value: "hard" },
  { label: "超硬水",   value: "very_hard" },
];

const filtered = computed(() => {
  if (!waters.value) return [];
  if (activeFilter.value === "all") return waters.value;
  return waters.value.filter((w) => w.water_type === activeFilter.value);
});

const countryLabel = (code: string | null) =>
  ({ jpn: "日本", fra: "フランス", usa: "アメリカ" }[code ?? ""] ?? code ?? "");
</script>
