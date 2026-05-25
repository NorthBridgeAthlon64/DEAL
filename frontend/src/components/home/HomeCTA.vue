<script setup></script>

<template>
  <section class="section">
    <div class="cta card">
      <div class="cta-text">
        <h3>选择应用场景</h3>
        <p>针对个人、商业、国家三类场景，在对应页面直接完成红外图像增强演示。</p>
      </div>
      <div class="cta-actions">
        <RouterLink class="btn btn-secondary btn-md" to="/personal">个人</RouterLink>
        <RouterLink class="btn btn-secondary btn-md" to="/commercial">商业</RouterLink>
        <RouterLink class="btn btn-secondary btn-md" to="/national">国家</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
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

.cta-text h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.cta-text p {
  margin: 4px 0 0;
  font-size: 15px;
  color: var(--text-secondary);
}

.cta-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
</style>
