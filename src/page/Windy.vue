<script setup>
import {computed, onMounted, ref} from "vue";
import {message} from "ant-design-vue";
import {getJSON} from "../util/request.js";
import dayjs from 'dayjs';
import {round} from "lodash-es";

const windy = ref()
const openTip = ref(false)
const showBottom = ref(true)

const domain = window.location.hostname
const loadMap = ref(false)
const lat = ref(30.261)
const lng = ref(120.117)
const lat_init = ref(30.261)
const lng_init = ref(120.117)
const lineData = ref({})

const type = ref("sunset")
const overlay = ref("satellite")
const product = ref("ecmwf")
const date = ref(dayjs())
const pickerPos = ref(null) // { lat: number, lon: number }
const city = ref(null)


const _cloudHeight = ref(3150)
const confirmLoading = ref(false);
const cloudHeight = ref(3150)
const showCloudHeight = ref(false)
const boundary = ref(400)

const getFuncString = (func) => {
  return func.toString() + "\n" + func.name;
}

const setLineAndMarker = (val) => {
  const data = JSON.parse(JSON.stringify(val))
  function sunsetSunriseLine(data, L, map) {
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
    name: sunsetSunriseLine.name,
    func: getFuncString(sunsetSunriseLine),
    data: data
  },'*')
}

const drawSunLine = (val) => {
  const data = JSON.parse(JSON.stringify(val))
  function move(data, L, map) {
    const init = () => {
      window.sunLine = L.polyline(data, {color: '#ffffff', weight: 2});
      window.sunLine.addTo(map)
    }

    if (!window.sunLine) {
      init()
    } else {
      window.sunLine.setLatLngs(data)
    }
  }

  windy.value.contentWindow.postMessage({
    type: 'run',
    name: move.name,
    func: getFuncString(move),
    data: data
  },'*')
}

// ----- get api -----
const getSunset = async () => {
  const res = await getJSON(`api/getSunsetTime?lat=${lat.value}&lng=${lng.value}&time=${date.value.valueOf()}&hc=${cloudHeight.value / 1000}`);
  lineData.value = res.data;
  boundary.value = Math.round(res.data.boundary);
}

const getSunrise = async () => {
  const res = await getJSON(`api/getSunriseTime?lat=${lat.value}&lng=${lng.value}&time=${date.value.valueOf()}&hc=${cloudHeight.value / 1000}`);
  lineData.value = res.data;
  boundary.value = Math.round(res.data.boundary);
}

const getSunPos = async () => {
  const res = await getJSON(`api/getSunPos?lat=${lat.value}&lng=${lng.value}`);
  drawSunLine(res.data)
}

const getCityPos = async () => {
  try {
    const res = await getJSON(`api/getLocation?loc=${city.value}`);
    moveCenter(res.data.lat, res.data.lng)
    changePos(res.data.lat, res.data.lng)
  } catch (err) {
    message.error(err.msg);
  }
}

// ----- attribute change -----

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

const changeDate = () => {
  if (date.value) {
    changeType()
  }
}

const changePos = async (_lat = undefined, _lng = undefined) => {
  if (_lat === undefined || _lng === undefined) {
    lat.value = pickerPos.value.lat
    lng.value = pickerPos.value.lon
  } else {
    lat.value = _lat
    lng.value = _lng
  }

  await changeType()
  await getSunPos()
  windy.value.contentWindow.postMessage({
    type: 'pickerPos',
    pos: null
  },'*')
}

const changeCloudHeight = async () => {
  confirmLoading.value = true
  cloudHeight.value = _cloudHeight.value;
  await changeType();
  confirmLoading.value = false
  showCloudHeight.value = false
}

const moveCenter = async (lat, lng) => {
  function setCenter(data, L, map, W) {
    map.panTo([data.lat, data.lng])
  }
  windy.value.contentWindow.postMessage({
    type: 'run',
    name: setCenter.name,
    func: getFuncString(setCenter),
    data: { lat, lng }
  },'*')
}

// ----- set listener ------
const setPositionListener = () => {
  function setPickerListener(data, L, map, W) {
    W.store.on('pickerLocation',pos => {
      window.parent.postMessage({ type: 'pickerPos', pos },'*')
    })
    window.addEventListener("message",e => {
      if (e.data.type === 'pickerPos') {
        W.store.set('pickerLocation',e.data.pos)
      }
    })
  }
  windy.value.contentWindow.postMessage({
    type: 'run',
    name: setPickerListener.name,
    func: getFuncString(setPickerListener)
  },'*')
  window.addEventListener("message",e => {
    if (e.data.type === 'pickerPos') {
      pickerPos.value = e.data.pos
    }
  })
}

// ----- 初始化 -----
const init = () => {
  try {
    setLineAndMarker(lineData.value)
    setPositionListener()
    setInterval(getSunPos,5000)
    getSunPos()
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
        if (e.data.type === 'doneLoad') {
          init()
        }
      })
    } catch (e) {
      message.error(JSON.stringify(e))
    }
  }
  // 1. 获取位置信息
  try {
    navigator.geolocation.getCurrentPosition(async position => {
      try {
        lat.value = position.coords.latitude
        lng.value = position.coords.longitude
        lat_init.value = position.coords.latitude
        lng_init.value = position.coords.longitude
        load()
      } catch (e) {
        message.warning('使用默认位置')
        load()
      }
    }, async err => {
      message.warning('使用默认位置')
      load()
    })
  } catch (e) {
    message.warning('使用默认位置')
    load()
  }
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
            <a-radio-button value="clouds">预测</a-radio-button>
          </a-radio-group>
        </span>
        <span class="item">
          <span>预报：</span>
          <a-radio-group v-model:value="product" button-style="solid" @change="changeProduct">
            <a-radio-button value="ecmwf">ecm</a-radio-button>
            <a-radio-button value="gfs">gfs</a-radio-button>
            <a-radio-button value="icon">icon</a-radio-button>
          </a-radio-group>
        </span>
      </div>
      <div class="vcenter">
        <span class="item">
          <span>时间: </span>
          <a-date-picker v-model:value="date" @change="changeDate"/>
        </span>
        <span class="item">
          <span>位置: </span>
          <a-input-search
              v-model:value="city"
              placeholder="请输入城市"
              enter-button
              @search="getCityPos"
          />
        </span>
      </div>
      <div class="vcenter">
        <span class="item">
          <span>云底高度：{{ cloudHeight / 1000 }} km</span>&nbsp;
          <a-button ghost @click="showCloudHeight = true;_cloudHeight = cloudHeight">修改</a-button>
        </span>
      </div>
    </a-card>
  </div>
  <div id="container">
    <iframe v-if="loadMap" ref="windy" id="windy" :src="`//${domain}:9180/sunset/windy_iframe?lat=${lat_init}&lon=${lng_init}`" frameborder="0"></iframe>
  </div>
  <div class="content bottom" ref="bottom">
    <div class="hide-button" @click="showBottom = !showBottom">{{showBottom ? '收缩' : '展开'}}</div>
    <div v-show="showBottom" class="info">
      <span class="pos-span"><b>经纬度:&nbsp;</b>{{lat}}, {{lng}}<button v-if="pickerPos != null" @click="changePos">修改位置</button></span>
      <div class="pos-table">
        <div>
          <div><b>经度：</b>{{lng}}</div>
          <div><b>纬度：</b>{{lat}}</div>
        </div>
        <div><button v-if="pickerPos != null" @click="changePos">修改位置</button></div>
      </div>
      <span class="clear"></span>
      <span><b>{{ type === 'sunset' ? '落日' : '日出' }}时间:&nbsp;</b>{{ lineData.time }}</span>
    </div>
    <div v-show="showBottom" class="tip">
      <div class="divider"></div>
      <div>说明：<span style="color: #ff5900">浅橙色</span>代表太阳落日前30分钟线，<span style="color: #ff2400">橙色</span>代表落日线，<span style="color: #cc0000">暗红色</span>代表太阳落日后30分钟线；<span style="color: #7553f2;">紫色点</span>代表您的位置，<span style="color: #17aa03;">绿色点</span>代表距离您<b>{{boundary}}km</b>处，<span style="color: #318bff;">蓝色点</span>代表距离您<b>{{boundary*2}}km</b>处。一般而言，<b><span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间有云，<span style="color: #17aa03;">绿色点</span>和<span style="color: #318bff;">蓝色点</span>之间没有云，说明有<span style="color: #ff2400">晚霞</span>。</b>如果<span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间的云太厚了，那么无云空间需要离您更近才可能会烧。</div>
    </div>
    <div v-show="showBottom" class="tip-expand">
      <div @click="openTip = true">展开说明</div>
    </div>
    <a-modal v-model:open="showCloudHeight"
             title="云底高度"
             ok-text="确定"
             cancel-text="取消"
             @ok="changeCloudHeight"
             :confirm-loading="confirmLoading">
      <div style="display: flex;">
        <a-slider v-model:value="_cloudHeight" :min="1000" :max="10000" :step="50" style="flex: 1;margin-left: 0"/>
        <div style="display: flex;align-items: center;margin-left: 5px">
          <a-input-number
            v-model:value="_cloudHeight"
            :min="1000"
            :max="10000"
            :step="50"/>
          <div>&nbsp;m</div>
        </div>
      </div>
      <div style="margin-top: 12px">
        <template v-if="_cloudHeight <= 2500">
          <b>低云</b>：很难形成火烧云，入射光线距离比较近。
        </template>
        <template v-else-if="_cloudHeight <= 6000">
          <b>中云</b>：能形成很猛烈的火烧云，大烧云基本都是由它组成。
        </template>
        <template v-else>
          <b>高云</b>：能形成比较温柔的火烧云，云比较高，如果远端没有云，烧的持续时间往往也比较久。
        </template>
      </div>
    </a-modal>
  </div>
  <a-drawer
      v-model:open="openTip"
      :style="{
        'background': '#000'
      }"
      :closable="false"
      placement="bottom"
      height="150"
      @after-open-change="afterOpenChange"
  >
    <div>说明：<span style="color: #ff5900">浅橙色</span>代表太阳落日前30分钟线，<span style="color: #ff2400">橙色</span>代表落日线，<span style="color: #cc0000">暗红色</span>代表太阳落日后30分钟线；<span style="color: #7553f2;">紫色点</span>代表您的位置，<span style="color: #17aa03;">绿色点</span>代表距离您<b>{{boundary}}km</b>处，<span style="color: #318bff;">蓝色点</span>代表距离您<b>{{boundary*2}}km</b>处。一般而言，<b><span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间有云，<span style="color: #17aa03;">绿色点</span>和<span style="color: #318bff;">蓝色点</span>之间没有云，说明有<span style="color: #ff2400">晚霞</span>。</b>如果<span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间的云太厚了，那么无云空间需要离您更近才可能会烧。</div>
  </a-drawer>
</div>
</template>

<style lang="scss" scoped>
.link-btn {
  text-decoration: underline;
  cursor: pointer;
  user-select: none;
}

#windy-container {
  height: 100%;
  //overflow: hidden;
  display: flex;
  flex-direction: column;

  .content {
    padding: 10px;
  }

  .ant-card {
    border-color: #555;
    background-color: #242424;
    color: white;
  }

  .ant-picker {
    background: transparent;
    color: white !important;
    border-color: #555;
  }

  .divider {
    position: relative;
    padding: 7px 5px;
    clear: both;
    &:before {
      content: '';
      background-color: #3c3c3c;
      width: 100%;
      height: 1px;
      position: absolute;
      bottom: 7px;
      left: 0;
    }
  }
}

.vcenter {
  &:not(:first-child) {
    margin-top: 5px;
  }
  display: flex;
  align-items: center;
  .item {
    margin-right: 10px;
    >span {
      word-break: keep-all;
    }
  }
}

#container {
  flex: 1;
  #windy {
    width: 100%;
    height: 100%;
  }
}

.bottom {
  position: relative;
  padding-bottom: 5px !important;
  .hide-button {
    padding: 5px 7px;
    border-radius: 0 0 5px 5px;
    opacity: 0.7;
    background: #3c3c3c;
    color: white;
    position: absolute;
    right: 0;
    top: 0;
    font-size: 12px;
    cursor: pointer;
    z-index: 1000;
  }
  .info {
    margin-bottom: 5px;
    .pos-table {
      display: none;
      margin-bottom: 5px;
      >div:last-child {
        padding: 3px 10px;
        button {
          background: #646cff;
          color: white;
          padding: 0 10px;
          height: 100%;
          transition: 0.3s all;
          &:hover {
            background: #7880f4;
          }
        }
      }
      @media screen and (max-width: 485px) {
        display: flex;
      }
    }
    >span {
      float: left;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      &.clear {
        @media screen and (max-width: 847px) {
          clear: both;
        }
      }
      &:first-child {
        margin-right: 10px;
        @media screen and (max-width: 485px) {
          display: none;
        }
      }
      button {
        text-align: center;
        font-size: 0.7em;
        line-height: 24px;
        margin-left: 10px;
        height: 24px;
        background: #646cff;
        color: white;
        padding: 0 10px;
        transition: 0.3s all;
        &:hover {
          background: #7880f4;
        }
      }
    }
  }

  .tip {
    clear: both;
    >div:last-child {
      max-height: 100px;
      overflow-y: auto;
    }
    @media screen and (max-width: 499px) {
      display: none;
    }
    @media screen and (max-height: 750px) {
      display: none;
    }
  }
  .tip-expand {
    padding-top: 5px;
    display: none;
    clear: both;
    >div {
      text-align: center;
      background: #1677ff;
      transition: 0.3s all;
      &:active {
        background: #4f98ff;
      }
      color: white;
      cursor: pointer;
    }
    @media screen and (max-width: 499px) {
      display: block;
    }
    @media screen and (max-height: 750px) {
      display: block;
    }
  }
}


:deep {
  .ant-card-body {
    padding: 5px 10px !important;
  }

  .ant-radio-button-wrapper,.ant-btn-background-ghost {
    background: transparent;
    color: white;
    border-color: #555;
  }

  .ant-radio-button-wrapper {
    @media screen and (max-width: 499px) {
      padding-inline: 13px;
    }

    @media screen and (max-width: 471px) {
      padding-inline: 10px;
    }

    @media screen and (max-width: 428px) {
      padding-inline: 8px;
    }

    @media screen and (max-width: 399px) {
      padding-inline: 7px;
    }

    @media screen and (max-width: 384px) {
      padding-inline: 6px;
    }

    @media screen and (max-width: 370px) {
      padding-inline: 5px;
    }

    @media screen and (max-width: 355px) {
      padding-inline: 4px;
    }

    @media screen and (max-width: 340px) {
      padding-inline: 3px;
    }

    @media screen and (max-width: 326px) {
      padding-inline: 2px;
    }
  }

  .ant-input-search {
    width: auto;
    vertical-align: middle;
    input {
      color: white;
      background: #242424;
      border-color: #555;
      &::placeholder {
        color: #FFFFFF99;
      }
    }
  }

  .ant-picker-input {
    input, .ant-picker-suffix {
      color: white;
    }

    input::placeholder {
      color: white;
    }



    .ant-picker-clear {
      background: #242424;
      color: #FFFFFF99;
    }
  }
}
</style>
