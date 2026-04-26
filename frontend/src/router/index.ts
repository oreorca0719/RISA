import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
    },
    {
      path: '/student',
      name: 'student-home',
      component: () => import('@/views/StudentHomeView.vue'),
    },
    {
      path: '/student/diagnosis',
      name: 'diagnosis',
      component: () => import('@/views/DiagnosisView.vue'),
    },
    {
      path: '/student/result',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
    },
  ],
})

export default router
