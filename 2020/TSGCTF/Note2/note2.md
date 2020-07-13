# Note2
*TSG CTF 2020 - Web 428*<br>
*Writeup by Payload as DefenitelyZer0*


## Problem

Sorry but we found unintended solution for the problem "Note". We fixed it now. FLAG format and attachments are same as "Note".

## Solution of previous Note

Our team solved proble Note using [time based regex inject (by posix, great teammate)](https://blog.p6.is/time-based-regex-injection/). The write-up for original Note problem is [here](https://gist.github.com/po6ix/f3c013d974c6003a8dbc573c887602ae) (also written by posix)

## New Regex Payload

The difference between Note and Note2 is regex restriction. A following line is added in Note2
```js
const re = new RegExp(this.search.replace(/[{}()+*]/g, ''));
```
We made a DOS using abnormal regex group like `^TSGCTF.[A-Z](((.*)*)*)`, but now we can't use any of parenthesis and asterisk. 

After a sweat dream, we checked following regex pattern also be able to cause DOS. 

```re
^TSGCTF.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?!
```

This regex pattern doesn't use any of blocked chars, we can do original Note's things again.

One more thing we did is a extracting almost-last characters. As increasing front match length, this oracle's precision is decreasing. Thus we enhanced the regex to match only some middle parts of flag

```re
.?.?.?.?.?.?.?.?.?OPW5E729[0-9].?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.? ...(keep going)
```

Since I extracted some of flags with my hands, please check [posix's previous writeup](https://gist.github.com/po6ix/f3c013d974c6003a8dbc573c887602ae) or [arang's repository](https://github.com/JaewookYou/ctf-writeups/tree/master/2020TSGCTF/note2)! 

**`TSGCTF{5JFJMWOPOPW5E729}`**