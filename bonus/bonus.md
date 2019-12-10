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

#### Now write the modified command to launch bash on boot and replace "quiet splash --" by init=/bin/bash

```
/casper/vmlinuz file=/cdrom/preseed/custom.seed boot=casper initrd=/casper/initrd.gz init=/bin/bash
```

#### You are now root !
