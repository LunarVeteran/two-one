# 黒いレースの境界線

在第二章中，我们推测神秘代码2是以16字节（128bit）为block size进行加密的数据，在此之上又使用了62进制编码，把每一位0~61的数字用 `[0-9a-zA-Z]` 的字符来表示。

但是，我们并不知道每一个字符究竟对应的是几，也就无法把这种编码恢复成密文。接下来的首要任务，就是破解这个对应关系，重建62进制译码表。

设想一下，如何将普通的二进制数据编码成62进制呢？
最简单的办法应该是，将原始数据直接当成一个非常大的整数，然后将其转为62进制，最后再将每一位数字转换成一个字符。

我们先假设这两步转换都是Big endian，也就是左边的字符/数字代表高位，右边的字符/数字代表低位。
就以 `b'hello world!'` 为例：把这一串字节看作一个256进制数字 `[104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33]` ，转换成其他进制就是：

```math
\begin{aligned}
& {[104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33]}_{256} \\
= & 32309054545037006034346730529_{10} \\
= & {[42, 1, 12, 13, 55, 25, 60, 43, 22, 2, 58, 49, 55, 29, 54, 1]}_{62}
\end{aligned}
```

神秘代码2的长度绝大多数都是108个字符，而108位的62进制数字最大是 $`108 \times \log_2 62 = 643.0532`$ 比特，刚好放得下80字节。
如果原始明文数据形如 `res.tuwan.com/zipgoods/20180616/581914b801ceecf8512682bc949ff21e.jpg` ，长度为68字节，经过128比特的padding之后会被填充到80字节。

明文固定的开头 `res.tuwan.com/zipgoods/` 长度为23字节，经过128bit的block cipher加密后（不使用随机IV），会造成密文开头的16字节都是相同的。
虽然我们不知道开头的16字节密文具体是什么，但是可以确定，整段密文的值一定在 `[开头密文]000000...0000` 与 `[开头密文]ffffff...ffff` 之间，后面不确定的部分长度为64字节。
这样的密文，在经过62进制编码之后会变成什么样呢？

令

```math
\begin{aligned}
a &= {[ \overbrace{\text{ciphertext}}^{16\text{位}}, \overbrace{0, 0, 0, \cdots, 0, 0}^{64\text{位}} ]}_{256} \\
b &= {[ \overbrace{\text{ciphertext}}^{16\text{位}}, \overbrace{255, 255, 255, \cdots, 255, 255}^{64\text{位}} ]}_{256}
\end{aligned}
```

再令

```math
\begin{aligned}
c &= b - a \\
&= {[ \overbrace{255, 255, 255, \cdots, 255, 255}^{64\text{位}} ]}_{256} \\
&= {256}^{64} - 1 \\
&= {[ \overbrace{59, 27, 9, \cdots, 18, 3}^{86\text{位}} ]}_{62}
\end{aligned}
```

则对于任意一条密文 $x$ ，都有 $`a \le x \le b`$ 。
再再令 $`y = x - a`$ ，则有 $`0 \le y \le c`$ 。
我们写一个小学二年级就学过的 $`a + y = x`$ 的竖式出来：

```math
\begin{array}{}
  & [ & a_{107}, & a_{106}, & \cdots, & a_{87}, & a_{86}, & a_{85}, & a_{84}, & \cdots, & a_{1}, & a_{0} & ]_{62} \\
 +& [ &          &          &         &         &         & y_{85}, & y_{84}, & \cdots, & y_{1}, & y_{0} & ]_{62} \\ \hline
 =& [ & x_{107}, & x_{106}, & \cdots, & x_{87}, & x_{86}, & x_{85}, & x_{84}, & \cdots, & x_{1}, & x_{0} & ]_{62}
\end{array}
```

就很容易看出，虽然我们并不知道密文 $`x`$ 的值，但是它的左侧22位 $`[x_{107}, x_{106}, \cdots, x_{87}, x_{86}]_{62}`$ 只有两种可能性：

```math
[x_{107}, x_{106}, \cdots, x_{87}, x_{86}]_{62} =
\begin{cases}
[a_{107}, a_{106}, \cdots, a_{87}, a_{86}]_{62} & a_{85} + y_{85} \text{没有进位} \\
[a_{107}, a_{106}, \cdots, a_{87}, a_{86}]_{62} + 1 & a_{85} + y_{85} \text{有进位}
\end{cases}
```

那么，实际情况如何呢？
在所有108字符的神秘代码2，开头的字符只有两种形式：`GLDM9lMIBglnFv7YKftLBG`和`GLDM9lMIBglnFv7YKftLBu`。
头21个字符完全固定，第22个字符只有两种可能性，与预测完全符合。
至此，我们不仅确认了猜想，还获得了一条重要情报：
在62进制译码表中， `G` 和 `u` 是两个相邻的数字。

如此大费周章，仅仅确定了62个字符中的2个的相对关系？
我知道你很急，但是你别急。

回到原始的明文数据，我们知道明文都是形如 `res.tuwan.com/zipgoods/20180616/581914b801ceecf8512682bc949ff21e.jpg` 这样的字符串。
在这种数据中，多次重复出现的前缀并不限于 `res.tuwan.com/zipgoods/` 的部分，
紧跟在后面的日期也常常是重复的。
而且 `res.tuwan.com/zipgoods/20180616/` 的长度是32字节，刚好够到了下一个block的边界。
也就是说，对于一堆32字节前缀相同的明文，对应密文的32字节前缀也是相同的。

对于某一个给定的32字节密文前缀，把上面的分析重复一遍：令

```math
\begin{aligned}
a &= {[ \overbrace{\text{ciphertext}}^{32\text{位}}, \overbrace{0, 0, 0, \cdots, 0, 0}^{48\text{位}} ]}_{256} \\
b &= {[ \overbrace{\text{ciphertext}}^{32\text{位}}, \overbrace{255, 255, 255, \cdots, 255, 255}^{48\text{位}} ]}_{256} \\
c &= b - a \\
&= {[ \overbrace{255, 255, 255, \cdots, 255, 255}^{32\text{位}} ]}_{256} \\
&= {256}^{32} - 1 \\
&= {[ \overbrace{7, 38, 60, \cdots, 50, 15}^{65\text{位}} ]}_{62}
\end{aligned}
```

令 $`x`$ 为任意（有相同的32字节前缀的）密文，令 $`y = x - a`$ ，写出 $`a + y`$ 的竖式：

```math
\begin{array}{}
  & [ & a_{107}, & a_{106}, & \cdots, & a_{66}, & a_{65}, & a_{64}, & a_{63}, & \cdots, & a_{1}, & a_{0} & ]_{62} \\
 +& [ &          &          &         &         &         & y_{64}, & y_{63}, & \cdots, & y_{1}, & y_{0} & ]_{62} \\ \hline
 =& [ & x_{107}, & x_{106}, & \cdots, & x_{66}, & x_{65}, & x_{64}, & x_{63}, & \cdots, & x_{1}, & x_{0} & ]_{62}
\end{array}
```

我们可以发现一件非常幸运的事情：因为

```math
[y_{64}]_{62} \le [c_{64}]_{62} = [7]_{62}
```

在算上进位的影响之后， $x$ 的前缀只有9种可能：

```math
[a_{107}, a_{106}, \cdots, a_{65}, a_{64}]_{62} \le
[x_{107}, x_{106}, \cdots, x_{65}, x_{64}]_{62} \le
[a_{107}, a_{106}, \cdots, a_{65}, a_{64}]_{62} + 8
```

马上来验证一下。

在所有的神秘代码2里面，随意筛选一组开头 $`107 - 64 + 1 = 44`$ 个字符全都相同的数据：
开头是 `GLDM9lMIBglnFv7YKftLBuvWxqGKDxowQO7ssMiutjM` 的值，下一位字符有 `C,G,U,V,h,p,u,x,y` ，一共9种可能性。
那么，这9个字符，在62进制译码表中一定属于连续的9个数字。

再挑一组。开头 `GLDM9lMIBglnFv7YKftLBuhOk3T8sN61z8RbVnNBpWo` ，下一位 `C,G,V,h,p,q,u,x,y` 。
这9个字符跟上一组的9个，有8个字符是重叠的，多了一个 `q` ，少了一个 `U` 。
也就是说，重叠的 `C,G,V,h,p,u,x,y` 是连续的8个数字，而 `q` 和 `U` 分别紧挨着这8个数字的两端。

作为奖励内容，再来看一组相同的前缀吧：
开头是 `GLDM9lMIBglnFv7YKftLBG1wOAboMKgYVOXlXO1b8` （注意，这个前缀的长度仅有41字符），后面跟着的3个字符有 `Rz7,Rze,Rzf,Rzg,Rzr,Rzs,Rzt,Rzz,SUU` 。
这是一次进位！
它告诉我们， `z` 和 `U` 两个字符分别对应0和61（虽然还不知道哪个是哪个）。

就像这样，一组一组地收集译码表中连续的数字，玩一玩拼图游戏，很轻松地就可以把62个字符的顺序理清楚。
但是拼图没有办法告诉我们哪一头是0，哪一头是61，这可怎么办呢？

很简单，试一下就知道了。
所有长度为108字符的神秘代码2，使用译码表转成62进制整数，必须小于 $`256^{80} = 2^{640}`$ 。
如果这个条件被打破了，说明译码表错了。
拿着我们确定的62个字符的顺序，正着反着都试一次，就可以把错误的选项排除掉了。

相信聪明的你此时一定已经成功破解了译码表了吧？
来对个答案如何？

    >>> BASE62_ALPHABET = '...'  # change me
    >>> import hashlib
    >>> hashlib.sha256(BASE62_ALPHABET.encode('ascii')).hexdigest()
    'e6a035dfc00549ae352b0f7ee0f9dd1f0a375a8bf05b8f83664c61e5892253fe'

解决了62进制编码，下一步要研究的就是（疑似为AES CBC的）加密算法了。

## 附加题

1. 从一开始，我们就假设二进制数据到整数和整数到62进制的转换都是Big endian的。
如果这两步中实际上存在Little endian的转换，会发生什么呢？

2. 用现在获得的信息，我们已经可以对所有的神秘代码2进行62进制转换，获得原始的密文数据了。
但是如果试图去转换神秘代码1，就会发现一个问题：
有的62进制数的最高位（最左侧的数字）是0。
在一个数字的最高位加上0，自然是不会让数字的值有所变化的。
那加上0的意义何在呢？

   （提示：为了转换的唯一性考虑，从一串字节数据转换到62进制编码数据的这个函数，必须是一个双射（bijection）。）

---

[返回主页](../README.md)

[上一章](chapter3.md)

[下一章](chapter5.md)
