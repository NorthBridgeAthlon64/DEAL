import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../pages/Home.vue';
import Personal from '../pages/Personal.vue';
import Commercial from '../pages/Commercial.vue';
import National from '../pages/National.vue';

import Paper from '../pages/Paper.vue';

const routes = [
  { path: '/', name: 'home', component: Home, meta: { title: '首页 | DEAL' } },
  { path: '/paper', name: 'paper', component: Paper, meta: { title: '阅读论文 | DEAL' } },
  { path: '/personal', name: 'personal', component: Personal, meta: { title: '个人应用 | DEAL' } },
  {
    path: '/commercial',
    name: 'commercial',
    component: Commercial,
    meta: { title: '商业应用 | DEAL' },
  },
  { path: '/national', name: 'national', component: National, meta: { title: '国家应用 | DEAL' } },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

router.afterEach((to) => {
  document.title = to.meta.title || 'DEAL';
});

export default router;
