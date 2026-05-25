<script setup>
import { shallowRef } from 'vue';

const faqs = [
  {
    question: 'DEAL 与传统红外增强方法有何不同？',
    answer:
      'DEAL 通过极小极大优化动态模拟热成像退化，将退化因素建模为对抗攻击，仅需 50 张清晰图像即可训练。相比之下，传统方法通常需要大量成对数据，且难以覆盖真实场景中的复杂退化分布。',
  },
  {
    question: '可以离线运行吗？',
    answer:
      '支持。将推理端部署为本地 Flask 服务或 ONNX 边缘推理，前端仅负责交互与可视化。预训练权重可下载后离线使用。',
  },
  {
    question: '支持哪些退化类型？',
    answer:
      '目前支持条纹噪声去除、超分辨率重建（×4）、混合复合退化恢复。动态对抗策略可以泛化到训练时未见过的退化模式。',
  },
  {
    question: '数据是否安全？',
    answer:
      '前端不持久化用户图像。可选择本地部署，图像数据完全不出域。支持访问控制与日志审计。',
  },
];

const activeIndex = shallowRef(null);

function toggle(index) {
  activeIndex.value = activeIndex.value === index ? null : index;
}
</script>

<template>
  <section class="section">
    <div class="faq">
      <div
        v-for="(item, index) in faqs"
        :key="item.question"
        class="faq-item"
        :class="{ open: activeIndex === index }"
      >
        <button class="faq-question" type="button" @click="toggle(index)">
          <span class="faq-arrow">▸</span>
          <span>{{ item.question }}</span>
        </button>
        <div class="faq-answer">
          {{ item.answer }}
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.faq-item {
  border-bottom: 1px solid var(--border-light);
}

.faq-question {
  width: 100%;
  padding: 20px 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  background: transparent;
  border: none;
  color: var(--text-primary);
  text-align: left;
}

.faq-question:hover {
  color: var(--brand);
}

.faq-arrow {
  font-size: 12px;
  color: var(--text-tertiary);
  transition: transform 250ms ease;
}

.faq-item.open .faq-arrow {
  transform: rotate(90deg);
  color: var(--brand);
}

.faq-item.open .faq-question {
  color: var(--brand);
}

.faq-answer {
  padding: 0 4px 20px 28px;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.6;
  max-height: 0;
  overflow: hidden;
  transition: max-height 250ms ease;
}

.faq-item.open .faq-answer {
  max-height: 200px;
}
</style>
