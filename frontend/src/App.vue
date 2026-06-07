<template>
  <router-view />
</template>

<script setup>
</script>

<style>
html, body, #app {
  height: 100%; min-height: 100vh; min-height: 100dvh;
  margin: 0; padding: 0; overscroll-behavior: none;
}
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #fdfaf6; color: #3a322c;
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
}
a { text-decoration: none; color: inherit; }
:focus-visible { outline: 2px solid rgba(37,99,235,0.4); outline-offset: 2px; border-radius: 3px; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d8cec2; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #beb2a4; }
</style>
