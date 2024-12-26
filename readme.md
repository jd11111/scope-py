# Install:
- drop libps2000.so into folder
- allow filesystem to access scope:
> services.udev.extraRules = ''SUBSYSTEM=="usb", ATTR{idVendor}==SCOPEVENDORID, ATTR{idProduct}==SCOPEPRODUCTID, TAG+="uaccess", RUN{builtin}+="uaccess"'';

can get SCOPEVENDORID:SCOPEPRODUCTID from lsusb!!!
