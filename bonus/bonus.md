Bonus

### Modify boot

#### Mount iso

#### Edit isolinux.cfg in isolinux folder

#### Concatenate kernel and append

```
/casper/vmlinuz file=/cdrom/preseed/custom.seed boot=casper initrd=/casper/initrd.gz "quiet splash --"
```

#### Edit "quiet splash --" by init=/bin/bash

```
/casper/vmlinuz file=/cdrom/preseed/custom.seed boot=casper initrd=/casper/initrd.gz init=/bin/bash
```

#### Launche the VM and flood the ESC key

It should show 
```
aborted. boot : 
```

#### Now write the modified command

```
/casper/vmlinuz file=/cdrom/preseed/custom.seed boot=casper initrd=/casper/initrd.gz init=/bin/bash
```

#### You are now root !
