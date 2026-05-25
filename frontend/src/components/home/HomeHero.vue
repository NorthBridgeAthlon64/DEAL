<script setup>
const badges = ['动态对抗退化', '脉冲神经网络', '数据高效学习'];
</script>

<template>
  <section class="hero section">
    <div class="hero-inner">
      <span class="hero-tag">CVPR 2025</span>
      <h1 class="hero-title">
        <span>数据高效对抗学习</span>
        <span>高质量红外图像增强</span>
      </h1>
      <p class="hero-subtitle">
        仅需 50 张清晰红外图像即可完成训练。通过极小极大优化将热成像退化模拟为对抗攻击，动态捕获广泛退化分布，结合脉冲神经网络与尺度变换双交互网络，在极端条件下恢复清晰红外画面。
      </p>
      <div class="hero-badges">
        <span v-for="badge in badges" :key="badge" class="tag">{{ badge }}</span>
      </div>
      <div class="hero-actions">
        <RouterLink class="btn btn-primary btn-lg" to="/personal">开始使用</RouterLink>
        <a
          class="btn btn-secondary btn-lg"
          href="https://github.com/LiuZhu-CV/DEAL"
          target="_blank"
          rel="noreferrer"
        >
          阅读论文
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 120px 0 80px;
  text-align: center;
}

.hero-inner {
  max-width: 820px;
  margin: 0 auto;
}

.hero-tag {
  display: inline-block;
  background: var(--brand-soft);
  color: var(--brand);
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
  padding: 4px 12px;
  margin-bottom: 16px;
}

.hero-title {
  font-size: clamp(40px, 5vw, 64px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.08;
  color: var(--text-primary);
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  max-width: 640px;
  margin: 24px auto 0;
  line-height: 1.6;
}

.hero-badges {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
  flex-wrap: wrap;
}

.hero-actions {
  margin-top: 36px;
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: clamp(32px, 6vw, 48px);
  }
}
</style>
