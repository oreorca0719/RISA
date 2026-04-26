<template>
  <div class="result-page">
    <NavBar @logout="handleLogout" />
    <main class="main">
      <div class="page-header">
        <h1>📊 내 결과</h1>
        <p>나의 읽기 능력을 확인해봐요!</p>
      </div>

      <!-- 진단 결과 없을 때 -->
      <div v-if="!hasResult" class="empty-state">
        <div class="empty-illust">🔍</div>
        <h2>아직 진단 결과가 없어요</h2>
        <p>진단을 완료하면 나의 읽기 수준을 알 수 있어요!</p>
        <button class="btn-primary" @click="router.push('/student/diagnosis')">
          지금 진단하러 가기 🚀
        </button>
      </div>

      <!-- 진단 결과 있을 때 (TODO: 실제 데이터 연동) -->
      <div v-else class="result-content">
        <div class="level-card">
          <div class="level-badge">Lv. 3</div>
          <h2>읽기 수준: <span class="highlight">중급</span></h2>
          <p>또래 평균과 비슷한 수준이에요! 조금만 더 노력하면 상급이 될 수 있어요 💪</p>
        </div>

        <div class="chart-grid">
          <div class="chart-card">
            <h3>🎤 음독 유창성</h3>
            <div class="bar-wrap">
              <div class="bar" style="width: 72%"></div>
            </div>
            <span class="score">72점</span>
            <p class="coming-soon">🔧 상세 분석 준비 중</p>
          </div>
          <div class="chart-card">
            <h3>👁️ 묵독 유창성</h3>
            <div class="bar-wrap">
              <div class="bar bar--yellow" style="width: 65%"></div>
            </div>
            <span class="score">65점</span>
            <p class="coming-soon">🔧 상세 분석 준비 중</p>
          </div>
          <div class="chart-card">
            <h3>🧠 독해 이해</h3>
            <div class="bar-wrap">
              <div class="bar bar--coral" style="width: 58%"></div>
            </div>
            <span class="score">58점</span>
            <p class="coming-soon">🔧 상세 분석 준비 중</p>
          </div>
        </div>

        <div class="prescription-card">
          <h3>📚 맞춤 도서 처방</h3>
          <p class="coming-soon">🔧 AI 맞춤 도서 추천 기능 준비 중이에요!</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const hasResult = ref(false) // TODO: 실제 API 연동 후 변경

function handleLogout() { router.push('/login') }
</script>

<style scoped>
.result-page { min-height: 100vh; background: var(--gray-light); }
.main { max-width: 900px; margin: 0 auto; padding: 2rem; }
.page-header { margin-bottom: 2rem; }
.page-header h1 { font-size: 1.8rem; font-weight: 900; }
.page-header p { color: var(--gray); margin-top: 0.3rem; }

.empty-state {
  background: var(--white);
  border-radius: var(--radius);
  padding: 4rem 2rem;
  text-align: center;
  box-shadow: var(--shadow);
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
}
.empty-illust { font-size: 5rem; }
.empty-state h2 { font-size: 1.4rem; font-weight: 900; }
.empty-state p { color: var(--gray); }

.result-content { display: flex; flex-direction: column; gap: 1.5rem; }

.level-card {
  background: linear-gradient(135deg, var(--mint) 0%, var(--mint-dark) 100%);
  border-radius: var(--radius);
  padding: 2.5rem;
  color: white;
  display: flex; flex-direction: column; gap: 0.8rem;
}
.level-badge {
  background: rgba(255,255,255,0.2);
  display: inline-block; padding: 0.4rem 1rem;
  border-radius: 99px; font-weight: 900; font-size: 0.9rem; width: fit-content;
}
.level-card h2 { font-size: 1.5rem; font-weight: 900; }
.highlight { color: var(--yellow); }
.level-card p { opacity: 0.9; }

.chart-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.chart-card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: var(--shadow);
  display: flex; flex-direction: column; gap: 0.8rem;
}
.chart-card h3 { font-size: 1rem; font-weight: 800; }
.bar-wrap { background: var(--gray-light); border-radius: 99px; height: 12px; overflow: hidden; }
.bar { background: var(--mint); height: 100%; border-radius: 99px; transition: width 1s ease; }
.bar--yellow { background: var(--yellow-dark); }
.bar--coral { background: var(--coral); }
.score { font-size: 1.5rem; font-weight: 900; color: var(--navy); }

.prescription-card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
  display: flex; flex-direction: column; gap: 1rem;
}
.prescription-card h3 { font-size: 1.1rem; font-weight: 800; }

.btn-primary {
  background: var(--mint); color: white; border: none;
  padding: 0.9rem 2.5rem; border-radius: 99px;
  font-size: 1rem; font-weight: 800; transition: all 0.2s;
}
.btn-primary:hover { background: var(--mint-dark); transform: translateY(-2px); box-shadow: var(--shadow-hover); }
.coming-soon { font-size: 0.82rem; color: var(--gray); background: var(--gray-light); padding: 0.4rem 0.8rem; border-radius: 99px; width: fit-content; }
</style>
