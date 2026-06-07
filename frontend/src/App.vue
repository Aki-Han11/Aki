<template>
  <router-view />
</template>

<script setup>
</script>

<style>
/* ══════════════════════════════════════════════════════════════
   Global Reset & Base Styles — EBookStore
   Clean, modern, pixel-perfect foundation
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
  background: #ffffff;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

a {
  text-decoration: none;
  color: inherit;
}

/* ── Smooth focus rings ── */
:focus-visible {
  outline: 2px solid rgba(37,99,235,0.5);
  outline-offset: 2px;
  border-radius: 4px;
}

/* ── Scrollbar refinement ── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
