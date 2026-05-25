<script setup>
import { RouterLink } from 'vue-router';
import { ArrowLeft, Download } from 'lucide-vue-next';
import { PAPER_PDF_PATH } from '../constants/links';
</script>

<template>
  <main class="paper-page">
    <div class="container paper-shell">
      <header class="paper-header">
        <RouterLink class="back-link" to="/">
          <ArrowLeft :size="16" />
          返回首页
        </RouterLink>
        <div class="paper-title-block">
          <span class="paper-tag">CVPR 2025</span>
          <h1>DEAL: Data-Efficient Adversarial Learning for High-Quality Infrared Imaging</h1>
          <p class="paper-meta">Zhu Liu, Zijun Wang, Jinyuan Liu, Fanqi Meng, Long Ma, Risheng Liu</p>
        </div>
        <a class="btn btn-secondary btn-sm download-link" :href="PAPER_PDF_PATH" download="DEAL_CVPR2025.pdf">
          <Download :size="16" />
          下载 PDF
        </a>
      </header>

      <section class="paper-viewer card">
        <iframe
          class="pdf-frame"
          :src="PAPER_PDF_PATH"
          title="DEAL CVPR 2025 Paper"
        />
      </section>
    </div>
  </main>
</template>

<style scoped>
.paper-page {
  padding: 32px 0 64px;
}

.paper-shell {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.paper-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
}

.back-link:hover {
  color: var(--brand);
}

.paper-title-block {
  flex: 1;
  min-width: 260px;
}

.paper-tag {
  display: inline-block;
  background: var(--brand-soft);
  color: var(--brand);
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
  padding: 4px 10px;
  margin-bottom: 10px;
}

.paper-title-block h1 {
  margin: 0;
  font-size: clamp(22px, 3vw, 30px);
  line-height: 1.25;
  color: var(--text-primary);
}

.paper-meta {
  margin: 10px 0 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.download-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.paper-viewer {
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg-secondary);
  min-height: calc(100vh - 220px);
}

.pdf-frame {
  width: 100%;
  height: calc(100vh - 220px);
  min-height: 720px;
  border: none;
  display: block;
  background: #fff;
}

@media (max-width: 768px) {
  .pdf-frame {
    min-height: 60vh;
    height: 70vh;
  }
}
</style>
