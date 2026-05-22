<template>
  <div class="app-shell">
    <header class="app-header">
      <h1>DEAL 红外图像增强</h1>
      <p>Data-Efficient Adversarial Learning · CVPR 2025</p>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: linear-gradient(160deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #e2e8f0;
}

.app-header {
  text-align: center;
  padding: 2rem 1rem 1rem;
}

.app-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.app-header p {
  margin: 0.5rem 0 0;
  opacity: 0.75;
  font-size: 0.95rem;
}

main {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1rem 2rem;
}
</style>
