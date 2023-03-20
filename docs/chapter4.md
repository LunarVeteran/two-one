# 黒いレースの境界線

在第二章中，我们推测神秘代码2是以16字节（128bit）为block size进行加密的数据，在此之上又使用了62进制编码，把每一位0~61的数字用 `[0-9a-zA-Z]` 的字符来表示。

但是，我们并不知道每一个字符究竟对应的是几，也就无法把这种编码恢复成密文。接下来的首要任务，就是破解这个对应关系，重建62进制译码表。

设想一下，如何将普通的二进制数据编码成62进制呢？
最简单的办法应该是，将原始数据直接当成一个非常大的整数，然后将其转为62进制，最后再将每一位数字转换成一个字符。

我们先假设这两步转换都是Big endian，也就是左边的字符/数字代表高位，右边的字符/数字代表低位。
就以 `b'hello world!'` 为例：把这一串字节看作一个256进制数字 `[104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33]` ，转换成其他进制就是：

$$
\begin{aligned}
& {[104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33]}_{256} \\
= & 32309054545037006034346730529_{10} \\
= & {[42, 1, 12, 13, 55, 25, 60, 43, 22, 2, 58, 49, 55, 29, 54, 1]}_{62}
\end{aligned}
$$

神秘代码2的长度绝大多数都是108个字符，而108位的62进制数字最大是 $108 \times \log_2 62 = 643.0532$ 比特，刚好放得下80字节。
如果原始明文数据形如 `res.tuwan.com/zipgoods/20180616/581914b801ceecf8512682bc949ff21e.jpg` ，长度为68字节，经过128比特的padding之后会被填充到80字节。

明文固定的开头 `res.tuwan.com/zipgoods/` 长度为23字节，经过128bit的block cipher加密后（不使用随机IV），会造成密文开头的16字节都是相同的。
虽然我们不知道开头的16字节密文具体是什么，但是可以确定，整段密文的值一定在 `[开头密文]000000...0000` 与 `[开头密文]ffffff...ffff` 之间，后面不确定的部分长度为64字节。
这样的密文，在经过62进制编码之后会变成什么样呢？

令

$$
\begin{aligned}
a &= {[ \overbrace{开头密文}^{16位}, \overbrace{0, 0, 0, \cdots, 0, 0}^{64位} ]}_{256} \\
b &= {[ \overbrace{开头密文}^{16位}, \overbrace{255, 255, 255, \cdots, 255, 255}^{64位} ]}_{256}
\end{aligned}
$$

再令

$$
\begin{aligned}
c &= b - a \\
&= {[ \overbrace{255, 255, 255, \cdots, 255, 255}^{64位} ]}_{256} \\
&= {256}^{64} - 1 \\
&= {[ \overbrace{59, 27, 9, \cdots, 18, 3}^{86位} ]}_{62}
\end{aligned}
$$

则对于任意一条密文 $x$ ，都有 $a \le x \le b$ 。
再再令 $y = x - a$ ，则有$0 \le y \le c$ 。
我们写一个小学二年级就学过的 $a + y = x$ 的竖式出来：

$$
\begin{array}{rrrrrrrrrrrr}
& [ & a_{107}, & a_{106}, & \cdots, & a_{87}, & a_{86}, & a_{85}, & a_{84}, & \cdots, & a_{1}, & a_{0} & ]_{62}\\
+ & [ & & & & & & y_{85}, & y_{84}, & \cdots, & y_{1}, & y_{0} & ]_{62} \\ \hline
= & [ & x_{107}, & x_{106}, & \cdots, & x_{87}, & x_{86}, & x_{85}, & x_{84}, & \cdots, & x_{1}, & x_{0} & ]_{62}
\end{array}
$$

就很容易看出，虽然我们并不知道密文 $x$ 的值，但是它的左侧22位 $[x_{107}, x_{106}, \cdots, x_{87}, x_{86}]_{62}$ 只有两种可能性：

1. 如果在 $a_{85} + y_{85}$ 这一步没有进位的话，那么 $[x_{107}, x_{106}, \cdots, x_{87}, x_{86}]_{62} = [a_{107}, a_{106}, \cdots, a_{87}, a_{86}]_{62}$

1. 如果在 $a_{85} + y_{85}$ 这一步进了位的话，那么 $[x_{107}, x_{106}, \cdots, x_{87}, x_{86}]_{62} = [a_{107}, a_{106}, \cdots, a_{87}, a_{86}]_{62} + 1$

那么，实际情况如何呢？
在所有108字符的神秘代码2，开头的字符只有两种形式：`GLDM9lMIBglnFv7YKftLBG`和`GLDM9lMIBglnFv7YKftLBu`。
头21个字符完全固定，第22个字符只有两种可能性。

至此，我们获得了一条重要情报：在62进制译码表中， `G` 和 `u` 是两个相邻的数字。

_未完待续……_

---

[返回主页](../README.md)

[上一章](chapter3.md)