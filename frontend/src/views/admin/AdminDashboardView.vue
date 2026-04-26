<template>
  <AdminLayout @logout="handleLogout">
    <template #title>대시보드</template>

    <div class="dashboard">
      <!-- 요약 카드 -->
      <div class="stat-grid">
        <div class="stat-card" v-for="stat in stats" :key="stat.label">
          <div class="stat-icon">{{ stat.icon }}</div>
          <div class="stat-info">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
          <div class="stat-badge" :class="stat.color">{{ stat.change }}</div>
        </div>
      </div>

      <!-- 최근 활동 + 시스템 상태 -->
      <div class="bottom-grid">
        <div class="panel">
          <h2 class="panel-title">최근 진단 활동</h2>
          <div class="activity-list">
            <div class="activity-item coming-soon-item">
              <span>🔧</span>
              <span>진단 이력 데이터 연동 준비 중</span>
            </div>
          </div>
        </div>

        <div class="panel">
          <h2 class="panel-title">시스템 상태</h2>
          <div class="system-list">
            <div class="system-item" v-for="s in systemStatus" :key="s.name">
              <span class="system-name">{{ s.name }}</span>
              <span class="system-dot" :class="s.status === 'ok' ? 'dot-ok' : 'dot-warn'"></span>
              <span class="system-status" :class="s.status === 'ok' ? 'text-ok' : 'text-warn'">
                {{ s.status === 'ok' ? '정상' : '확인 필요' }}
              </span>
            </div>
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

const stats = [
  { icon: '👨‍🎓', label: '전체 학생 수', value: '-', change: '준비 중', color: 'badge-mint' },
  { icon: '📝', label: '총 진단 횟수', value: '-', change: '준비 중', color: 'badge-yellow' },
  { icon: '📚', label: '텍스트 풀', value: '-', change: '준비 중', color: 'badge-coral' },
  { icon: '🏫', label: '등록 교사 수', value: '-', change: '준비 중', color: 'badge-mint' },
]

const systemStatus = [
  { name: 'FastAPI 서버', status: 'warn' },
  { name: 'PostgreSQL RDS', status: 'warn' },
  { name: 'Redis Cache', status: 'warn' },
  { name: 'Clova STT API', status: 'warn' },
  { name: 'Claude API', status: 'warn' },
]

function handleLogout() { router.push('/login') }
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 1.5rem; }

.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.stat-card {
  background: #1a1d27;
  border: 1px solid #2a2d3e;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.stat-icon { font-size: 2rem; }
.stat-info { flex: 1; }
.stat-value { font-size: 1.8rem; font-weight: 900; color: #fff; }
.stat-label { font-size: 0.8rem; color: #666; font-weight: 600; margin-top: 0.1rem; }
.stat-badge {
  font-size: 0.75rem; font-weight: 700;
  padding: 0.3rem 0.7rem; border-radius: 99px;
}
.badge-mint { background: rgba(78,205,196,0.15); color: #4ECDC4; }
.badge-yellow { background: rgba(255,230,109,0.15); color: #f5d800; }
.badge-coral { background: rgba(255,107,107,0.15); color: #FF6B6B; }

.bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.panel {
  background: #1a1d27;
  border: 1px solid #2a2d3e;
  border-radius: 16px;
  padding: 1.5rem;
}
.panel-title { font-size: 0.95rem; font-weight: 800; color: #fff; margin-bottom: 1.2rem; }

.coming-soon-item {
  display: flex; align-items: center; gap: 0.7rem;
  color: #555; font-size: 0.9rem; padding: 1rem;
  background: #252836; border-radius: 10px;
}

.system-list { display: flex; flex-direction: column; gap: 0.8rem; }
.system-item {
  display: flex; align-items: center; gap: 0.7rem;
  padding: 0.7rem 1rem; background: #252836; border-radius: 10px;
}
.system-name { flex: 1; color: #aaa; font-size: 0.9rem; font-weight: 700; }
.system-dot { width: 8px; height: 8px; border-radius: 50%; }
.dot-ok { background: #4ECDC4; }
.dot-warn { background: #FFE66D; }
.text-ok { font-size: 0.8rem; font-weight: 700; color: #4ECDC4; }
.text-warn { font-size: 0.8rem; font-weight: 700; color: #FFE66D; }
</style>
