<template>
  <div class="bg-amber-50 rounded-xl border border-amber-100 p-6">
    <h2 class="text-lg font-semibold text-amber-900 mb-4">コーヒー適性</h2>
    <div class="flex items-center gap-4 mb-4">
      <div class="flex gap-1 text-2xl">
        <span
          v-for="i in 5"
          :key="i"
          :class="i <= (score ?? 0) ? 'opacity-100' : 'opacity-20'"
        >☕</span>
      </div>
      <div>
        <p class="text-lg font-bold text-amber-800">{{ scoreLabel }}</p>
        <p class="text-sm text-amber-600">{{ scoreDescription }}</p>
      </div>
    </div>
    <div class="grid grid-cols-2 gap-2 text-sm">
      <div v-for="use in coffeeUses" :key="use.label" class="flex items-center gap-2">
        <span :class="use.ok ? 'text-green-500' : 'text-gray-300'">
          {{ use.ok ? "✓" : "✗" }}
        </span>
        <span class="text-gray-600">{{ use.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ score: number | null | undefined }>();

const scoreLabel = computed(() => {
  const s = props.score ?? 0;
  if (s >= 5) return "最高";
  if (s >= 4) return "適している";
  if (s >= 3) return "普通";
  if (s >= 2) return "やや不向き";
  return "不向き";
});

const scoreDescription = computed(() => {
  const s = props.score ?? 0;
  if (s >= 4) return "コーヒー抽出に適した軟水〜中硬水です。";
  if (s >= 3) return "使用可能ですが、最適ではありません。";
  return "硬水のためコーヒーには不向きです。浄水器の使用を推奨します。";
});

const coffeeUses = computed(() => {
  const s = props.score ?? 0;
  return [
    { label: "ハンドドリップ",   ok: s >= 4 },
    { label: "浅煎り向き",       ok: s >= 4 },
    { label: "エスプレッソ",     ok: s >= 3 },
    { label: "深煎り向き",       ok: s >= 3 },
  ];
});
</script>
