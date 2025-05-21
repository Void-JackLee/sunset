<script setup>
import { ref } from "vue";
import { getAttr } from "../util/util.js";
import {getJSON} from "../util/request.js";
import {message} from "ant-design-vue";

const windy = ref()

window.addEventListener("message",e => {
  if (e.data.type === 'run') {
    console.log("run " + e.data.name);
    const L = windy.value.contentWindow.L;
    const map = windy.value.contentWindow.W.map.map;
    const func = eval(e.data.func)
    func(e.data.data,L,map)
  }
})

const lat = ref(getAttr('lat'))
const lon = ref(getAttr('lon'))
const marker = ref(getAttr('marker'))

const init = async () => {
  window.parent.postMessage('doneLoad','*')
}
</script>

<template>
  <div id="container">
    <iframe @load="init" ref="windy" id="windy" scrolling="no" :src="`/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=°C&metricWind=default&zoom=7&overlay=satellite&product=ecmwf&level=surface&lat=${lat}&lon=${lon}&detailLat=${lat}&detailLon=${lon}${marker === 'true' ? '&marker=true' : ''}&message=true`" frameborder="0"></iframe>
  </div>
</template>

<style scoped>
#container {
  height: 100%;
  overflow: hidden;
}

#windy {
  width: 100%;
  height: 100%;
}
</style>