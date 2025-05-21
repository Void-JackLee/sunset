<script setup>
import {computed, onMounted, ref} from "vue";
import {message} from "ant-design-vue";
import {getJSON} from "../util/request.js";

const windy = ref()

const domain = window.location.hostname
const lat = ref(30.261)
const lng = ref(120.117)

const getFuncString = (func) => {
  return func.toString() + "\n" + func.name;
}

function mount(data, L, map) {
  const srcDotIcon = L.divIcon({ html: '<div style="width: 15px;height: 15px;border-radius: 7.5px;background: #7553f2"></div>' });
  const midDotIcon = L.divIcon({ html: '<div style="width: 10px;height: 10px;border-radius: 5px;background: #17aa03"></div>' });
  const targetDotIcon = L.divIcon({ html: '<div style="width: 10px;height: 10px;border-radius: 5px;background: #318bff"></div>' });
  L.polyline(data['sunset'], {color: '#ff2400', weight: 2}).addTo(map)
  L.polyline(data['before30'], {color: '#ff5900', weight: 2}).addTo(map)
  L.polyline(data['after30'], {color: '#cc0000', weight: 2}).addTo(map)
  L.marker(data['sunset'][0], { icon: srcDotIcon }).addTo(map)
  L.marker(data['before30'][1], { icon: midDotIcon }).addTo(map)
  L.marker(data['sunset'][1], { icon: midDotIcon }).addTo(map)
  L.marker(data['after30'][1], { icon: midDotIcon }).addTo(map)
  L.marker(data['before30'][2], { icon: targetDotIcon }).addTo(map)
  L.marker(data['sunset'][2], { icon: targetDotIcon }).addTo(map)
  L.marker(data['after30'][2], { icon: targetDotIcon }).addTo(map)
}

const init = async () => {
  try {
    const res = await getJSON(`api/getSunsetTime?lat=${lat.value}&lng=${lng.value}&marker=false`);
    windy.value.contentWindow.postMessage({
      type: 'run',
      name: mount.name,
      func: getFuncString(mount),
      data: res.data
    },'*')
  } catch (e) {
    message.error(JSON.stringify(e))
  }
}

window.addEventListener("message",e => {
  if (e.data === 'doneLoad') {
    init()
  }
})

// onMounted(init)
</script>

<template>
<div id="windy-container">
  <iframe ref="windy" id="windy" :src="`//${domain}:9180/sunset/windy_iframe?lat=${lat}&lon=${lng}`" frameborder="0"></iframe>
  <div id="tool">
    说明：<span style="color: #ff5900">浅橙色</span>代表太阳落日前30分钟线，<span style="color: #ff2400">橙色</span>代表落日线，<span style="color: #cc0000">暗红色</span>代表太阳落日后30分钟线；<span style="color: #7553f2;">紫色点</span>代表您的位置，<span style="color: #17aa03;">绿色点</span>代表距离您200km处，<span style="color: #318bff;">蓝色点</span>代表距离您400km处。一般而言，<b><span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间有云，<span style="color: #17aa03;">绿色点</span>和<span style="color: #318bff;">蓝色点</span>之间没有云，说明有<span style="color: #ff2400">晚霞</span>。</b>如果<span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间的云太厚了，那么无云空间需要离您更近才可能会烧。
  </div>
</div>
</template>

<style lang="scss" scoped>

#tool {
  //height: 100px;
  padding: 16px;
}

#windy-container {
  height: 100%;
  //overflow: hidden;
  display: flex;
  flex-direction: column;
}

#windy {
  width: 100%;
  //height: 100%;
  flex: 1;
}
</style>