<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
    <div class="px-6 py-4 border-b border-gray-100">
      <h2 class="text-lg font-semibold text-gray-900">詳細水質データ</h2>
    </div>
    <table class="w-full text-sm">
      <tbody class="divide-y divide-gray-50">
        <tr v-for="row in rows" :key="row.label" class="hover:bg-gray-50">
          <td class="px-6 py-3 text-gray-500 w-48">{{ row.label }}</td>
          <td class="px-6 py-3 font-medium text-gray-900">
            {{ row.value != null ? `${row.value}${row.unit ? " " + row.unit : ""}` : "—" }}
          </td>
        </tr>
        <tr class="hover:bg-gray-50">
          <td class="px-6 py-3 text-gray-500">データ信頼度</td>
          <td class="px-6 py-3">
            <span class="px-2 py-0.5 rounded text-xs font-medium" :class="confidenceClass">
              {{ confidenceLabel }}
            </span>
          </td>
        </tr>
        <tr v-if="quality?.measured_at" class="hover:bg-gray-50">
          <td class="px-6 py-3 text-gray-500">測定日</td>
          <td class="px-6 py-3 text-gray-600">{{ quality.measured_at.slice(0, 10) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
interface Quality {
  hardness?: number | null;
  ph?: number | null;
  calcium?: number | null;
  magnesium?: number | null;
  sodium?: number | null;
  tds?: number | null;
  chlorine?: number | null;
  drinkable?: boolean;
  boil_recommended?: boolean;
  confidence_score?: string;
  measured_at?: string | null;
}

const props = defineProps<{ quality: Quality | null | undefined }>();

const rows = computed(() => [
  { label: "硬度",               value: props.quality?.hardness,   unit: "mg/L" },
  { label: "pH",                 value: props.quality?.ph,         unit: "" },
  { label: "カルシウム (Ca)",    value: props.quality?.calcium,    unit: "mg/L" },
  { label: "マグネシウム (Mg)", value: props.quality?.magnesium,  unit: "mg/L" },
  { label: "ナトリウム (Na)",   value: props.quality?.sodium,     unit: "mg/L" },
  { label: "TDS",                value: props.quality?.tds,        unit: "mg/L" },
  { label: "残留塩素",           value: props.quality?.chlorine,   unit: "mg/L" },
]);

const confidenceClass = computed(() => ({
  "bg-green-100 text-green-800":  props.quality?.confidence_score === "official",
  "bg-yellow-100 text-yellow-800": props.quality?.confidence_score === "community",
  "bg-gray-100 text-gray-500":    !props.quality?.confidence_score || props.quality.confidence_score === "estimated",
}));

const confidenceLabel = computed(
  () =>
    ({ official: "公式データ", community: "コミュニティ", estimated: "推定値" }[
      props.quality?.confidence_score ?? ""
    ] ?? "不明")
);
</script>
