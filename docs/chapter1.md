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

不错不错，只是看了一眼就发现了这么重要的信息！
那么多盯着看一会儿，一定就能发现更多。
开始大胆假设，小心求证吧。

将所有的各种途径收集到的链接整理一下，可以发现都符合这样的格式：

    http://img4.tuwandata.com/{版本}/thumb/{格式}/{神秘代码1}/u/{神秘代码2}

版本的值有`v2`、`v3`和`v4`，格式的值有`jpg`和`all`。神秘代码1，根据前人的经验，在v2和v3的链接里面都是base64编码，v4目前不明。神秘代码2，在v2链接里面直接就是原图地址，v3和v4是一样的，具体格式仍然不明。

做几个小实验就能确定，链接中间的格式字段才是真正决定链接下载到的图片格式的。
如果把格式改成png，那么就可以下载到png格式的图片，改成webp也有效；有些链接的原图是GIF动图（比如这个：`http://img4.tuwandata.com/v4/thumb/all/31HqHAJsFbJI32877dr0AqlsJtsE24uYloVCl4d5WcO/u/GvFPJrTJvB9HmAlQA3r9XKIA6flvoq6yhfI0zlP7ae8datAtErRc4yacGHKjkcPv9.gif`），这样的链接里的格式字段都是all，如果改成jpg，就会获得jpg格式的静态图片。
而整个链接结尾的扩展名，也就是神秘代码2的扩展名，并不决定图片格式：如果是v2链接，修改了扩展名会返回404，而v3、v4链接修改了扩展名没有影响。
这也说明，v3、v4链接的神秘代码2，只有扩展名之前的部分才是有用的。

到目前为止都很简单，接下来就到了好好利用前人智慧的时间，对神秘代码1的base64编码下手吧！

---

[返回主页](../README.md)

[下一章](chapter2.md)

[1]: https://github.com/jrhu05/jerryWebSpider
[2]: https://sbcoder.cn/2019/05/13/tuwan_spider.html
[3]: https://github.com/jrhu05/jerryWebSpider/blob/master/db/my_spider.sql