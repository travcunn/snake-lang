# Simple CPU Emulator
A simple CPU emulator and assembler written in Python

# Architecture
### CPU
The CPU has 3 registers:
- Program counter register
- Instruction register
- Accumulator register

### Instruction Set

| Opcode | Mnemonic | Instruction               | Description                                                                                                                                                                                                              |
|--------|----------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | INP      | Input                     | take a number from the input card and put it in a specified memory cell.                                                                                                                                                 |
| 1      | CLA      | Clear and add             | clear the accumulator and add the contents of a memory cell to the accumulator.                                                                                                                                          |
| 2      | ADD      | Add                       | add the contents of a memory cell to the accumulator.                                                                                                                                                                    |
| 3      | TAC      | Test accumulator contents | performs a sign test on the contents of the accumulator; if minus, jump to a specified memory cell.                                                                                                                      |
| 4      | SFT      | Shift                     | shifts the accumulator x places left, then y places right, where x is the upper address digit and y is the lower.                                                                                                        |
| 5      | OUT      | Output                    | take a number from the specified memory cell and write it on the output card.                                                                                                                                            |
| 6      | STO      | Store                     | copy the contents of the accumulator into a specified memory cell.                                                                                                                                                       |
| 7      | SUB      | Subtract                  | subtract the contents of a specified memory cell from the accumulator.                                                                                                                                                   |
| 8      | JMP      | Jump                      | jump to a specified memory cell. The current cell number is written in cell 99. This allows for one level of subroutines by having the return be the instruction at cell 99 (which had '8' hardcoded as the first digit. |
| 9      | HRS      | Halt and reset            | move bug to the specified cell, then stop program execution.                                                                                                                                                             |

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
