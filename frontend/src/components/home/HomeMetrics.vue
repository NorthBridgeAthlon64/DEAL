<script setup>
const metrics = [
  { value: '仅需 50 张', label: '训练图像数量' },
  { value: '动态对抗', label: '退化模拟策略' },
  { value: '双交互网络', label: '脉冲+尺度变换' },
  { value: '毫秒级', label: '单张推理延迟' },
];
</script>

<template>
  <section class="section">
    <div class="metrics-grid">
      <div v-for="metric in metrics" :key="metric.label" class="metrics-card">
        <div class="metrics-value">{{ metric.value }}</div>
        <div class="metrics-label">{{ metric.label }}</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  padding: 40px 0;
}

.metrics-card {
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 24px;
  text-align: center;
}

.metrics-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.metrics-label {
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  color: var(--text-tertiary);
  letter-spacing: 0.05em;
  margin-top: 6px;
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
