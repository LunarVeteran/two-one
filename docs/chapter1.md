# 首先当然是收集情报

兔玩君的这个API接口已经有 [很多][1] [前人们][2] 分析过了。
当时能拿到全图的都是v3或者更老的版本，而现在的接口已经是v4了，以前的方法已经失效，但是仍然有非常多有用的资料。

最重要的API入口是`https://api.tuwan.com/apps/Welfare/detail`。这是个JSONP GET接口，参数有很多，实际有用的就一个：`id={}`。
例如，请求这个地址`https://api.tuwan.com/apps/Welfare/detail?id=888`，[就能获得这样的数据（调整了格式并对中文进行了解码）](snippets/detail_888.js)。

多试几次就会发现：`id`为正整数的时候，要么会返回某个特定图包的信息，要么会报错；`id`为0的时候，则会在几个图包之中随机返回一个。

在接口返回的数据中有很多图片链接，封面图、预览图、缩略图等等，这些链接都是v2或者v4。
而在[前人收集的数据][3]中，能够找到很多v3的链接。
整合多方数据，很容易就能找到同一张图片的多个链接，就像这样：

* 封面图(624x935像素，97425字节)：`http://img4.tuwandata.com/v2/thumb/jpg/YTczZiw2MjQsMCw5LDMsMSwtMSxOT05FLCwsOTA=/u/res.tuwan.com/zipgoods/20180616/581914b801ceecf8512682bc949ff21e.jpg`

* 历史数据中的v3链接(1242x1861像素，361023字节)：`http://img4.tuwandata.com/v3/thumb/jpg/YTczZiwwLDAsOSwzLDEsLTEsTk9ORSwsLDkw/u/GLDM9lMIBglnFv7YKftLBGT3cJwG79ZiLPK0Vx1fuyPdpW6vU1RBPbt8AhwUPEuzA3p6UqQQhlcHxxrRyqDAbzrGCWDUslLn8FJikUDO4hiB.jpg`

* 预览图(1242x1861像素，361023字节)：`http://img4.tuwandata.com/v4/thumb/jpg/EuHtdsj20mziggepjNLyK8JdNGLpsorR2ajsZqq54vw/u/GLDM9lMIBglnFv7YKftLBGT3cJwG79ZiLPK0Vx1fuyPdpW6vU1RBPbt8AhwUPEuzA3p6UqQQhlcHxxrRyqDAbzrGCWDUslLn8FJikUDO4hiB.jpg`

* 缩略图(158x158像素，6194字节)：`http://img4.tuwandata.com/v4/thumb/jpg/W87uG0uTZJPXjLMSnLxcm13VgLDEMIcaDWw8JH34P3Q/u/GLDM9lMIBglnFv7YKftLBGT3cJwG79ZiLPK0Vx1fuyPdpW6vU1RBPbt8AhwUPEuzA3p6UqQQhlcHxxrRyqDAbzrGCWDUslLn8FJikUDO4hiB.jpg`

嗯？这个v2地址，好像有什么露出来了……？

* 原图(1242x1861像素，1394281字节)：`http://res.tuwan.com/zipgoods/20180616/581914b801ceecf8512682bc949ff21e.jpg`

_未完待续……_

---

[返回主页](../README.md)

下一章：敬请期待

[1]: https://github.com/jrhu05/jerryWebSpider
[2]: https://sbcoder.cn/2019/05/13/tuwan_spider.html
[3]: https://github.com/jrhu05/jerryWebSpider/blob/master/db/my_spider.sql