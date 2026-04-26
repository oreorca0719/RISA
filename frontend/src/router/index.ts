import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
    { path: '/register', name: 'register', component: () => import('@/views/RegisterView.vue') },
    { path: '/student', name: 'student-home', component: () => import('@/views/StudentHomeView.vue') },
    { path: '/student/diagnosis', name: 'diagnosis', component: () => import('@/views/DiagnosisView.vue') },
    { path: '/student/result', name: 'result', component: () => import('@/views/ResultView.vue') },
    { path: '/admin', name: 'admin-dashboard', component: () => import('@/views/admin/AdminDashboardView.vue') },
    { path: '/admin/users', name: 'admin-users', component: () => import('@/views/admin/AdminUsersView.vue') },
    { path: '/admin/stats', name: 'admin-stats', component: () => import('@/views/admin/AdminStatsView.vue') },
    { path: '/admin/texts', name: 'admin-texts', component: () => import('@/views/admin/AdminTextsView.vue') },
    { path: '/admin/system', name: 'admin-system', component: () => import('@/views/admin/AdminSystemView.vue') },
  ],
})

export default router
