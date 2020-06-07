#Defenit CTF 2020 - Bad Tumblers
#By Payload as ToEatSushi

import requests
import json
from time import sleep
API_KEY = "API_KEY"
headers = {"User-Agent": "Mozilla/5.0"}

def scan_transaction(addr):
    target = "http://api-ropsten.etherscan.io/api?module=account&action=txlist&address=%s&startblock=0&endblock=99999999&sort=asc&apikey=%s" % (addr, API_KEY)
    resp = requests.get(target, headers = headers)
    sleep(0.2)
    t = json.loads(resp.text)
    return [(x["hash"], x["from"], x["to"]) for x in t["result"] if int(x["timeStamp"]) >= 1590900000 and int(x["timeStamp"]) <= 1591000000]


#initial scan
x1 = scan_transaction("0x5149aa7ef0d343e785663a87cc16b7e38f7029b2") #addrA
x2 = scan_transaction("0x2Fd3F2701ad9654c1Dd15EE16C5dB29eBBc80Ddf") #addrC

from collections import OrderedDict
cand_addr = OrderedDict()
trans = dict()
for (h, _, i) in x1:
    trans[h] = True
    if i in cand_addr:
        cand_addr[i] += 1
    else:
        cand_addr[i] = 1

for (h, i, _) in x2:
    trans[h] = True
    if i in cand_addr:
        cand_addr[i] += 1
    else:
        cand_addr[i] = 1

print("Initialized : %s", cand_addr.keys())

i = 0
while i != len(cand_addr):
    cur_cand = list(cand_addr.keys())[i]
    transactions = scan_transaction(cur_cand)
    print("%d scanning: %s" % (i, cur_cand))
    toTumble = False
    fromTumble = False
    dbg1, dbg2= 0, 0
    for t in transactions:
        _hash, _from, _to = t
        if _hash in trans: #already processed
            continue
        trans[_hash] = True
        dbg1 += 1
        if _from == cur_cand:
            if _to in cand_addr:
                cand_addr[_to] += 1
                toTumble = True
            else:
                cand_addr[_to] = 1
                dbg2 += 1
        elif _to == cur_cand:
            if _from in cand_addr:
                cand_addr[_from] += 1
                fromTumble = True
            else:
                cand_addr[_from] = 1
                dbg2 += 1

    print("%d hashed added, %d new address added. Total addr : %d" % (dbg1, dbg2, len(cand_addr.keys())))
    if toTumble and (not fromTumble):
        print("\n\n\nFound : %s\n\n\n" % cur_cand)
		break
    i += 1
