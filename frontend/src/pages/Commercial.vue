<script setup>
import { ref } from 'vue';
import { Factory, Store, Video } from 'lucide-vue-next';
import ImageProcessor from '../components/ImageProcessor.vue';

const demoRef = ref(null);

const cards = [
  {
    title: '工业热像检测',
    description:
      '在高温、烟雾和强电磁干扰环境下提升缺陷检测的鲁棒性，减少漏检与误报。',
    items: ['电力设备/管道红外巡检增强', '边缘推理毫秒级延迟', '与 SCADA/MES 系统对接'],
    icon: Factory,
  },
  {
    title: '智慧安防监控',
    description:
      '夜间、雨雾等低能见度场景下保持清晰热源画面，提升入侵检测与行为分析精度。',
    items: ['与 VMS/NVR 的 REST/RTSP 旁路集成', '可选隐私遮罩与水印', 'GPU/CPU 灵活切换'],
    icon: Video,
  },
  {
    title: '智慧零售热力分析',
    description:
      '商场、仓储环境下提升客流热力分析与货架监测的信噪比，降低补光成本。',
    items: ['与 BI/数据看板对接', '批量处理历史热像录像', '集成自助收银与盘点终端'],
    icon: Store,
  },
];

function scrollToDemo() {
  demoRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
</script>

<template>
  <main class="page">
    <div class="container">
      <section class="page-hero section">
        <span class="page-tag">应用场景 ·商业</span>
        <h1 class="page-title">为工业检测与智慧安防提供清晰的红外视觉能力</h1>
        <p class="page-subtitle">
          DEAL 通过动态对抗学习提升红外成像质量，适配边缘设备与云端部署，在低对比度与强噪声环境中保持稳定的物体识别与异常检测率。
        </p>
      </section>

      <section class="section">
        <div class="card-grid">
          <article v-for="card in cards" :key="card.title" class="card feature-card">
            <component :is="card.icon" :size="22" class="card-icon" />
            <h3 class="card-title">{{ card.title }}</h3>
            <p class="card-desc">{{ card.description }}</p>
            <ul class="card-list">
              <li v-for="item in card.items" :key="item">{{ item }}</li>
            </ul>
          </article>
        </div>
      </section>

      <section class="section">
        <div class="cta card">
          <div>
            <h3>概念验证与集成</h3>
            <p>在本页验证红外增强效果，或咨询 SDK/API 部署方案。</p>
          </div>
          <div class="cta-actions">
            <button class="btn btn-primary btn-md" type="button" @click="scrollToDemo">
              下滑演示
            </button>
            <a class="btn btn-ghost btn-md" href="mailto:contact@deal.ai">预约技术交流</a>
          </div>
        </div>
      </section>

      <section ref="demoRef" class="section">
        <ImageProcessor />
      </section>
    </div>
  </main>
</template>

<style scoped>
.page {
  padding-bottom: 80px;
}

.page-hero {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-tag {
  font-size: 14px;
  font-weight: 600;
  color: var(--brand);
}

.page-title {
  font-size: clamp(28px, 3.6vw, 36px);
  font-weight: 700;
  margin: 0;
}

.page-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  max-width: 720px;
  margin: 0;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.feature-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-icon {
  color: var(--brand);
}

.card-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.card-desc {
  margin: 0;
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.card-list {
  margin: 0;
  padding-left: 18px;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.cta {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.cta h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.cta p {
  margin: 4px 0 0;
  font-size: 15px;
  color: var(--text-secondary);
}

.cta-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
