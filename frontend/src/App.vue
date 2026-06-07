<template>
  <router-view />
</template>

<script setup>
</script>

<style>
/* ══════════════════════════════════════════════════════════════
   Global Reset & Base Styles — EBookStore
   Warm ivory palette · Unified design language
   ══════════════════════════════════════════════════════════════ */

html, body, #app {
  height: 100%;
  min-height: 100vh;
  min-height: 100dvh;
  margin: 0;
  padding: 0;
  overscroll-behavior: none;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
  background: #faf7f2;
  color: #3a322c;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

a {
  text-decoration: none;
  color: inherit;
}

:focus-visible {
  outline: 2px solid rgba(37,99,235,0.5);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Global Element Plus overrides — warm theme */
.el-card {
  background: #fffdfa !important;
  border: 1px solid #f0ece6 !important;
  border-radius: 18px !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.018), 0 1px 2px rgba(0,0,0,0.022) !important;
}
.el-button--primary {
  --el-button-bg-color: #2563eb;
  --el-button-border-color: #2563eb;
  --el-button-hover-bg-color: #1d4ed8;
  --el-button-hover-border-color: #1d4ed8;
}
.el-tag { border-radius: 8px !important; }
.el-input__wrapper {
  border-radius: 12px !important;
  box-shadow: none !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d4c8b8; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #b8a898; }
</style>
