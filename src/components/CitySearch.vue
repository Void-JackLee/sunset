<script setup lang="ts">
import {ref} from "vue";
import {message} from "ant-design-vue";
import { getJSON } from "../util/request";

const city = ref(null)
const code = ref('')
const codeRef = ref()
const openCaptcha = ref(false)
const loading = ref(false)
const rand = ref(new Date().getTime())

const emit = defineEmits(["changePos"])

const getCityPos = async () => {
  loading.value = true
  try {
    const res = await getJSON(`api/getLocation?loc=${city.value}&code=${code.value}`);
    emit("changePos",res.data.lat, res.data.lng);
    openCaptcha.value = false
  } catch (err) {
    message.error(err.msg);
    getRand()
  }
  loading.value = false
}

const openCaptchaModal = () => {
  if (city.value) {
    openCaptcha.value = true
    code.value = '';
    setTimeout(() => {codeRef.value.focus();}, 100)

    getRand()
  }
}

const getRand = () => {
  rand.value = new Date().getTime()
}
</script>

<template>
  <span>位置：</span>
  <a-input-search
      v-model:value="city"
      placeholder="请输入城市"
      enter-button
      @search="openCaptchaModal"
  />
  <a-modal title="验证码" v-model:open="openCaptcha" @ok="getCityPos" :confirm-loading="loading">
    <table>
      <tr>
        <td colspan="2">
          <img :src="'api/captcha?_=' + rand" @click="getRand">
        </td>
      </tr>
      <tr>
        <td>请输入验证码：</td>
        <td><a-input ref="codeRef" v-model:value="code" @keydown.enter="getCityPos"></a-input></td>
      </tr>
    </table>
  </a-modal>
</template>

<style lang="scss" scoped>
img {
  cursor: pointer;
}

table {
  margin-top: 20px;
  margin-left: 20px;

  tr:last-child td {
    padding-top: 20px;
  }
}
</style>
