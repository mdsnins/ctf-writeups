# Beginner's Web
*TSG CTF 2020 - Web 168*<br>
*Writeup by Payload as DefenitelyZer0*


## Problem

Why people tend to think things more difficult than it is?

## Converter Object

To get a flag, we have to call `flagConverter` function. There are three converter functions in problem, `flagConverter`, `base64Converter` and `scryptConverter`. Each of them are stored into object `converters`, with key `FLAG_(SESSION)`, `base64` and `scrypt`.

## Logic

As we think in challenge's name, server side's logic is simple. Server get two parameter `converter` and `input` using POST, and tries to call `converters[*converter*](*input*)`. However, there is a filter that checks `converter` contains literal `F`, `L`, `A` or `G`, we can't call it directly

## \_\_defineSetter\_\_

There are some native built-in methods in each javascript object such as `__defineGetter__`, `__defineSetter__`, and so on. And also we can access these method by looking up key. For eaxample `a.__defineGetter__` and `a["__defineGetter__"]` are same. Since server filters `/[FLAG]/` in `converter`, we can use `__defineSetter__` to trick the server

As its name, `__defineSetter__` defines a setter of the specific property of object. Let's see the problem's source code.

```js
converters[request.body.converter](request.body.input, (error, result) => {
    if (error) {
        reject(error);
    } else {
        resolve(result);
    }
});
```

So when we give `input` as `FLAG_***SESSION***` and `converter` as `__defineSetter__`, it will be excuted as

```js
converters["__defineSetter__"]("FLAG_***SESSION***", (error, result) => {
    if (error) {
        reject(error);
    } else {
        resolve(result);
    }
});
```

## Race it

We can override setter of `FLAG_***SESSION***` of `converters` object, so the only left thing is to make race condition. Just send two concurrent packets very fast, it will give an answer! 

Why? Because, early arrived packet already changed setter of `FLAG_***SESSION***`, and the other packet's request try to set `FLAG_***SESSION***` to `flagConverter`. It will raise an error and show `flagConverter.toString()` which contains a real flag

**`TSGCTF{Goo00o0o000o000ood_job!_you_are_rEAdy_7o_do_m0re_Web}`**

Now I'm ready :P