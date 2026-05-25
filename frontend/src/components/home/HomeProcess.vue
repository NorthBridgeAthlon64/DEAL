<script setup>
const steps = [
  {
    title: '输入红外图像',
    description: '上传单张红外图像，支持常见格式，最大 15MB',
  },
  {
    title: '动态退化分析',
    description: 'DAS 模块分析输入图像的退化类型与强度分布',
  },
  {
    title: '脉冲特征提取',
    description: 'SSM 模块以脉冲信号捕获退化区域的锐利特征',
  },
  {
    title: '对抗增强重建',
    description: '双交互网络融合多尺度特征，对抗式恢复清晰红外画面',
  },
  {
    title: '输出增强结果',
    description: '生成高信噪比红外图像，支持下载与下游任务接入',
  },
];

const completedSteps = new Set([0, 1]);
</script>

<template>
  <section class="section">
    <div class="process">
      <div class="process-bar">
        <div v-for="(step, index) in steps" :key="step.title" class="process-node">
          <div
            class="process-circle"
            :class="{ complete: completedSteps.has(index) }"
          >
            {{ String(index + 1).padStart(2, '0') }}
          </div>
          <div class="process-line" :class="{ complete: completedSteps.has(index) }"></div>
        </div>
      </div>
      <div class="process-details">
        <div v-for="(step, index) in steps" :key="step.title" class="process-item">
          <div class="process-title">
            {{ String(index + 1).padStart(2, '0') }} {{ step.title }}
          </div>
          <div class="process-desc">{{ step.description }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.process {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.process-bar {
  display: flex;
  align-items: center;
}

.process-node {
  display: flex;
  align-items: center;
  flex: 1;
}

.process-circle {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  background: transparent;
}

.process-circle.complete {
  border-color: var(--brand);
  color: var(--brand);
  background: var(--brand-soft);
}

.process-line {
  height: 2px;
  flex: 1;
  background: var(--border);
  margin: 0 12px;
  margin-top: 15px;
}

.process-line.complete {
  background: var(--brand);
}

.process-node:last-child .process-line {
  display: none;
}

.process-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.process-title {
  font-size: 15px;
  font-weight: 600;
  margin-top: 10px;
}

.process-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .process-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .process-node {
    width: 100%;
  }

  .process-line {
    display: none;
  }
}
</style>
