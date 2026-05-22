<template>
  <div class="max-w-3xl mx-auto px-4 py-10">
    <div v-if="!water" class="text-center py-20 text-gray-400">
      商品情報が見つかりませんでした。
      <NuxtLink to="/bottled-water" class="text-blue-600 block mt-2">一覧に戻る</NuxtLink>
    </div>

    <template v-else>
      <Head>
        <Title>{{ water.name }} 水質データ — 硬度{{ water.hardness }}mg/L</Title>
        <Meta
          name="description"
          :content="`${water.name}（${water.brand}）の水質データ。硬度${water.hardness}mg/L・pH${water.ph}の${waterTypeJa}。コーヒー適性スコア${water.coffee_score}/5。`"
        />
      </Head>

      <nav class="flex gap-1 text-sm text-gray-400 mb-4">
        <NuxtLink to="/bottled-water" class="hover:text-blue-600">市販水一覧</NuxtLink>
        <span>/</span>
        <span class="text-gray-700">{{ water.name }}</span>
      </nav>

      <div class="mb-8">
        <div class="flex items-center gap-3 mb-1">
          <h1 class="text-3xl font-bold text-gray-900">{{ water.name }}</h1>
          <HardnessBadge :water-type="water.water_type" />
        </div>
        <p class="text-gray-500">{{ water.brand }} | 原産国: {{ countryLabel }}</p>
        <p v-if="water.water_source" class="text-gray-400 text-sm mt-1">水源: {{ water.water_source }}</p>
      </div>

      <!-- サマリーカード -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div v-for="card in summaryCards" :key="card.label" class="bg-white rounded-xl shadow-sm p-4 text-center border border-gray-100">
          <p class="text-xs text-gray-500 mb-1">{{ card.label }}</p>
          <p class="text-2xl font-bold text-gray-900">{{ card.value ?? "—" }}</p>
          <p v-if="card.unit" class="text-xs text-gray-400">{{ card.unit }}</p>
        </div>
      </div>

      <!-- コーヒー適性 -->
      <CoffeeScore :score="water.coffee_score" class="mb-8" />

      <!-- 詳細テーブル -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-8">
        <div class="px-6 py-4 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-900">詳細水質データ</h2>
        </div>
        <table class="w-full text-sm">
          <tbody class="divide-y divide-gray-50">
            <tr v-for="row in detailRows" :key="row.label" class="hover:bg-gray-50">
              <td class="px-6 py-3 text-gray-500 w-48">{{ row.label }}</td>
              <td class="px-6 py-3 font-medium text-gray-900">
                {{ row.value != null ? `${row.value} ${row.unit}` : "—" }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 水道水と比較ボタン -->
      <NuxtLink
        to="/compare"
        class="inline-flex items-center px-5 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
      >
        水道水と比較する →
      </NuxtLink>
    </template>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "default" });

const route = useRoute();
const config = useRuntimeConfig();

const { data: water } = await useAsyncData(`commercial-${route.params.id}`, () =>
  $fetch<Record<string, any>>(
    `${config.public.apiBase}/api/v1/commercial-water/${route.params.id}`
  ).catch(() => null)
);

const waterTypeJa = computed(
  () =>
    ({ soft: "軟水", medium: "中硬水", hard: "硬水", very_hard: "超硬水" }[
      water.value?.water_type as string
    ] ?? "")
);

const countryLabel = computed(
  () => ({ jpn: "日本", fra: "フランス", usa: "アメリカ" }[water.value?.country_code ?? ""] ?? water.value?.country_code ?? ""
  )
);

const summaryCards = computed(() => [
  { label: "硬度",   value: water.value?.hardness,   unit: "mg/L" },
  { label: "pH",     value: water.value?.ph,         unit: "" },
  { label: "TDS",    value: water.value?.tds,        unit: "mg/L" },
  { label: "コーヒー適性", value: `${water.value?.coffee_score ?? "—"}/5`, unit: "" },
]);

const detailRows = computed(() => [
  { label: "硬度",               value: water.value?.hardness,   unit: "mg/L" },
  { label: "pH",                 value: water.value?.ph,         unit: "" },
  { label: "カルシウム (Ca)",    value: water.value?.calcium,    unit: "mg/L" },
  { label: "マグネシウム (Mg)", value: water.value?.magnesium,  unit: "mg/L" },
  { label: "ナトリウム (Na)",   value: water.value?.sodium,     unit: "mg/L" },
  { label: "TDS",                value: water.value?.tds,        unit: "mg/L" },
]);
</script>
