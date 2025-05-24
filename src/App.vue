<script setup>
import zhCN from "ant-design-vue/es/locale/zh_CN";

import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';

dayjs.locale(zhCN.locale);
</script>

<template>
  <a-config-provider :locale="zhCN">
    <router-view/>
  </a-config-provider>
</template>

<style scoped>

</style>
