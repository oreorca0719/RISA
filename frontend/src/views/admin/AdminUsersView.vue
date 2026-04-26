<template>
  <AdminLayout @logout="handleLogout">
    <template #title>사용자 관리</template>

    <div class="users-page">
      <!-- 탭 + 검색 -->
      <div class="toolbar">
        <div class="tabs">
          <button
            v-for="tab in tabs" :key="tab.value"
            class="tab" :class="{ active: activeTab === tab.value }"
            @click="activeTab = tab.value"
          >
            {{ tab.icon }} {{ tab.label }}
          </button>
        </div>
        <div class="search-bar">
          <input v-model="search" placeholder="이름 또는 아이디 검색..." />
        </div>
      </div>

      <!-- 테이블 -->
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>이름</th>
              <th>아이디</th>
              <th v-if="activeTab === 'student'">학년</th>
              <th v-if="activeTab === 'teacher'">소속</th>
              <th>가입일</th>
              <th>상태</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody>
            <tr class="coming-soon-row">
              <td colspan="7">
                <div class="empty-state">
                  <span>🔧</span>
                  <span>사용자 데이터 API 연동 준비 중입니다</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button class="page-btn" disabled>← 이전</button>
        <span class="page-info">1 / 1</span>
        <button class="page-btn" disabled>다음 →</button>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/admin/AdminLayout.vue'

const router = useRouter()
const search = ref('')
const activeTab = ref('student')

const tabs = [
  { value: 'student', label: '학생', icon: '👨‍🎓' },
  { value: 'parent', label: '학부모', icon: '👨‍👩‍👧' },
  { value: 'teacher', label: '교사', icon: '👩‍🏫' },
]

function handleLogout() { router.push('/login') }
</script>

<style scoped>
.users-page { display: flex; flex-direction: column; gap: 1.2rem; }

.toolbar {
  display: flex; align-items: center; justify-content: space-between; gap: 1rem;
  background: #1a1d27; border: 1px solid #2a2d3e; border-radius: 16px; padding: 1rem 1.5rem;
}
.tabs { display: flex; gap: 0.4rem; }
.tab {
  background: none; border: 1px solid #2a2d3e; color: #666;
  padding: 0.5rem 1.2rem; border-radius: 8px;
  font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: all 0.2s;
}
.tab.active { background: rgba(78,205,196,0.15); border-color: #4ECDC4; color: #4ECDC4; }
.tab:hover:not(.active) { border-color: #444; color: #aaa; }

.search-bar input {
  background: #252836; border: 1px solid #2a2d3e; color: #fff;
  padding: 0.6rem 1.2rem; border-radius: 8px; font-size: 0.9rem;
  width: 280px; outline: none; font-family: 'Nunito', sans-serif;
}
.search-bar input:focus { border-color: #4ECDC4; }
.search-bar input::placeholder { color: #555; }

.table-wrap {
  background: #1a1d27; border: 1px solid #2a2d3e;
  border-radius: 16px; overflow: hidden;
}
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  text-align: left; padding: 1rem 1.5rem;
  font-size: 0.75rem; font-weight: 800; color: #555;
  text-transform: uppercase; letter-spacing: 0.05em;
  border-bottom: 1px solid #2a2d3e;
}
.data-table td { padding: 1rem 1.5rem; border-bottom: 1px solid #1e2130; }

.coming-soon-row td { padding: 0; }
.empty-state {
  display: flex; align-items: center; gap: 0.7rem; justify-content: center;
  padding: 3rem; color: #555; font-size: 0.9rem;
}

.pagination {
  display: flex; align-items: center; justify-content: center; gap: 1rem;
}
.page-btn {
  background: #1a1d27; border: 1px solid #2a2d3e; color: #666;
  padding: 0.5rem 1.2rem; border-radius: 8px;
  font-size: 0.85rem; font-weight: 700; cursor: pointer;
}
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-info { color: #666; font-size: 0.85rem; font-weight: 700; }
</style>
