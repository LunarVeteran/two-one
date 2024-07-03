# 先知不削能玩？

现在我们手上有了大量的疑似使用AES128 CBC加密的密文。
我们希望能拿到它们对应的明文。

有过竞赛或者实战经验的人应该马上就能想到padding oracle攻击：
只要我们能够通过某种方法分辨一个密文是否有合法的padding，
就可以一个bit一个bit地把明文反推出来。

那么，去寻找我们的先知（oracle）吧。

为了向API提交任意密文，
我们需要将密文用Base62进行编码，
作为神秘代码2，组装成一个v3 URL。
因为不知道对应的明文是什么，
神秘代码1中的那个哈希只能暴力全都试一遍。
当哈希不正确的时候，API返回404；
而撞到正确的哈希时，API就可能会返回有用的信息了。

实际拿一些密文尝试一下，
就会发现哈希正确时，
API经常会返回HTTP状态码424，
此时的响应body是XML编码的错误信息。

比如，时不时会出现这样的信息：

```
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>MirrorFailed</Code>
  <Message>Error status : 0 from mirror host, should return 200 OK.</Message>
  <RequestId>************************</RequestId>
  <HostId>tuwanimg.oss-cn-qingdao.aliyuncs.com</HostId>
</Error>
```

看起来是因为并发太高，后端出了点问题，这个信息并不是特别有用。

还有这样的：

```
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>MirrorFailed</Code>
  <Message>Host:a73f,624,0,9,3,1,-1,NONE,,,90, contains some illegal characters.</Message>
  <RequestId>************************</RequestId>
  <HostId>tuwanimg.oss-cn-qingdao.aliyuncs.com</HostId>
</Error>
```

看起来是把密文解密了之后，
发现明文中的内容不是一个合法的域名，
于是报的错，
还非常亲切地把这个非法域名的内容写在了错误信息里面。

嗯，挺有用的。
padding oracle还没找到，却找到一个decryption oracle，明文直接给出来了。

这个oracle也不是全能的，
通过它解密出来的内容有很多限制。
比如泄露的明文中有很多字符被替换成了`%ef%bf%bd`啦，
只有域名部分会泄露所以斜杠之后的内容都看不到啦，
超过某个长度就没用啦啦，等等等等。
但是，因为密文是CBC加密的，
我们也有很多操纵明文的方法。
这里就不展开讲了，但是利用这个先知，可以非常轻松地把每一个v4链接的神秘代码2都解成明文。

_未完待续……_

---

[返回主页](../README.md)

[上一章](chapter4.md)