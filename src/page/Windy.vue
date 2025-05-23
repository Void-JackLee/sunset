<script setup>
import {computed, onMounted, ref} from "vue";
import {message} from "ant-design-vue";
import {getJSON} from "../util/request.js";

const windy = ref()

const domain = window.location.hostname
const loadMap = ref(false)
const lat = ref(30.261)
const lng = ref(120.117)
const lineData = ref({})

const type = ref("sunset")
const overlay = ref("satellite")
const product = ref("ecmwf")

const getFuncString = (func) => {
  return func.toString() + "\n" + func.name;
}

const getSunset = async () => {
  const res = await getJSON(`api/getSunsetTime?lat=${lat.value}&lng=${lng.value}`);
  lineData.value = res.data;
}

const getSunrise = async () => {
  const res = await getJSON(`api/getSunriseTime?lat=${lat.value}&lng=${lng.value}`);
  lineData.value = res.data;
}

const setLineAndMarker = (val) => {
  const data = JSON.parse(JSON.stringify(val))
  function move(data, L, map) {
    const init = (lineData, markerData) => {
      const srcDotIcon = L.divIcon({ html: '<div style="width: 15px;height: 15px;border-radius: 7.5px;background: #7553f2"></div>' });
      const midDotIcon = L.divIcon({ html: '<div style="width: 10px;height: 10px;border-radius: 5px;background: #17aa03"></div>' });
      const targetDotIcon = L.divIcon({ html: '<div style="width: 10px;height: 10px;border-radius: 5px;background: #318bff"></div>' });
      const lines = [
        L.polyline(lineData[0], {color: '#ff2400', weight: 2}),
        L.polyline(lineData[1], {color: '#ff5900', weight: 2}),
        L.polyline(lineData[2], {color: '#cc0000', weight: 2}),
      ]
      const markers = [
        L.marker(markerData[0], { icon: srcDotIcon }),
        L.marker(markerData[1], { icon: midDotIcon }),
        L.marker(markerData[2], { icon: midDotIcon }),
        L.marker(markerData[3], { icon: midDotIcon }),
        L.marker(markerData[4], { icon: targetDotIcon }),
        L.marker(markerData[5], { icon: targetDotIcon }),
        L.marker(markerData[6], { icon: targetDotIcon })
      ]
      window.lines = lines
      window.markers = markers
      for (const line of lines) {
        line.addTo(map)
      }
      for (const marker of markers) {
        marker.addTo(map)
      }
    }

    const lineData = [
      data['target'], data['before30'], data['after30']
    ]

    const markerData = [
      data['target'][0],
      data['before30'][1],
      data['target'][1],
      data['after30'][1],
      data['before30'][2],
      data['target'][2],
      data['after30'][2]
    ]

    if (!window.lines || !window.markers) {
      init(lineData, markerData)
    } else {
      const lines = window.lines
      const markers = window.markers

      for (const i in lineData) {
        lines[i].setLatLngs(lineData[i])
      }

      for (const i in markerData) {
        markers[i].setLatLng(markerData[i])
      }
    }
  }

  windy.value.contentWindow.postMessage({
    type: 'run',
    name: move.name,
    func: getFuncString(move),
    data: data
  },'*')
}

const changeType = async () => {
  if (type.value === 'sunset') {
    try {
      await getSunset()
      setLineAndMarker(lineData.value)
    } catch (e) {
      message.error(JSON.stringify(e))
    }
  } else if (type.value === 'sunrise') {
    try {
      await getSunrise()
      setLineAndMarker(lineData.value)
    } catch (e) {
      message.error(JSON.stringify(e))
    }
  }
}

const changeOverlay = () => {
  function setOverlay(data, L, map, W) {
    W.store.set('overlay',data.overlay)
    W.store.set('product',data.product)
  }
  windy.value.contentWindow.postMessage({
    type: 'run',
    name: setOverlay.name,
    func: getFuncString(setOverlay),
    data: {
      overlay: overlay.value,
      product: product.value
    }
  },'*')
}

const changeProduct = () => {
  function setProduct(data, L, map, W) {
    W.store.set('product',data)
  }
  windy.value.contentWindow.postMessage({
    type: 'run',
    name: setProduct.name,
    func: getFuncString(setProduct),
    data: product.value
  },'*')
}

// ----- 初始化 Start -----
const init = () => {
  try {
    setLineAndMarker(lineData.value)
  } catch (e) {
    message.error(e)
  }
}

onMounted(async () => {
  const load = async () => {
    try {
      await getSunset()
      loadMap.value = true
      window.addEventListener("message",e => {
        if (e.data === 'doneLoad') {
          init()
        }
      })
    } catch (e) {
      message.error(JSON.stringify(e))
    }
  }
  // 1. 获取位置信息
  navigator.geolocation.getCurrentPosition(async position => {
    lat.value = position.coords.latitude
    lng.value = position.coords.longitude
    load()
  }, async err => {
    console.log('using default')
    load()
  })
})
// ----- 初始化 End -----
</script>

<template>
<div id="windy-container">
  <div class="content">
    <a-card>
      <div class="vcenter">
        <span class="item">
          <span>类型：</span>
          <a-radio-group v-model:value="type" button-style="solid" @change="changeType">
            <a-radio-button value="sunset">晚霞</a-radio-button>
            <a-radio-button value="sunrise">朝霞</a-radio-button>
          </a-radio-group>
        </span>
        <span class="item">
          <span>图层：</span>
          <a-radio-group v-model:value="overlay" button-style="solid" @change="changeOverlay">
            <a-radio-button value="satellite">云图</a-radio-button>
            <a-radio-button value="clouds">云预测</a-radio-button>
          </a-radio-group>
        </span>
        <span class="item">
          <span>预报：</span>
          <a-radio-group v-model:value="product" button-style="solid" @change="changeProduct">
            <a-radio-button value="ecmwf">ecm</a-radio-button>
            <a-radio-button value="gfs">gfs</a-radio-button>
          </a-radio-group>
        </span>
      </div>
    </a-card>
  </div>
  <div id="container">
    <iframe v-if="loadMap" ref="windy" id="windy" :src="`//${domain}:9180/sunset/windy_iframe?lat=${lat}&lon=${lng}`" frameborder="0"></iframe>
  </div>
  <div class="content">
    <div style="margin-bottom: 5px">
      <span><b>经纬度:</b> {{lat}}, {{lng}}</span>
      <span style="margin-left: 10px"><b>{{ type === 'sunset' ? '落日' : '日出' }}时间:</b> {{ lineData.time }}</span>
    </div>
    <div>说明：<span style="color: #ff5900">浅橙色</span>代表太阳落日前30分钟线，<span style="color: #ff2400">橙色</span>代表落日线，<span style="color: #cc0000">暗红色</span>代表太阳落日后30分钟线；<span style="color: #7553f2;">紫色点</span>代表您的位置，<span style="color: #17aa03;">绿色点</span>代表距离您200km处，<span style="color: #318bff;">蓝色点</span>代表距离您400km处。一般而言，<b><span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间有云，<span style="color: #17aa03;">绿色点</span>和<span style="color: #318bff;">蓝色点</span>之间没有云，说明有<span style="color: #ff2400">晚霞</span>。</b>如果<span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间的云太厚了，那么无云空间需要离您更近才可能会烧。</div>
  </div>
</div>
</template>

<style lang="scss" scoped>

.content {
  //height: 100px;
  padding: 10px;
}

.vcenter {
  display: flex;
  align-items: center;
  .item {
    margin-right: 10px;
  }
}

#windy-container {
  height: 100%;
  //overflow: hidden;
  display: flex;
  flex-direction: column;
}

#container {
  flex: 1;
  #windy {
    width: 100%;
    height: 100%;
  }
}

.ant-card {
  border-color: #555;
  background-color: #242424;
  color: white;
}

:deep {
  .ant-card-body {
    padding: 5px 10px !important;
  }

  .ant-radio-button-wrapper {
    background: transparent;
    color: white;
    border-color: #555;
  }
}


</style>