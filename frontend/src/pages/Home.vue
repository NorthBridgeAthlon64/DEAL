<script setup>
import HomeCapabilities from '../components/home/HomeCapabilities.vue';
import HomeCTA from '../components/home/HomeCTA.vue';
import HomeFaq from '../components/home/HomeFaq.vue';
import HomeFeatureCards from '../components/home/HomeFeatureCards.vue';
import HomeHero from '../components/home/HomeHero.vue';
import HomeMetrics from '../components/home/HomeMetrics.vue';
import HomeProcess from '../components/home/HomeProcess.vue';
import HomeTimeline from '../components/home/HomeTimeline.vue';
</script>

<template>
  <main class="home">
    <div class="container">
      <HomeHero />
      <HomeMetrics />
      <HomeFeatureCards />
      <HomeCTA />
      <HomeCapabilities />
      <HomeProcess />
      <HomeTimeline />
      <HomeFaq />
    </div>
  </main>
</template>

<style scoped>
.home {
  padding-bottom: 80px;
}
</style>
