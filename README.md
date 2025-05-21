# 实时云图朝晚霞通道绘制

为了解决目前朝霞晚霞预报翻车概率大的问题，本项目在windy云图的基础上绘制了朝晚霞通道，可以在临近晚霞时协助人们判断是否出发去拍摄。

![截图](img/screenshot1.png)

<span style="color: #ff5900">浅橙色</span>代表太阳落日前30分钟线，<span style="color: #ff2400">橙色</span>代表落日线，<span style="color: #cc0000">暗红色</span>代表太阳落日后30分钟线；<span style="color: #7553f2;">紫色点</span>代表您的位置，<span style="color: #17aa03;">绿色点</span>代表距离您200km处，<span style="color: #318bff;">蓝色点</span>代表距离您400km处。一般而言，<b><span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间有云，<span style="color: #17aa03;">绿色点</span>和<span style="color: #318bff;">蓝色点</span>之间没有云，说明有<span style="color: #ff2400">晚霞</span>。</b>如果<span style="color: #7553f2;">紫色点</span>和<span style="color: #17aa03;">绿色点</span>之间的云太厚了，那么无云空间需要离您更近才可能会烧。

### 未来目标

可以根据红外云图判断云底高度，从而更精准的计算太阳和云之间的关系。