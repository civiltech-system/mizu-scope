<template>
  <span
    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
    :class="badgeClass"
  >
    {{ label }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{ waterType: string | null | undefined }>();

const badgeClass = computed(() => ({
  "bg-blue-100 text-blue-800":   props.waterType === "soft",
  "bg-green-100 text-green-800": props.waterType === "medium",
  "bg-yellow-100 text-yellow-800": props.waterType === "hard",
  "bg-red-100 text-red-800":     props.waterType === "very_hard",
  "bg-gray-100 text-gray-500":   !props.waterType,
}));

const label = computed(
  () =>
    ({ soft: "軟水", medium: "中硬水", hard: "硬水", very_hard: "超硬水" }[
      props.waterType ?? ""
    ] ?? "不明")
);
</script>
