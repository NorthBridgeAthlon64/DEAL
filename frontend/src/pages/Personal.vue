<script setup>
import { ref } from 'vue';
import { Bike, Camera, Home } from 'lucide-vue-next';
import ImageProcessor from '../components/ImageProcessor.vue';

const demoRef = ref(null);

const cards = [
  {
    title: '手持热像仪增强',
    description:
      '一键优化手机热成像插件或手持热像仪的图像，去除条纹噪声与非均匀性，提升测温清晰度。',
    items: ['实时条纹噪声去除', '非均匀性校正', '批量处理户外拍摄素材'],
    icon: Camera,
  },
  {
    title: '户外夜视辅助',
    description:
      '骑行、徒步、夜跑场景下，增强穿戴式红外设备的画面可见度，安全导航更清晰。',
    items: ['头戴红外设备增强', '夜间低对比度场景恢复', '离线模式保护隐私'],
    icon: Bike,
  },
  {
    title: '家庭安防热成像',
    description:
      '家用红外摄像头暗角与噪声增强，减少误报，保留热源细节。',
    items: ['热源异常检测更稳定', '与 NAS/本地网关集成', '低功耗边缘推理'],
    icon: Home,
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
        <span class="page-tag">应用场景 ·个人</span>
        <h1 class="page-title">为摄影爱好者与户外玩家提供的红外增强工具</h1>
        <p class="page-subtitle">
          即开即用的红外图像增强体验，快速改善消费级热像仪的低信噪比画面，还原清晰的热辐射细节。
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
            <h3>快速上手</h3>
            <p>在下方的演示区上传红外图像，或将 DEAL 算法嵌入本地工具链。</p>
          </div>
          <button class="btn btn-primary btn-md" type="button" @click="scrollToDemo">
            立即演示
          </button>
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
