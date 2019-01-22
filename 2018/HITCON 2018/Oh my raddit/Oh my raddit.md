# Oh my raddit
*HITCON CTF 2018 Web 262*<br>
*Writeup by Payload, KAIST GoN*


## Problem

This is based on a real world case. If you get the crypto point, it can be sovled in 10 minutes!

[http://13.115.255.46](13.115.255.46)

## Look up

In main page, we can do 4 things.

* Read hint (/static/hint.py)
* Change numbers of topics to be shown
* Read topic (redirect to outside)
* Download some .pdf file

Every link except the hint is in format `?s={encrypted_message}`<br>Also hint.py says `assert ENCRYPTON_KEY.islower()`


## Guess it!

First, let's see second feature of the site that I mentioned. Drop-down list trigger the below javascript.

```javascript
function change(t){
    var limit = t.value;
    if (limit == 10) {
        location.href = '?s=06e77f2958b65ffd3ca92540eb2d0a42';
    } else if (limit == 100) {
        location.href = '?s=06e77f2958b65ffd2c0f7629b9e19627';
    } else {
        location.href = '/';
    }
}
```

We can see two encrypted blocks which have 32 length in hex-string, which means 16byte block. And we can also see common part `06e77f2958b65ffd` and the other parts `3ca92540eb2d0a42` and `2c0f7629b9e19627`.<br>I tried to search `3ca92540eb2d0a42` in whole page source, then it matched 18 times in site. In addition, I found one more interesting fact that `3ca92540eb2d0a42` is only located at the end of message block.

In conclusion, I found two interesting facts about encrypted meesage.

* `3ca92540eb2d0a42` appears many times! 
* `3ca92540eb2d0a42` only located at the end of meesage block which contains padding!

So I can say three things about this encryption

* Message block size is 8bytes(64bit)
* It uses ECB mode.
* `3ca92540eb2d0a42` is the result of `encrypt('\x08' * 8)`


## Find a Key
The only thing we know is `encrypt('\x08' * 8) == 3ca92540eb2d0a42`. Also I can guess the encryption method may be DES by its block size. So I tried a brute-force attack using `hashcat`

Since we know the encryption key only has lower case alphabets, `hashcat` gave me a cracked key `ldgnnaro` rapidly.

Wow! Then flag is `hitcon{ldgnnaro}`!

## Find a *REAL* Key
Oops, I can't auth the flag `hitcon{ldgnnaro}`. What???? I tried to decrypt a lot of message block in page using key `ldgnnaro` and it successfully decrypted! Then, what's the problem?

I calmed down and thought about DES once again. Because of DES algorithm, it can have multiple keys to encryption and decryption. Kindly, orange, the author of this problem, wrote the one more thing in page.

*P.S. If you fail in submitting the flag and want to argue with author, read the source first*

This page has download feature, so maybe we can download arbitrary file in server using this featrue. One of the download links decrypted as 
`m=d&f=uploads/70c97cc1-079f-4d01-8798-f36925ec1fd7.pdf`. Got it!

Now we can download arbitrary file! First, I downloaded /proc/self/cmdline using `m=d&f=/proc/self/cmdline`. It says the main module of this website is `app.py`. Then I tried to download app.py using `m=d&f=app.py`. And it successfully downloaded and the few lines at beginning of app.py shows 

```python
# coding: UTF-8
import os
import web
import urllib
import urlparse
from Crypto.Cipher import DES

web.config.debug = False
ENCRPYTION_KEY = 'megnnaro'
```

The **REAL** flag is *`hitcon{megnnaro}`*

