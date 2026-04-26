<template>
  <AdminLayout @logout="handleLogout">
    <template #title>시스템 모니터링</template>

    <div class="system-page">
      <!-- 서비스 상태 -->
      <div class="section">
        <h2 class="section-title">서비스 상태</h2>
        <div class="service-grid">
          <div class="service-card" v-for="svc in services" :key="svc.name">
            <div class="svc-header">
              <span class="svc-icon">{{ svc.icon }}</span>
              <span class="svc-name">{{ svc.name }}</span>
              <span class="svc-status" :class="svc.status">
                {{ svc.status === 'ok' ? '● 정상' : svc.status === 'warn' ? '● 확인 필요' : '● 오류' }}
              </span>
            </div>
            <div class="svc-detail">{{ svc.detail }}</div>
          </div>
        </div>
      </div>

      <!-- AWS 리소스 -->
      <div class="section">
        <h2 class="section-title">AWS 인프라</h2>
        <div class="infra-grid">
          <div class="infra-card" v-for="r in awsResources" :key="r.name">
            <div class="infra-icon">{{ r.icon }}</div>
            <div class="infra-info">
              <div class="infra-name">{{ r.name }}</div>
              <div class="infra-value">{{ r.value }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 에러 로그 -->
      <div class="section">
        <h2 class="section-title">에러 로그</h2>
        <div class="log-panel">
          <div class="log-empty">
            <span>🔧</span>
            <span>CloudWatch 로그 연동 준비 중입니다</span>
          </div>
        </div>
      </div>

      <!-- API 응답 시간 -->
      <div class="section">
        <h2 class="section-title">API 엔드포인트 상태</h2>
        <div class="endpoint-list">
          <div class="endpoint-row" v-for="ep in endpoints" :key="ep.path">
            <span class="method" :class="ep.method.toLowerCase()">{{ ep.method }}</span>
            <span class="path">{{ ep.path }}</span>
            <span class="ep-status">준비 중</span>
            <span class="latency">-ms</span>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/admin/AdminLayout.vue'

const router = useRouter()

const services = [
  { icon: '⚡', name: 'FastAPI 서버', status: 'warn', detail: 'ECS Fargate — 연동 확인 필요' },
  { icon: '🗄️', name: 'PostgreSQL RDS', status: 'warn', detail: 'db.t3.micro — 연결 대기 중' },
  { icon: '⚡', name: 'Redis Cache', status: 'warn', detail: 'ElastiCache — 설정 필요' },
  { icon: '🎤', name: 'Clova STT', status: 'warn', detail: 'API 키 미설정' },
  { icon: '🤖', name: 'Claude API', status: 'warn', detail: 'API 키 미설정' },
  { icon: '📦', name: 'S3 (Frontend)', status: 'ok', detail: 'risa-frontend-dev — 배포 완료' },
]

const awsResources = [
  { icon: '🌐', name: 'ALB URL', value: 'risa-backend-alb-1783502255.ap-northeast-1.elb.amazonaws.com' },
  { icon: '🏗️', name: 'ECS Cluster', value: 'risa-dev' },
  { icon: '📦', name: 'ECR Repository', value: 'risa-backend' },
  { icon: '🗃️', name: 'S3 Bucket', value: 'risa-frontend-dev' },
  { icon: '🌏', name: 'Region', value: 'ap-northeast-1 (Tokyo)' },
]

const endpoints = [
  { method: 'GET', path: '/api/health' },
  { method: 'POST', path: '/api/auth/login' },
  { method: 'POST', path: '/api/auth/register' },
  { method: 'POST', path: '/api/diagnosis/session' },
  { method: 'POST', path: '/api/diagnosis/fluency/oral' },
  { method: 'POST', path: '/api/diagnosis/comprehension' },
  { method: 'GET', path: '/api/diagnosis/result/{id}' },
]

function handleLogout() { router.push('/login') }
</script>

<style scoped>
.system-page { display: flex; flex-direction: column; gap: 1.5rem; }
.section { display: flex; flex-direction: column; gap: 0.8rem; }
.section-title { font-size: 0.95rem; font-weight: 800; color: #fff; }

.service-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; }
.service-card {
  background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 12px; padding: 1.2rem;
}
.svc-header { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem; }
.svc-icon { font-size: 1.2rem; }
.svc-name { flex: 1; font-size: 0.9rem; font-weight: 800; color: #ccc; }
.svc-status { font-size: 0.75rem; font-weight: 700; }
.svc-status.ok { color: #4ECDC4; }
.svc-status.warn { color: #FFE66D; }
.svc-status.error { color: #FF6B6B; }
.svc-detail { font-size: 0.78rem; color: #555; }

.infra-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.8rem; }
.infra-card {
  background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 12px; padding: 1rem 1.2rem;
  display: flex; align-items: center; gap: 0.8rem;
}
.infra-icon { font-size: 1.5rem; }
.infra-name { font-size: 0.75rem; color: #555; font-weight: 700; }
.infra-value { font-size: 0.85rem; color: #aaa; font-weight: 600; word-break: break-all; }

.log-panel {
  background: #0a0c12; border: 1px solid #2a2d3e; border-radius: 12px;
  padding: 2rem; font-family: monospace;
}
.log-empty {
  display: flex; align-items: center; gap: 0.7rem; justify-content: center;
  color: #444; font-size: 0.9rem;
}

.endpoint-list {
  background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 12px; overflow: hidden;
}
.endpoint-row {
  display: flex; align-items: center; gap: 1rem; padding: 0.8rem 1.2rem;
  border-bottom: 1px solid #1e2130; font-size: 0.85rem;
}
.endpoint-row:last-child { border-bottom: none; }
.method {
  font-weight: 800; font-size: 0.75rem; padding: 0.2rem 0.6rem;
  border-radius: 4px; min-width: 50px; text-align: center;
}
.method.get { background: rgba(78,205,196,0.15); color: #4ECDC4; }
.method.post { background: rgba(255,230,109,0.15); color: #f5d800; }
.path { flex: 1; color: #888; font-family: monospace; }
.ep-status { font-size: 0.75rem; color: #555; font-weight: 700; }
.latency { color: #555; font-size: 0.8rem; width: 50px; text-align: right; }
</style>
