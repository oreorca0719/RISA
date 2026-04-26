<template>
  <AdminLayout @logout="handleLogout">
    <template #title>텍스트 풀 관리</template>

    <div class="texts-page">
      <!-- 필터 + 추가 버튼 -->
      <div class="toolbar">
        <div class="filters">
          <select v-model="filterGrade">
            <option value="">전체 학년</option>
            <option v-for="g in gradeOptions" :key="g.value" :value="g.value">{{ g.label }}</option>
          </select>
          <select v-model="filterGenre">
            <option value="">전체 장르</option>
            <option value="narrative">이야기글 (서사)</option>
            <option value="expository">설명글 (정보)</option>
          </select>
          <select v-model="filterLevel">
            <option value="">전체 수준</option>
            <option value="low">하</option>
            <option value="mid">중</option>
            <option value="high">상</option>
          </select>
        </div>
        <button class="add-btn">+ 텍스트 추가</button>
      </div>

      <!-- 원칙 안내 -->
      <div class="principle-banner">
        <span>📋</span>
        <div>
          <strong>이은주(2026) 텍스트 선정 7원칙 적용 필요</strong>
          <span> — 배경지식 통제 · 문화 편향 배제 · 장르 2종 이상 · 학년별 어휘 수준 · 적정 길이 · 독립성 · 중립성</span>
        </div>
      </div>

      <!-- 테이블 -->
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>제목</th>
              <th>학년</th>
              <th>장르</th>
              <th>수준</th>
              <th>어절 수</th>
              <th>7원칙</th>
              <th>등록일</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody>
            <tr class="coming-soon-row">
              <td colspan="8">
                <div class="empty-state">
                  <span>🔧</span>
                  <span>텍스트 풀 데이터 등록 및 API 연동 준비 중</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 구성 현황 -->
      <div class="coverage-panel">
        <h2 class="panel-title">텍스트 풀 구성 현황</h2>
        <p class="coverage-desc">학년별 × 장르별 × 수준별 최소 1개 이상 필요 (총 42개 이상)</p>
        <div class="coverage-grid">
          <div class="coverage-header">
            <span></span>
            <span>이야기글 (하)</span>
            <span>이야기글 (중)</span>
            <span>이야기글 (상)</span>
            <span>설명글 (하)</span>
            <span>설명글 (중)</span>
            <span>설명글 (상)</span>
          </div>
          <div class="coverage-row" v-for="g in gradeOptions" :key="g.value">
            <span class="grade-name">{{ g.label }}</span>
            <span class="cell empty" v-for="i in 6" :key="i">-</span>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/admin/AdminLayout.vue'

const router = useRouter()
const filterGrade = ref('')
const filterGenre = ref('')
const filterLevel = ref('')

const gradeOptions = [
  { value: 'elem1', label: '초등 1학년' },
  { value: 'elem2', label: '초등 2학년' },
  { value: 'elem3', label: '초등 3학년' },
  { value: 'elem4', label: '초등 4학년' },
  { value: 'elem5', label: '초등 5학년' },
  { value: 'elem6', label: '초등 6학년' },
  { value: 'mid1',  label: '중등 1학년' },
]

function handleLogout() { router.push('/login') }
</script>

<style scoped>
.texts-page { display: flex; flex-direction: column; gap: 1.2rem; }

.toolbar {
  display: flex; align-items: center; justify-content: space-between;
  background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 16px; padding: 1rem 1.5rem;
}
.filters { display: flex; gap: 0.6rem; }
select {
  background: #252836; border: 1px solid #2a2d3e; color: #aaa;
  padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.85rem;
  font-family: 'Nunito', sans-serif; outline: none; cursor: pointer;
}
select:focus { border-color: #4ECDC4; }

.add-btn {
  background: #4ECDC4; color: #0f1117; border: none;
  padding: 0.6rem 1.5rem; border-radius: 8px;
  font-size: 0.9rem; font-weight: 800; cursor: pointer; transition: all 0.2s;
}
.add-btn:hover { background: #38b2ab; }

.principle-banner {
  background: rgba(78,205,196,0.08); border: 1px solid rgba(78,205,196,0.2);
  border-radius: 12px; padding: 1rem 1.5rem;
  display: flex; align-items: flex-start; gap: 0.8rem;
  font-size: 0.85rem; color: #888;
}
.principle-banner span:first-child { font-size: 1.2rem; flex-shrink: 0; }
.principle-banner strong { color: #4ECDC4; }

.table-wrap {
  background: #1a1d27; border: 1px solid #2a2d3e;
  border-radius: 16px; overflow: hidden;
}
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  text-align: left; padding: 1rem 1.2rem;
  font-size: 0.72rem; font-weight: 800; color: #555;
  text-transform: uppercase; letter-spacing: 0.05em;
  border-bottom: 1px solid #2a2d3e;
}
.data-table td { padding: 1rem 1.2rem; border-bottom: 1px solid #1e2130; }
.empty-state {
  display: flex; align-items: center; gap: 0.7rem; justify-content: center;
  padding: 2.5rem; color: #555; font-size: 0.9rem;
}

.coverage-panel {
  background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 16px; padding: 1.5rem;
}
.panel-title { font-size: 0.95rem; font-weight: 800; color: #fff; margin-bottom: 0.4rem; }
.coverage-desc { font-size: 0.8rem; color: #555; margin-bottom: 1.2rem; }
.coverage-grid { display: flex; flex-direction: column; gap: 0.4rem; overflow-x: auto; }
.coverage-header, .coverage-row {
  display: grid; grid-template-columns: 100px repeat(6, 1fr);
  gap: 0.4rem; align-items: center;
}
.coverage-header span {
  font-size: 0.7rem; font-weight: 700; color: #555;
  text-align: center; padding: 0.4rem;
}
.grade-name { font-size: 0.8rem; color: #888; font-weight: 700; }
.cell {
  background: #252836; border-radius: 6px; padding: 0.5rem;
  text-align: center; font-size: 0.8rem; color: #444; font-weight: 700;
}
</style>
