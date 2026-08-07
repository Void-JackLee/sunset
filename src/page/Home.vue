<script setup>
import {ref} from "vue";
import {useRoute, useRouter} from "vue-router";

const route = useRoute();
const router = useRouter();

let select = route.path.split('/').pop()
const selectedKeys = ref([select]);
const handleClick = e => {
  window.location.href = e.key
};

const year = ref(new Date().getFullYear())
</script>

<template>
  <div id="home">
    <a-layout-header>
      <div class="logo">Void晚霞观测</div>
      <a-menu
          v-model:selectedKeys="selectedKeys"
          theme="dark"
          mode="horizontal"
          @click="handleClick"
          :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="windy"><b>windy</b></a-menu-item>
<!--        <a-menu-item key="preview-3d"><b>3D预览</b></a-menu-item>-->
      </a-menu>
    </a-layout-header>
    <router-view style="flex: 1" />
    <footer class="footer">
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

.footer {
  padding-bottom: 5px;
  text-align: center
}
</style>
