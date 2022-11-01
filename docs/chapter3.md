# 色图是第一生产力

Q: 我们的目标是什么？

A: 看图！

Q: 我们手上有什么？

A: 从API上扒下来的2000多个图包的所有缩略图URL！

Q: 我们想要得到什么？

A: 这些缩略图URL所对应的全尺寸图片URL！

Q: 怎样才能得到呢？

A: 对于v2的链接，可以直接拿到后半段神秘代码2的原始地址！
对于v2和v3链接，可以修改神秘代码1来获取全尺寸图片！
对于v4链接，呃……可以改写成v3链接，然后暴力破解神秘代码1里面的4位哈希值！

Q: 暴力破解v4链接太不优雅了，如果对每个链接都来爆破，这得花多长时间啊。有更好的办法吗？

当然是有的。

我们已经知道，v3链接中的神秘代码1使用base64编码。
我们推测，v4链接中的神秘代码很可能用了某种加密+“base62”编码，并且这个加密的特性是，同一段明文，多次加密获得的都是相同的密文。
所有的缩略图URL中神秘代码1的明文应该都是`xxxx,158,158,9,3,1,-1,NONE,,,90`的形式，只有第一个字段中的4个字符不同，其他部分都是不变的。
因此，如果两个URL中的神秘代码2对应的哈希值相同，那么在v4缩略图链接中的神秘代码1也应该是相同的，反之亦然。
既然哈希的长度只有4个字符，那么应该存在不少的碰撞。
事实果真如此吗？

还用这张已经看了好多次的图片为例：

v4缩略图URL是：
`http://img4.tuwandata.com/v4/thumb/jpg/W87uG0uTZJPXjLMSnLxcm13VgLDEMIcaDWw8JH34P3Q/u/GLDM9lMIBglnFv7YKftLBGT3cJwG79ZiLPK0Vx1fuyPdpW6vU1RBPbt8AhwUPEuzA3p6UqQQhlcHxxrRyqDAbzrGCWDUslLn8FJikUDO4hiB.jpg`，
v3全尺寸图片的URL是：
`http://img4.tuwandata.com/v3/thumb/jpg/YTczZiwwLDAsOSwzLDEsLTEsTk9ORSwsLDkw/u/GLDM9lMIBglnFv7YKftLBGT3cJwG79ZiLPK0Vx1fuyPdpW6vU1RBPbt8AhwUPEuzA3p6UqQQhlcHxxrRyqDAbzrGCWDUslLn8FJikUDO4hiB.jpg`。
将v3链接中的神秘代码1进行解码，获得的是`a73f,0,0,9,3,1,-1,NONE,,,90`。

在收集到的URL中翻找一下，可以找到另一条v4缩略图链接，其中的神秘代码1是相同的：
`http://img4.tuwandata.com/v4/thumb/jpg/W87uG0uTZJPXjLMSnLxcm13VgLDEMIcaDWw8JH34P3Q/u/GLDM9lMIBglnFv7YKftLBuhcEgbuyBACEFWQ67A3lqO4AllLWiv1IxLnoaYJh99wadnByaLx31KGBJdfaosqHg5GTpNH4GCvAtNVDWneGEKJ.jpg`

使用前一个v3链接中的神秘代码1，和新链接中的神秘代码2，直接组装一个v3链接：
`http://img4.tuwandata.com/v3/thumb/jpg/YTczZiwwLDAsOSwzLDEsLTEsTk9ORSwsLDkw/u/GLDM9lMIBglnFv7YKftLBuhcEgbuyBACEFWQ67A3lqO4AllLWiv1IxLnoaYJh99wadnByaLx31KGBJdfaosqHg5GTpNH4GCvAtNVDWneGEKJ.jpg`

成功访问到了新链接对应的全尺寸图片，证实了我们的猜想。

v4缩略图链接中的每一个神秘代码1，对应了一个独特的哈希值，只要知道这个哈希值，就能获取全尺寸图片。`W87uG0uTZJPXjLMSnLxcm13VgLDEMIcaDWw8JH34P3Q` --> `a73f`

那么，只要建立一个神秘代码1-->哈希值的映射表，不就可以随便看图，不需要对每个v4链接进行爆破了吗？

之前收集的各种来源的URL派上了用场。
如果知道某个v4缩略图链接指向的图片和v2、v3链接是同一张，就可以在映射表里填上一行。

剩下那些没有对应v2、v3的v4链接，仍然可以使用爆破的方式。
不过，暴力破解的范围从65536个可能的哈希值，缩小到了*尚未在映射表里出现过的哈希值*。
每增加一条记录，需要爆破的空间就小一点。
优雅，实在是太优雅了！

想必各位已经等不及了，那就快点端上来罢：

[白嫖兔玩君](https://lunarveteran.github.io/baipiao/index.html)

这个网页通过JavaScript载入了映射表，于是可以直接调用兔玩君的API，使用缩略图URL来生成全尺寸图片的URL，从而浏览全部的大图。

---

另外，为了节省大家的时间，同时让服务器少受一些摧残，这里也放出完整的映射表。
虽然稍微加了那么一点点密，但是如果你读到了这里，一定有办法找到密钥的！
[`decrypt_magic_code_1.py`](../decrypt_magic_code_1.py)

图也看完了，现在只剩下学术性的问题了：这些神秘代码究竟是用了什么编码和加密方式，有没有办法解密呢？

_敬请期待……_

---

[返回主页](../README.md)

[上一章](chapter2.md)