# Wallbreaker Easy
*0CTF/TCTF 2019 Web 157*<br>
*Writeup by Payload, KAIST GoN*


## Problem

Imagick is a awesome library for hackers to break \`disable_functions\`.

So I installed php-imagick in the server, opened a \`backdoor\` for you.

Let's try to execute \`/readflag\` to get the flag.

Open basedir: /var/www/html:/tmp/{{some hash}}

Hint: eval($_POST["backdoor"]);


## Look up

As problem says, we have to bypass `disable_functions` and get a code execution to run `/readflag`

It may be related `LD_PRELOAD injection` like [Insomnihack l33t-hoster](../../Insomnihack\ 2019/l33t-hoster/) or any GhostScript vulnerabilites(like TokyoWesterns CTF Slack Emoji Converter / SECCON GhostKingdom) . So let's check same strategy is available first. Send backdoor=phpinfo(); will tell us what functions are disabled.

Before start, method 'POST' is bothering me. So I attached following HTML.

```html
<form method="POST">
    <textarea name="backdoor"></textarea>
    <button type="submit">Send!</button>
</form>
```

Below is `disable_functions` in phpinfo().
![Disabled Functions](https://i.imgur.com/Ub6oTB4.png)

`pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,system,exec,shell_exec,popen,proc_open,passthru,symlink,link,syslog,imap_open,ld,mail`


All system functions(`shell_exec`, `system`, ...) are disabled, and both `mail()` and `imap_open()` which are famous disable_functions bypass methods are also disabled. However, as we guessed first, `putenv()` which make `LD_PRELOAD injection` available is not disabled. So, it'll be key!

In addition, functions for file read/write (`file_put_contents`, `file_get_contents`, ...) are not blocked, we can upload our arbitrary files.

## Imagick executes binaries

Problem said Imagick is installed, and we also can check the Imagick in phpinfo.
![Imagick](https://i.imgur.com/n5c5Gso.png)

Installed Imagick has latest version which already patched GhostScript vulnerability. Thus, I thought it's not about GhostScript RCE vulnerabilities.

To make `LD_PRELOAD injection`, php must run binary via `execve` after we call `putenv()`. I checked various Imagicks features using `strace`. 

I tested opening various type using Imagicks. Image formats(`.jpg`, `.png`, ...) are processed in PHP, not executes any other binaries. However, when user tries to open non-image formats(`.pdf`, `.ps`,`.eps`, ...) in Imagick, it calls `/usr/bin/gs` to process the files. Thus, these will be trigger our injected library.

![Not Authorized](https://i.imgur.com/qGa0rIK.jpg)
However, `.pdf` and other ghostscript formats are disabled as default, it doesn't run the `gs`. So, we have to fake it.

![Wow!](https://i.imgur.com/H4ktOdM.png)
After some experiments, valid `.eps` file isn't authorized and don't run `gs`. But, invalid `.eps` file doesn't thorw the error. Also, strace shows it runs `/usr/bin/gs` normally.
![Wow!!](https://i.imgur.com/xwf9LrL.png)

Great, we found a vulnerability.

## Exploit

As [I did in past](../../Insomnihack\ 2019/l33t-hoster/), it's easy to build a injecting library. I made a library to open reverse shell by compiling my [bypass.c](./bypass.c). To run our library, we have to 3 steps.

1. Listening reverse shell
2. Upload `bypass.so`, `bypass.eps`(invalid eps)
3. Open bypass.eps using Imagick
 
I made up the python script to do, finally I could got a reverse shell.
[run.py](./run.py)

![I got a shell](https://i.imgur.com/OoCOoqM.png)

**`flag{PUTENVANDIMAGICKAREGOODFRIENDS}`**
