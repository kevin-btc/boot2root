### Modify boot

#### Mount iso

#### open isolinux.cfg in isolinux folder

#### Find boot command kernel and append

```
/casper/vmlinuz file=/cdrom/preseed/custom.seed boot=casper initrd=/casper/initrd.gz "quiet splash --"
```

#### Launch the VM and flood the ESC key

It should show 
```
aborted. boot : 
```

#### Now write the boot command and replace "quiet splash --" by "init=/bin/bash" to launch bash on boot 

```
/casper/vmlinuz file=/cdrom/preseed/custom.seed boot=casper initrd=/casper/initrd.gz init=/bin/bash
```

#### You are now root !
