<script setup lang="ts">
interface Props {
  boundary: number;
  type: "rise" | "set";
  mode?: string;
}
const props = defineProps<Props>()
</script>

<template>
  <template v-if="mode === 'moon'">
    <div>说明：<span style="color: #ff5900">浅橙色</span>代表月{{ type === 'rise' ? '升' : '落' }}前30分钟线，<span style="color: #ff2400">橙色</span>代表月{{ type === 'rise' ? '升' : '落' }}线，<span style="color: #cc0000">暗红色</span>代表月{{ type === 'rise' ? '升' : '落' }}后30分钟线；<span style="color: #7553f2;">紫色点</span>代表您的位置，<span style="color: #318bff;">蓝色点</span>代表距离您<b>{{props.boundary}}km</b>处。一般而言，<b><span style="color: #318bff;">蓝色点</span>附近没有云，说明观测到 月{{ type === 'rise' ? '升' : '落' }} 的机会较高。</b></div>
  </template>
  <template v-else>
    <div>说明：<span style="color: #ff5900">浅橙色</span>代表太阳日{{ type === 'rise' ? '升' : '落' }}前30分钟线，<span style="color: #ff2400">橙色</span>代表日{{ type === 'rise' ? '升' : '落' }}线，<span style="color: #cc0000">暗红色</span>代表太阳日{{ type === 'rise' ? '升' : '落' }}后30分钟线；<span style="color: #7553f2;">紫色点</span>代表您的位置，<span style="color: #17aa03;">绿色点</span>代表距离您<b>{{props.boundary}}km</b>处，<span style="color: #318bff;">蓝色点</span>代表距离您<b>{{props.boundary*2}}km</b>处。一般而言，<b><span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间有云，<span style="color: #17aa03;">绿色点</span>和<span style="color: #318bff;">蓝色点</span>之间没有云，说明有<span style="color: #ff2400">{{ type === 'rise' ? '朝' : '晚' }}霞</span>。</b>如果<span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间的云太厚了，那么无云空间需要离您更近才可能会烧。</div>
  </template>

</template>

<style scoped>

</style>