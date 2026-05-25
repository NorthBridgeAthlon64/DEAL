<script setup>
const milestones = [
  {
    title: 'Q1 ·公开演示',
    description: '发布 Web Demo，提供前端预览、预训练模型与在线推理体验。',
  },
  {
    title: 'Q2 ·轻量化与边缘版',
    description: '推出 ONNX/NCNN 推理版本，加入自动量化工具，支持 ARM 边缘设备。',
  },
  {
    title: 'Q3 ·多任务协同',
    description: '增强结果同步支持目标检测与场景分割，降低下游任务整体延迟。',
  },
  {
    title: 'Q4 ·自适应增强',
    description: '根据退化类型与强度自适应选择增强策略，无需人工调参。',
  },
];
</script>

<template>
  <section class="section">
    <div class="timeline">
      <div v-for="item in milestones" :key="item.title" class="timeline-item">
        <div class="timeline-marker"></div>
        <div class="timeline-content">
          <div class="timeline-title">{{ item.title }}</div>
          <div class="timeline-desc">{{ item.description }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.timeline {
  border-left: 2px solid var(--border);
  padding-left: 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.timeline-item {
  position: relative;
  display: flex;
  gap: 24px;
}

.timeline-marker {
  position: absolute;
  left: -33px;
  width: 18px;
  height: 18px;
  border-radius: 999px;
  border: 3px solid var(--border);
  background: var(--surface);
}

.timeline-title {
  font-size: 16px;
  font-weight: 600;
}

.timeline-desc {
  margin-top: 6px;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>
