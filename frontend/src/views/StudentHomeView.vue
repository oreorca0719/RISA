<template>
  <div class="student-home">
    <NavBar @logout="handleLogout" />

    <main class="main">
      <div class="welcome-section">
        <div class="welcome-text">
          <h1>안녕하세요, <span class="name">{{ studentName }}</span>님! 👋</h1>
          <p>오늘도 책과 함께 즐거운 시간 보내봐요!</p>
        </div>
        <div class="welcome-illust">📚</div>
      </div>

      <div class="cards-grid">
        <div class="card card-diagnosis" @click="router.push('/student/diagnosis')">
          <div class="card-icon">🔍</div>
          <h2>읽기 진단</h2>
          <p>나의 읽기 능력을 확인해봐요</p>
          <div class="card-badge">시작하기 →</div>
        </div>

        <div class="card card-result" @click="router.push('/student/result')">
          <div class="card-icon">📊</div>
          <h2>내 결과</h2>
          <p>지난 진단 결과를 확인해봐요</p>
          <div class="card-badge card-badge--gray">결과 보기 →</div>
        </div>

        <div class="card card-books">
          <div class="card-icon">📖</div>
          <h2>추천 도서</h2>
          <p>나에게 딱 맞는 책을 찾아봐요</p>
          <div class="card-badge card-badge--yellow">준비 중 🔧</div>
        </div>
      </div>

      <div class="status-section">
        <h2>내 학습 현황</h2>
        <div class="status-cards">
          <div class="status-card">
            <div class="status-icon">🏆</div>
            <div class="status-info">
              <span class="status-value">-</span>
              <span class="status-label">진단 횟수</span>
            </div>
          </div>
          <div class="status-card">
            <div class="status-icon">⭐</div>
            <div class="status-info">
              <span class="status-value">-</span>
              <span class="status-label">읽기 수준</span>
            </div>
          </div>
          <div class="status-card">
            <div class="status-icon">📅</div>
            <div class="status-info">
              <span class="status-value">-</span>
              <span class="status-label">마지막 진단</span>
            </div>
          </div>
        </div>
        <p class="status-hint">진단을 완료하면 나의 읽기 수준을 알 수 있어요!</p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const studentName = ref('학생') // TODO: 실제 사용자 정보 연동

function handleLogout() {
  // TODO: 로그아웃 처리
  router.push('/login')
}
</script>

<style scoped>
.student-home { min-height: 100vh; background: var(--gray-light); }
.main { max-width: 1100px; margin: 0 auto; padding: 2rem; }

.welcome-section {
  background: linear-gradient(135deg, var(--mint) 0%, var(--mint-dark) 100%);
  border-radius: var(--radius);
  padding: 2.5rem;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}
.welcome-text h1 { font-size: 1.8rem; font-weight: 900; margin-bottom: 0.5rem; }
.welcome-text .name { color: var(--yellow); }
.welcome-text p { font-size: 1rem; opacity: 0.9; }
.welcome-illust { font-size: 5rem; }

.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.2rem;
  margin-bottom: 2rem;
}
.card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 2rem;
  cursor: pointer;
  transition: all 0.25s;
  box-shadow: var(--shadow);
}
.card:hover { transform: translateY(-4px); box-shadow: var(--shadow-hover); }
.card-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.card h2 { font-size: 1.2rem; font-weight: 800; margin-bottom: 0.4rem; color: var(--navy); }
.card p { font-size: 0.9rem; color: var(--gray); margin-bottom: 1.2rem; }

.card-badge {
  display: inline-block;
  background: var(--mint);
  color: white;
  font-weight: 800;
  font-size: 0.85rem;
  padding: 0.4rem 1rem;
  border-radius: 99px;
}
.card-badge--gray { background: var(--gray-light); color: var(--gray); }
.card-badge--yellow { background: var(--yellow); color: var(--navy); }

.status-section h2 { font-size: 1.2rem; font-weight: 800; margin-bottom: 1rem; }
.status-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}
.status-card {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow);
}
.status-icon { font-size: 2rem; }
.status-info { display: flex; flex-direction: column; }
.status-value { font-size: 1.5rem; font-weight: 900; color: var(--navy); }
.status-label { font-size: 0.8rem; color: var(--gray); font-weight: 600; }
.status-hint { color: var(--gray); font-size: 0.9rem; text-align: center; padding: 0.5rem; }
</style>
