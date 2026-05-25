<script setup>
import { ref } from 'vue';
import { Plane, Radar, ShieldCheck } from 'lucide-vue-next';
import ImageProcessor from '../components/ImageProcessor.vue';

const demoRef = ref(null);

const cards = [
  {
    title: '边海防红外巡察',
    description:
      '增强远距离红外探测画面的清晰度，提升微小热源目标的检测与跟踪稳定性。',
    items: ['雾霾雨雪夜间场景鲁棒', '与雷达/AIS 数据联动', '前哨站或舰载边缘部署'],
    icon: Radar,
  },
  {
    title: '应急救援热成像',
    description:
      '火场、塌方、雪崩等极端环境中提升搜救红外可见度，辅助被困人员定位与路径规划。',
    items: ['单兵端/无人机载红外增强', '低带宽高效编解码传输', '叠加热力分割与深度信息'],
    icon: ShieldCheck,
  },
  {
    title: '无人系统昼夜侦察',
    description:
      '面向无人机、无人车昼夜红外侦察与导航，提升 SLAM 和检测算法在遮挡烟尘下的可靠度。',
    items: ['轻量化模型支持 ARM/GPU', '时序稳定减少帧间抖动', '与指控系统对接'],
    icon: Plane,
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
        <span class="page-tag">应用场景 ·国家/军事</span>
        <h1 class="page-title">全天候、全谱段的红外态势感知与任务保障</h1>
        <p class="page-subtitle">
          DEAL 在极端天气、复杂电磁与低照条件下增强红外图像质量，面向边海防巡察、应急救援和战术侦察提供可靠的视觉能力。
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
            <h3>验证与适配</h3>
            <p>本页即可验证红外增强效果，或联系团队获取离线包与加固版部署方案。</p>
          </div>
          <div class="cta-actions">
            <button class="btn btn-primary btn-md" type="button" @click="scrollToDemo">
              下滑演示
            </button>
            <a class="btn btn-ghost btn-md" href="mailto:contact@deal.ai">需求沟通</a>
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
