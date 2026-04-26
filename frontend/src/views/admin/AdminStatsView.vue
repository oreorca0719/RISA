<template>
  <AdminLayout @logout="handleLogout">
    <template #title>진단 통계</template>

    <div class="stats-page">
      <!-- 요약 수치 -->
      <div class="stat-row">
        <div class="mini-stat" v-for="s in summaryStats" :key="s.label">
          <span class="mini-icon">{{ s.icon }}</span>
          <div>
            <div class="mini-value">{{ s.value }}</div>
            <div class="mini-label">{{ s.label }}</div>
          </div>
        </div>
      </div>

      <!-- 차트 영역 -->
      <div class="charts-grid">
        <div class="chart-panel">
          <h2 class="panel-title">독자 유형 분포</h2>
          <div class="donut-placeholder">
            <div class="donut-ring"></div>
            <div class="donut-center">준비 중</div>
          </div>
          <div class="legend">
            <div class="legend-item"><span class="dot dot-mint"></span> 애독자</div>
            <div class="legend-item"><span class="dot dot-yellow"></span> 간헐적 독자</div>
            <div class="legend-item"><span class="dot dot-coral"></span> 비독자</div>
          </div>
        </div>

        <div class="chart-panel">
          <h2 class="panel-title">읽기 수준 분포</h2>
          <div class="bar-chart">
            <div class="bar-row" v-for="level in readingLevels" :key="level.name">
              <span class="bar-label">{{ level.name }}</span>
              <div class="bar-track">
                <div class="bar-fill" :style="{ width: level.pct, background: level.color }"></div>
              </div>
              <span class="bar-pct">{{ level.pct }}</span>
            </div>
          </div>
          <p class="coming-soon">🔧 실제 데이터 연동 준비 중</p>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-panel">
          <h2 class="panel-title">층위별 평균 점수</h2>
          <div class="score-bars">
            <div class="score-row" v-for="score in scoreData" :key="score.label">
              <span class="score-label">{{ score.label }}</span>
              <div class="score-track">
                <div class="score-fill" :style="{ width: score.pct, background: score.color }"></div>
              </div>
              <span class="score-val">-점</span>
            </div>
          </div>
          <p class="coming-soon">🔧 채점 데이터 연동 준비 중</p>
        </div>

        <div class="chart-panel">
          <h2 class="panel-title">학년별 진단 참여율</h2>
          <div class="grade-list">
            <div class="grade-item" v-for="g in grades" :key="g.name">
              <span class="grade-name">{{ g.name }}</span>
              <div class="grade-track">
                <div class="grade-fill"></div>
              </div>
              <span class="grade-count">-명</span>
            </div>
          </div>
          <p class="coming-soon">🔧 사용자 데이터 연동 준비 중</p>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/admin/AdminLayout.vue'

const router = useRouter()

const summaryStats = [
  { icon: '📝', label: '총 진단 횟수', value: '-' },
  { icon: '👨‍🎓', label: '참여 학생 수', value: '-' },
  { icon: '📈', label: '평균 읽기 수준', value: '-' },
  { icon: '✅', label: '완료율', value: '-' },
]

const readingLevels = [
  { name: 'Lv.1 기초', pct: '0%', color: '#FF6B6B' },
  { name: 'Lv.2 초급', pct: '0%', color: '#FFE66D' },
  { name: 'Lv.3 중급', pct: '0%', color: '#4ECDC4' },
  { name: 'Lv.4 고급', pct: '0%', color: '#38b2ab' },
  { name: 'Lv.5 최상', pct: '0%', color: '#2C3E50' },
]

const scoreData = [
  { label: '사실적 이해', pct: '0%', color: '#4ECDC4' },
  { label: '추론적 이해', pct: '0%', color: '#FFE66D' },
  { label: '비판적 이해', pct: '0%', color: '#FF6B6B' },
]

const grades = [
  '초등 1학년', '초등 2학년', '초등 3학년',
  '초등 4학년', '초등 5학년', '초등 6학년', '중등 1학년'
].map(name => ({ name }))

function handleLogout() { router.push('/login') }
</script>

<style scoped>
.stats-page { display: flex; flex-direction: column; gap: 1.2rem; }

.stat-row {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;
}
.mini-stat {
  background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 12px;
  padding: 1.2rem 1.5rem; display: flex; align-items: center; gap: 1rem;
}
.mini-icon { font-size: 1.8rem; }
.mini-value { font-size: 1.5rem; font-weight: 900; color: #fff; }
.mini-label { font-size: 0.75rem; color: #666; font-weight: 600; }

.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.chart-panel {
  background: #1a1d27; border: 1px solid #2a2d3e;
  border-radius: 16px; padding: 1.5rem;
  display: flex; flex-direction: column; gap: 1.2rem;
}
.panel-title { font-size: 0.95rem; font-weight: 800; color: #fff; }

/* 도넛 placeholder */
.donut-placeholder {
  display: flex; align-items: center; justify-content: center;
  height: 160px; position: relative;
}
.donut-ring {
  width: 120px; height: 120px; border-radius: 50%;
  border: 16px solid #252836; position: relative;
}
.donut-center {
  position: absolute; font-size: 0.8rem; color: #555; font-weight: 700;
}
.legend { display: flex; gap: 1rem; }
.legend-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; color: #888; font-weight: 700; }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot-mint { background: #4ECDC4; }
.dot-yellow { background: #FFE66D; }
.dot-coral { background: #FF6B6B; }

/* 바 차트 */
.bar-chart, .score-bars, .grade-list { display: flex; flex-direction: column; gap: 0.8rem; }
.bar-row, .score-row, .grade-item {
  display: flex; align-items: center; gap: 0.8rem;
}
.bar-label, .score-label, .grade-name {
  width: 90px; font-size: 0.8rem; color: #888; font-weight: 700; flex-shrink: 0;
}
.bar-track, .score-track, .grade-track {
  flex: 1; height: 10px; background: #252836; border-radius: 99px; overflow: hidden;
}
.bar-fill, .score-fill, .grade-fill {
  height: 100%; border-radius: 99px; background: #4ECDC4; transition: width 0.8s;
}
.bar-pct, .score-val, .grade-count {
  width: 35px; font-size: 0.8rem; color: #666; font-weight: 700; text-align: right;
}

.coming-soon { font-size: 0.8rem; color: #444; }
</style>
