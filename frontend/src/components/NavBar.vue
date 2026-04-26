<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <RouterLink to="/student" class="logo">
        <span class="logo-icon">📚</span>
        <span class="logo-text">RISA</span>
      </RouterLink>
      <div class="nav-links">
        <RouterLink to="/student" class="nav-link">홈</RouterLink>
        <RouterLink to="/student/diagnosis" class="nav-link">진단하기</RouterLink>
        <RouterLink to="/student/result" class="nav-link">내 결과</RouterLink>
      </div>
      <button class="logout-btn" @click="$emit('logout')">로그아웃</button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
defineEmits(['logout'])
</script>

<style scoped>
.navbar {
  background: var(--white);
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}
.navbar-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 64px;
  display: flex;
  align-items: center;
  gap: 2rem;
}
.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-weight: 900;
  font-size: 1.4rem;
  color: var(--mint-dark);
}
.logo-icon { font-size: 1.5rem; }
.nav-links {
  display: flex;
  gap: 0.5rem;
  flex: 1;
}
.nav-link {
  text-decoration: none;
  color: var(--gray);
  font-weight: 700;
  padding: 0.4rem 1rem;
  border-radius: 99px;
  transition: all 0.2s;
}
.nav-link:hover,
.nav-link.router-link-active {
  background: var(--mint-light);
  color: var(--mint-dark);
}
.logout-btn {
  background: none;
  border: 2px solid var(--gray-light);
  color: var(--gray);
  font-weight: 700;
  padding: 0.4rem 1.2rem;
  border-radius: 99px;
  transition: all 0.2s;
}
.logout-btn:hover {
  border-color: var(--coral);
  color: var(--coral);
}
</style>
