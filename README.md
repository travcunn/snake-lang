# Simple CPU Emulator
A simple CPU emulator and assembler written in Python

# Architecture
### CPU
The CPU has 3 registers:
- Program counter register
- Instruction register
- Accumulator register

### Memory
There are 4096 'virtual' memory locations.

### IO
Input and output are handled through stdin/stdout.

# Installation
```
# python setup.py install
```

# Usage
### Assembler
```
# assembler -h
usage: assembler [-h] [-o OUTFILE] file

A 2 pass assembler.

positional arguments:
  file                  file to be assembled.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file (default: None)

```

### CPU
```
# cpu -h
usage: cpu [-h] [-o OUTFILE] [--step] file

A simple cpu.

positional arguments:
  file                  file to be assembled.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file (default: None)
  --step                step through each cpu cycle. (default: False)
```

### Putting it all together
Alternatively, data can be piped into both the CPU and assembler.
```
# assembler < programs/test.src | cpu
```

# Example Program
``` asm
a       DATA    4
b       DATA    2
result  DATA    0

        ADD     a
        ADD     b
        STO     result
        OUT     result
        HRS     a
```
Assemble the program:
```
# assembler < programs/test.src
002
800
004
4
005
2
006
0
010
204
011
205
012
606
013
506
014
904
002
810
```
Run it:
```
# assembler < programs/test.src | cpu
6
```
