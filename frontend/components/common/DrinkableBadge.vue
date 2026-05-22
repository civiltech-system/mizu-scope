<template>
  <span
    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
    :class="cls"
  >
    {{ label }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{ drinkable: boolean | null | undefined }>();

const cls = computed(() =>
  props.drinkable === true
    ? "bg-green-100 text-green-800"
    : props.drinkable === false
    ? "bg-red-100 text-red-800"
    : "bg-gray-100 text-gray-500"
);

const label = computed(() =>
  props.drinkable === true ? "飲用可" : props.drinkable === false ? "要煮沸" : "不明"
);
</script>
