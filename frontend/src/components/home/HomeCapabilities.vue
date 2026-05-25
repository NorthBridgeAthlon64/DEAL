<script setup>
import { Layers, Maximize2, Shield, Thermometer } from 'lucide-vue-next';

const items = [
  {
    title: '热成像增强',
    description: '消除红外图像中的条纹噪声、非均匀性和热晕，恢复真实的热辐射分布细节。',
    icon: Thermometer,
  },
  {
    title: '超分辨率重建',
    description: '提升低分辨率红外图像的空间分辨率，为远距离目标检测提供更清晰的输入。',
    icon: Maximize2,
  },
  {
    title: '复合退化恢复',
    description: '同时处理多种退化因素的叠加效应，在真实复杂场景下保持稳健的增强效果。',
    icon: Layers,
  },
  {
    title: '数据高效训练',
    description: '仅需 50 张清晰图像即可完成模型训练，大幅降低数据采集成本与标注负担。',
    icon: Shield,
  },
];
</script>

<template>
  <section class="section">
    <div class="capability-grid">
      <div v-for="item in items" :key="item.title" class="card capability-card">
        <component :is="item.icon" :size="24" class="capability-icon" />
        <h3 class="capability-title">{{ item.title }}</h3>
        <p class="capability-desc">{{ item.description }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.capability-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.capability-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.capability-icon {
  color: var(--brand);
}

.capability-title {
  margin: 8px 0 0;
  font-size: 16px;
  font-weight: 600;
}

.capability-desc {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

@media (max-width: 1024px) {
  .capability-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .capability-grid {
    grid-template-columns: 1fr;
  }
}
</style>
