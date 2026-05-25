<script setup>
import { shallowRef } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { Menu, Moon, Sun, X } from 'lucide-vue-next';
import { useTheme } from './composables/useTheme';

const menuOpen = shallowRef(false);
const { theme, toggleTheme } = useTheme();

function closeMenu() {
  menuOpen.value = false;
}
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="container header-inner">
        <RouterLink class="logo" to="/" @click="closeMenu">
          DEAL
          <span class="logo-dot"></span>
        </RouterLink>
        <nav class="nav-links">
          <RouterLink class="nav-link" to="/">首页</RouterLink>
          <RouterLink class="nav-link" to="/personal">个人</RouterLink>
          <RouterLink class="nav-link" to="/commercial">商业</RouterLink>
          <RouterLink class="nav-link" to="/national">国家</RouterLink>
        </nav>
        <div class="nav-actions">
          <button class="btn btn-ghost btn-sm" type="button" @click="toggleTheme">
            <Sun v-if="theme === 'dark'" :size="16" />
            <Moon v-else :size="16" />
          </button>
          <button class="btn btn-ghost btn-sm menu-button" type="button" @click="menuOpen = true">
            <Menu :size="18" />
          </button>
        </div>
      </div>
    </header>

    <main class="app-main">
      <Transition name="page-fade" mode="out-in">
        <RouterView />
      </Transition>
    </main>

    <footer class="app-footer">
      <div class="container footer-grid">
        <div class="footer-brand">
          <div class="logo">DEAL</div>
          <p>数据高效对抗学习红外图像增强 ·CVPR 2025</p>
        </div>
        <div class="footer-col">
          <div class="footer-title">产品</div>
          <RouterLink class="footer-link" to="/">首页</RouterLink>
          <RouterLink class="footer-link" to="/personal">个人应用</RouterLink>
          <RouterLink class="footer-link" to="/commercial">商业应用</RouterLink>
          <RouterLink class="footer-link" to="/national">国家应用</RouterLink>
        </div>
        <div class="footer-col">
          <div class="footer-title">资源</div>
          <a class="footer-link" href="https://github.com/LiuZhu-CV/DEAL" target="_blank" rel="noreferrer">
            论文(CVPR 2025)
          </a>
          <a class="footer-link" href="https://github.com/LiuZhu-CV/DEAL" target="_blank" rel="noreferrer">
            官方仓库
          </a>
          <a class="footer-link" href="https://github.com/LiuZhu-CV/DEAL" target="_blank" rel="noreferrer">
            Web Demo
          </a>
          <a class="footer-link" href="https://github.com/LiuZhu-CV/DEAL" target="_blank" rel="noreferrer">
            API 文档
          </a>
        </div>
        <div class="footer-col">
          <div class="footer-title">联系</div>
          <a class="footer-link" href="https://github.com/LiuZhu-CV/DEAL/issues" target="_blank" rel="noreferrer">
            GitHub Issues
          </a>
          <a class="footer-link" href="https://www.dlut.edu.cn" target="_blank" rel="noreferrer">
            大连理工大学
          </a>
        </div>
      </div>
      <div class="container footer-bottom">
        © 2026 DEAL Web Demo. 原始算法与论文版权归作者所有。本仓库为社区部署与演示分支。
      </div>
    </footer>

    <div v-if="menuOpen" class="mobile-overlay">
      <div class="mobile-header">
        <div class="logo">DEAL<span class="logo-dot"></span></div>
        <button class="btn btn-ghost btn-sm" type="button" @click="closeMenu">
          <X :size="18" />
        </button>
      </div>
      <div class="mobile-links">
        <RouterLink class="mobile-link" to="/" @click="closeMenu">首页</RouterLink>
        <RouterLink class="mobile-link" to="/personal" @click="closeMenu">个人</RouterLink>
        <RouterLink class="mobile-link" to="/commercial" @click="closeMenu">商业</RouterLink>
        <RouterLink class="mobile-link" to="/national" @click="closeMenu">国家</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: var(--bg);
  color: var(--text-primary);
}

.app-header {
  height: 56px;
  position: relative;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
}

.header-inner {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.logo-dot {
  width: 6px;
  height: 6px;
  background: var(--brand);
  border-radius: 999px;
  display: inline-block;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  padding: 6px 4px;
  border-bottom: 2px solid transparent;
}

.nav-link:hover {
  color: var(--text-primary);
}

.nav-link.router-link-exact-active {
  color: var(--brand);
  border-bottom-color: var(--brand);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.menu-button {
  display: none;
}

.app-footer {
  margin-top: 80px;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border);
  padding: 64px 0 32px;
}

.app-main {
  min-height: calc(100vh - 56px);
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 32px;
}

.footer-brand p {
  color: var(--text-secondary);
  font-size: 14px;
  max-width: 280px;
  margin: 12px 0 0;
}

.footer-title {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-tertiary);
  letter-spacing: 0.08em;
  margin-bottom: 12px;
}

.footer-link {
  display: block;
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 10px;
}

.footer-link:hover {
  color: var(--text-primary);
}

.footer-bottom {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  color: var(--text-tertiary);
}

.mobile-overlay {
  position: fixed;
  inset: 0;
  background: var(--bg);
  z-index: 100;
  display: flex;
  flex-direction: column;
  padding: 24px 20px;
}

.mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mobile-links {
  margin-top: 64px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  text-align: center;
}

.mobile-link {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .menu-button {
    display: inline-flex;
  }

  .footer-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
