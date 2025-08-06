<template>
  <div class="spinner" :class="size">
    <div class="spinner-circle"></div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  size: {
    type: String as () => 'small' | 'medium' | 'large',
    default: 'medium'
  }
})
</script>

<style scoped>
.spinner {
  display: inline-block;
  position: relative;
}

.spinner-circle {
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

.spinner.small .spinner-circle {
  width: 16px;
  height: 16px;
}

.spinner.medium .spinner-circle {
  width: 20px;
  height: 20px;
}

.spinner.large .spinner-circle {
  width: 24px;
  height: 24px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>