CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -g
IDIR =.

ODIR=obj

_DEPS = list.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = list.o list_test.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

list_test_make: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f 
