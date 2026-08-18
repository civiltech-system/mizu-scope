<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- 404 -->
    <div v-if="!region" class="text-center py-20">
      <p class="text-gray-500 mb-4">地域情報が見つかりませんでした。</p>
      <NuxtLink to="/" class="text-blue-600 hover:underline">地図に戻る</NuxtLink>
    </div>

    <template v-else>
      <Head>
        <Title>{{ pageTitle }}</Title>
        <Meta name="description" :content="pageDescription" />
        <Meta property="og:title" :content="pageTitle" />
        <Meta property="og:description" :content="pageDescription" />
      </Head>

      <!-- パンくず -->
      <nav class="flex items-center gap-1 text-sm text-gray-400 mb-4">
        <NuxtLink to="/" class="hover:text-blue-600">地図</NuxtLink>
        <span>/</span>
        <span>{{ region.prefecture }}</span>
        <span>/</span>
        <span class="text-gray-700">{{ region.city }}</span>
      </nav>

      <!-- ヘッダー -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-1">
          {{ region.prefecture }}{{ region.city }}の水道水
        </h1>
        <p class="text-gray-500 text-sm">
          水源: {{ region.water_source }} | 管理: {{ region.utility_name }}
        </p>
      </div>

      <!-- サマリーカード -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <SummaryCard label="硬度" :value="region.quality?.hardness" unit="mg/L">
          <HardnessBadge :water-type="region.water_type" class="mt-2" />
        </SummaryCard>
        <SummaryCard label="pH" :value="region.quality?.ph" />
        <SummaryCard label="TDS" :value="region.quality?.tds" unit="mg/L" />
        <div class="bg-white rounded-xl shadow-sm p-4 text-center border border-gray-100">
          <p class="text-xs text-gray-500 mb-2">飲用</p>
          <DrinkableBadge :drinkable="region.quality?.drinkable" />
        </div>
      </div>

      <!-- コーヒー適性 -->
      <CoffeeScore :score="region.coffee_score" class="mb-8" />

      <!-- 詳細水質テーブル -->
      <WaterQualityTable :quality="region.quality" class="mb-8" />

      <!-- 近い市販水 -->
      <div v-if="matchedWaters?.length" class="mb-8">
        <h2 class="text-xl font-bold text-gray-900 mb-2">近い水質の市販水</h2>
        <p class="text-sm text-gray-500 mb-4">
          硬度が近いミネラルウォーターです。コーヒーの代替水として参考にしてください。
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <NuxtLink
            v-for="water in matchedWaters"
            :key="water.id"
            :to="`/bottled-water/${water.id}`"
            class="bg-white rounded-xl shadow-sm p-4 border border-gray-100 hover:border-blue-300 transition-colors block"
          >
            <p class="font-semibold text-gray-800">{{ water.name }}</p>
            <p class="text-xs text-gray-400 mb-2">{{ water.brand }}</p>
            <p class="text-sm text-gray-600">硬度: <span class="font-medium">{{ water.hardness }} mg/L</span></p>
            <p class="text-sm text-gray-600">pH: <span class="font-medium">{{ water.ph }}</span></p>
            <HardnessBadge :water-type="water.water_type" class="mt-2" />
          </NuxtLink>
        </div>
        <NuxtLink
          to="/compare"
          class="mt-4 inline-flex items-center text-sm text-blue-600 hover:underline"
        >
          比較ページで詳しく比べる →
        </NuxtLink>
      </div>

    </template>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, h } from "vue";

definePageMeta({ layout: "default" });

const route = useRoute();
const config = useRuntimeConfig();

const slug = `${route.params.country}/${route.params.prefecture}/${route.params.city}`;

const { data: region } = await useAsyncData(`region-${slug}`, () =>
  $fetch<Record<string, any>>(
    `${config.public.apiBase}/api/v1/regions/slug/${slug}`
  ).catch(() => null)
);

const { data: matchedWaters } = await useAsyncData(
  `match-${region.value?.id}`,
  () => {
    if (!region.value?.id) return Promise.resolve(null);
    return $fetch<Record<string, any>[]>(
      `${config.public.apiBase}/api/v1/commercial-water/match/${region.value.id}`
    ).catch(() => null);
  }
);

const regionName = computed(
  () => `${region.value?.prefecture ?? ""}${region.value?.city ?? ""}`.trim()
);

const waterTypeJa = computed(() =>
  ({ soft: "軟水", medium: "中硬水", hard: "硬水", very_hard: "超硬水" }[
    region.value?.water_type as string
  ] ?? "水道水")
);

const pageTitle = computed(() => {
  if (!region.value) return "地域情報 | MizuMap";
  const h = region.value.quality?.hardness;
  return `${regionName.value}の水道水 硬度${h ?? "?"}mg/L ${waterTypeJa.value}`;
});

const pageDescription = computed(() => {
  if (!region.value?.quality) return `${regionName.value}の水道水情報`;
  const q = region.value.quality;
  return `${regionName.value}の水道水は硬度${q.hardness}mg/L・pH${q.ph}の${waterTypeJa.value}です。飲用${q.drinkable ? "可" : "要確認"}。コーヒー適性・詳細ミネラル情報を確認できます。`;
});

useHead({
  script: computed(() => {
    if (!region.value) return [];
    return [
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Place",
          name: `${regionName.value}の水道水`,
          description: pageDescription.value,
          geo: region.value.lat
            ? { "@type": "GeoCoordinates", latitude: region.value.lat, longitude: region.value.lng }
            : undefined,
        }),
      },
    ];
  }),
});

// ─── Inline sub-component ────────────────────────────────────────────────────
const SummaryCard = defineComponent({
  props: { label: String, value: [Number, null], unit: String },
  setup(props, { slots }) {
    return () =>
      h("div", { class: "bg-white rounded-xl shadow-sm p-4 text-center border border-gray-100" }, [
        h("p", { class: "text-xs text-gray-500 mb-1" }, props.label),
        h(
          "p",
          { class: "text-2xl font-bold text-gray-900" },
          props.value != null ? String(props.value) : "—"
        ),
        props.unit ? h("p", { class: "text-xs text-gray-400" }, props.unit) : null,
        slots.default?.(),
      ]);
  },
});
</script>
