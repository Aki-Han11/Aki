<template>
  <router-view />
</template>

<script setup>
</script>

<style>
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
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', 'Arial', sans-serif;
  background: #f5f7fa;
  color: #2c3e50;
}

a {
  text-decoration: none;
  color: inherit;
}
</style>
