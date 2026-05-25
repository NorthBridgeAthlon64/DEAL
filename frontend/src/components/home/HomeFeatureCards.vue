<script setup>
import { Cpu, GitBranch, Zap } from 'lucide-vue-next';

const cards = [
  {
    title: '核心架构',
    description:
      '提出动态对抗求解策略（DAS），通过极小极大优化将热成像退化构造为对抗过程，在训练中动态生成多样化的退化数据分布，仅用极少数据即可学习稳健的增强映射。',
    items: ['动态退化生成与对抗训练一体化', '脉冲引导分离模块捕获退化锐利特征', '尺度变换模块增强多尺度表达能力'],
    icon: Cpu,
  },
  {
    title: '网络设计',
    description:
      '双交互网络融合脉冲神经网络（SNN）与尺度变换（STM），以紧凑的模型参数实现高效特征表示。脉冲信号强度精准定位退化区域，尺度变换提供全局上下文。',
    items: ['脉冲引导分离模块（SSM）', '尺度变换模块（STM）', '紧凑参数，适合边缘部署'],
    icon: GitBranch,
  },
  {
    title: '应用能力',
    description:
      '在多种单一和复合退化场景下均表现优异，包括条纹噪声去除、超分辨率重建、混合退化恢复。推理延迟低，可部署于边缘设备和云端。',
    items: ['条纹噪声 / 超分辨率 / 复合退化', '仅需单张红外图像输入', 'Flask API + ONNX 可扩展部署'],
    icon: Zap,
  },
];
</script>

<template>
  <section class="section">
    <div class="feature-grid">
      <article v-for="card in cards" :key="card.title" class="card feature-card">
        <component :is="card.icon" class="feature-icon" :size="20" />
        <h3 class="feature-title">{{ card.title }}</h3>
        <p class="feature-desc">{{ card.description }}</p>
        <ul class="feature-list">
          <li v-for="item in card.items" :key="item">{{ item }}</li>
        </ul>
      </article>
    </div>
  </section>
</template>

<style scoped>
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.feature-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-icon {
  color: var(--brand);
}

.feature-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.feature-desc {
  margin: 0;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.feature-list {
  margin: 0;
  padding-left: 18px;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

@media (max-width: 1024px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
