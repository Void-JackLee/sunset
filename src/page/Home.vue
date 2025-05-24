<script setup>
import {ref} from "vue";

const selectedKeys = ref(['windy']);

const year = ref(new Date().getFullYear())
</script>

<template>
  <div id="home">
    <a-layout-header>
      <div class="logo">Void火烧云</div>
      <a-menu
          v-model:selectedKeys="selectedKeys"
          theme="dark"
          mode="horizontal"
          :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="windy"><b>windy</b></a-menu-item>
      </a-menu>
    </a-layout-header>
    <router-view style="flex: 1" />
    <footer style="bottom: 10px;text-align: center">
      © Void-JackLee 2025-{{ year }} <a href="https://beian.miit.gov.cn" target="_blank">浙ICP备20011690号-4</a>
    </footer>
  </div>

</template>

<style lang="scss" scoped>
#home {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.logo {
  float: left;
  width: 120px;
  height: 64px;
  line-height: 64px;
  //padding: 16px 12px 16px 12px;
  text-align: center;
  font-weight: bold;
  background: #001529;
  color: white;
}
</style>
