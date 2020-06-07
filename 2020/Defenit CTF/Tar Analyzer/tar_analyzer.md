# Tar Analyzer
*Defenit CTF 2020 - Web ???*<br>
*Writeup by Payload as TryToEatSushi*


## Problem

Our developer built simple web server for analyzing tar file and extracting online. He said server is super safe. Is it?

## Unintended way

It's defenitely solved by unintended way.
<h1>SYMLINK!!!!!!!!!!!!</h1>

## Exploitation
1. Make a symlink that points `/flag.txt`
2. Archive it to `.tar`
3. Upload and read.

**`Defenit{R4ce_C0nd1710N_74r_5L1P_w17H_Y4ML_Rce!}`**
