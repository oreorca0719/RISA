import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // TODO: 진단 페이지
    // { path: '/diagnosis', name: 'diagnosis', component: () => import('@/views/DiagnosisView.vue') },
    // TODO: 결과 페이지
    // { path: '/result/:id', name: 'result', component: () => import('@/views/ResultView.vue') },
  ],
})

export default router
