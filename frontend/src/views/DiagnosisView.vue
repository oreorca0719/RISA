<template>
  <div class="diagnosis-page">
    <NavBar @logout="handleLogout" />
    <main class="main">
      <div class="page-header">
        <h1>📝 읽기 진단</h1>
        <p>차근차근 따라오면 금방 끝나요! 할 수 있어요 💪</p>
      </div>

      <div class="steps-bar">
        <div
          v-for="(step, i) in steps"
          :key="i"
          class="step"
          :class="{ active: currentStep === i, done: currentStep > i }"
        >
          <div class="step-dot">{{ currentStep > i ? '✓' : i + 1 }}</div>
          <span class="step-label">{{ step }}</span>
        </div>
      </div>

      <div class="diagnosis-card">
        <!-- Step 0: 안내 -->
        <div v-if="currentStep === 0" class="step-content">
          <div class="illust">🎯</div>
          <h2>진단을 시작해볼까요?</h2>
          <p>진단은 총 3단계로 이루어져요.<br>음독 → 묵독 → 독해 문항 순서로 진행됩니다.</p>
          <div class="info-boxes">
            <div class="info-box">
              <span>🎤</span><strong>음독 유창성</strong><p>소리 내어 읽기</p>
            </div>
            <div class="info-box">
              <span>👁️</span><strong>묵독 유창성</strong><p>눈으로 읽기</p>
            </div>
            <div class="info-box">
              <span>🧠</span><strong>독해 이해</strong><p>내용 파악하기</p>
            </div>
          </div>
          <button class="btn-primary" @click="currentStep++">시작하기 🚀</button>
        </div>

        <!-- Step 1: 음독 유창성 -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="illust">🎤</div>
          <h2>음독 유창성 측정</h2>
          <p>아래 글을 소리 내어 읽어주세요!</p>
          <div class="text-box">
            <p class="reading-text">
              <!-- TODO: 실제 텍스트 풀에서 로드 -->
              봄이 왔어요. 들판에 꽃이 피고 새들이 노래해요.
              아이들은 공원에 나가 신나게 뛰어 놀아요.
              따뜻한 햇살이 온 세상을 환하게 비춰줘요.
            </p>
          </div>
          <div class="timer-area">
            <div class="timer">⏱ {{ timerDisplay }}</div>
            <button v-if="!timerRunning" class="btn-primary" @click="startTimer">읽기 시작</button>
            <button v-else class="btn-stop" @click="stopTimer">다 읽었어요! ✋</button>
          </div>
          <p class="coming-soon">🔧 STT 자동 측정 기능은 준비 중이에요</p>
        </div>

        <!-- Step 2: 묵독 유창성 -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="illust">👁️</div>
          <h2>묵독 유창성 측정</h2>
          <p>아래 글을 속으로 읽고, 다 읽으면 버튼을 눌러주세요!</p>
          <div class="text-box">
            <p class="reading-text">
              <!-- TODO: 실제 텍스트 풀에서 로드 -->
              바다는 넓고 깊어요. 파도가 철썩철썩 소리를 내며 밀려와요.
              바닷속에는 형형색색의 물고기들이 살고 있어요.
              우리는 바다를 소중히 지켜야 해요.
            </p>
          </div>
          <div class="timer-area">
            <div class="timer">⏱ {{ timerDisplay }}</div>
            <button v-if="!timerRunning" class="btn-primary" @click="startTimer">읽기 시작</button>
            <button v-else class="btn-stop" @click="stopTimer">다 읽었어요! ✋</button>
          </div>
        </div>

        <!-- Step 3: 독해 문항 -->
        <div v-if="currentStep === 3" class="step-content">
          <div class="illust">🧠</div>
          <h2>독해 이해 문항</h2>
          <p>앞에서 읽은 글을 생각하며 질문에 답해봐요!</p>
          <div class="question-card">
            <p class="question-num">문제 1</p>
            <p class="question-text">봄이 되면 들판에서 무엇이 피나요?</p>
            <div class="options">
              <label v-for="opt in ['잎', '꽃', '눈', '비']" :key="opt" class="option">
                <input type="radio" name="q1" :value="opt" v-model="answers[0]" />
                <span>{{ opt }}</span>
              </label>
            </div>
          </div>
          <p class="coming-soon">🔧 GRI 25문항 연동 예정</p>
          <button class="btn-primary" @click="currentStep++">제출하기 📨</button>
        </div>

        <!-- Step 4: 완료 -->
        <div v-if="currentStep === 4" class="step-content step-done">
          <div class="illust illust-big">🎉</div>
          <h2>진단 완료!</h2>
          <p>정말 잘했어요! 결과를 분석하고 있어요.</p>
          <div class="done-badge">처리 중... ⏳</div>
          <p class="coming-soon">🔧 AI 채점 및 결과 분석 기능 준비 중</p>
          <button class="btn-primary" @click="router.push('/student/result')">결과 보러 가기 →</button>
        </div>

        <!-- 이전/다음 버튼 (step 1, 2) -->
        <div v-if="currentStep > 0 && currentStep < 3" class="nav-btns">
          <button class="btn-back" @click="currentStep--">← 이전</button>
          <button class="btn-primary" @click="nextStep">다음 →</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const currentStep = ref(0)
const timerRunning = ref(false)
const timerSeconds = ref(0)
const answers = ref<string[]>([])
let timerInterval: ReturnType<typeof setInterval> | null = null

const steps = ['안내', '음독', '묵독', '독해', '완료']

const timerDisplay = computed(() => {
  const m = Math.floor(timerSeconds.value / 60).toString().padStart(2, '0')
  const s = (timerSeconds.value % 60).toString().padStart(2, '0')
  return `${m}:${s}`
})

function startTimer() {
  timerRunning.value = true
  timerSeconds.value = 0
  timerInterval = setInterval(() => timerSeconds.value++, 1000)
}

function stopTimer() {
  timerRunning.value = false
  if (timerInterval) clearInterval(timerInterval)
}

function nextStep() {
  if (timerRunning.value) stopTimer()
  currentStep.value++
  timerSeconds.value = 0
}

function handleLogout() { router.push('/login') }
</script>

<style scoped>
.diagnosis-page { min-height: 100vh; background: var(--gray-light); }
.main { max-width: 800px; margin: 0 auto; padding: 2rem; }
.page-header { margin-bottom: 2rem; }
.page-header h1 { font-size: 1.8rem; font-weight: 900; }
.page-header p { color: var(--gray); margin-top: 0.3rem; }

.steps-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--white);
  border-radius: var(--radius);
  padding: 1.2rem 2rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow);
  position: relative;
}
.step { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; flex: 1; }
.step-dot {
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--gray-light); color: var(--gray);
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 0.9rem; transition: all 0.3s;
}
.step.active .step-dot { background: var(--mint); color: white; }
.step.done .step-dot { background: var(--mint-dark); color: white; }
.step-label { font-size: 0.75rem; font-weight: 700; color: var(--gray); }
.step.active .step-label { color: var(--mint-dark); }

.diagnosis-card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 3rem;
  box-shadow: var(--shadow);
  min-height: 400px;
}
.step-content { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 1.2rem; }
.illust { font-size: 4rem; }
.illust-big { font-size: 5rem; }
h2 { font-size: 1.5rem; font-weight: 900; color: var(--navy); }
p { color: var(--gray); line-height: 1.6; }

.info-boxes { display: flex; gap: 1rem; margin: 0.5rem 0; }
.info-box {
  background: var(--mint-light);
  border-radius: var(--radius-sm);
  padding: 1.2rem;
  flex: 1;
  display: flex; flex-direction: column; align-items: center; gap: 0.3rem;
}
.info-box span { font-size: 1.8rem; }
.info-box strong { font-size: 0.9rem; font-weight: 800; color: var(--navy); }
.info-box p { font-size: 0.8rem; margin: 0; }

.text-box {
  background: var(--gray-light);
  border-radius: var(--radius-sm);
  padding: 1.5rem 2rem;
  width: 100%;
  border-left: 4px solid var(--mint);
}
.reading-text { font-size: 1.1rem; line-height: 1.9; color: var(--navy); text-align: left; }

.timer-area { display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.timer { font-size: 2.5rem; font-weight: 900; color: var(--mint-dark); }

.question-card {
  background: var(--gray-light);
  border-radius: var(--radius-sm);
  padding: 1.5rem;
  width: 100%;
  text-align: left;
}
.question-num { font-size: 0.85rem; font-weight: 700; color: var(--mint-dark); margin-bottom: 0.5rem; }
.question-text { font-size: 1.05rem; font-weight: 700; color: var(--navy); margin-bottom: 1rem; }
.options { display: flex; gap: 0.8rem; flex-wrap: wrap; }
.option {
  display: flex; align-items: center; gap: 0.4rem;
  background: white; border-radius: 99px; padding: 0.5rem 1.2rem;
  cursor: pointer; font-weight: 700; border: 2px solid #e8ecf0;
  transition: all 0.2s;
}
.option:has(input:checked) { border-color: var(--mint); background: var(--mint-light); color: var(--mint-dark); }
.option input { display: none; }

.coming-soon { font-size: 0.85rem; color: var(--gray); background: var(--gray-light); padding: 0.5rem 1rem; border-radius: 99px; }
.done-badge { background: var(--mint-light); color: var(--mint-dark); font-weight: 800; padding: 0.8rem 2rem; border-radius: 99px; }

.btn-primary {
  background: var(--mint); color: white; border: none;
  padding: 0.9rem 2.5rem; border-radius: 99px;
  font-size: 1rem; font-weight: 800; transition: all 0.2s;
}
.btn-primary:hover { background: var(--mint-dark); transform: translateY(-2px); box-shadow: var(--shadow-hover); }
.btn-stop {
  background: var(--coral); color: white; border: none;
  padding: 0.9rem 2.5rem; border-radius: 99px;
  font-size: 1rem; font-weight: 800; transition: all 0.2s;
}
.btn-stop:hover { filter: brightness(0.9); }

.nav-btns { display: flex; gap: 1rem; margin-top: 1rem; }
.btn-back {
  background: var(--gray-light); color: var(--gray); border: none;
  padding: 0.9rem 2rem; border-radius: 99px;
  font-size: 1rem; font-weight: 800; transition: all 0.2s;
}
.btn-back:hover { background: #e0e5ec; }
</style>
