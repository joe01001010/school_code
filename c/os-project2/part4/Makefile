obj-m += example2.o

all:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(CURDIR) CC=gcc-12 modules

clean:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(CURDIR) CC=gcc-12 clean
