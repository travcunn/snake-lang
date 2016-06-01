from __future__ import print_function

import math

# Set memory to 4k
MEMORY_SIZE = 1024 * 4


class Memory(object):
    """ This class controls the virtual memory space of the VM. """

    def __init__(self):
        """ Initialize memory. """
        self.mem = [0 for _ in range(0, MEMORY_SIZE)]
        self.mem[0] = '001'
        super(Memory, self).__init__()

    def get_memint(self, data):
        """ Get memory value. """
        return int(self.mem[data])


class IO(object):
    """ Class for virtual I/O. """

    def load_file(self, inputfile):
        """ Load a program into the input device. """

        contents = reversed(inputfile.readlines())
        self.reader = [line.rstrip('\n') for line in contents]

    def get_input(self):
        """ Receives input from the IO device. """
        return self.reader.pop()

    def stdout(self, data):
        print(data)


class VirtualMachine(object):
    """ Virtual machine that executes SnakeVM byte code. """

    def __init__(self):
        self.init_instructions()
        self.clear_registers()

        super(VirtualMachine, self).__init__()

    def init_instructions(self):
        """ Loads all CPU instructions. """

        self.opcodes = [
            self.opcode_0,
            self.opcode_1,
            self.opcode_2,
            self.opcode_3,
            self.opcode_4,
            self.opcode_5,
            self.opcode_6,
            self.opcode_7,
            self.opcode_8,
            self.opcode_9,
            self.opcode_10,
            self.opcode_11,
        ]

    def clear_registers(self):
        """ Clear CPU registers. """

        # Program counter register
        self.pc = 0
        # Instruction register
        self.ir = 0
        # Accumulator register
        self.acc = 0
        # Is the CPU running?
        self.running = False

    def fetch(self):
        """
        Retrieve an instruction from memory address pointed to by the program
        counter register.
        Next, increment the program counter.
        """
        self.ir = self.get_memint(self.pc)
        self.pc += 1

    def cycle(self):
        """ Execute a single opcode from the current program counter. """

        self.fetch()

        opcode, data = int(math.floor(self.ir / 100)), self.ir % 100

        self.opcodes[opcode](data)

    def opcode_0(self, data):
        """ INPUT Operation """
        self.mem[data] = self.get_input()

    def opcode_1(self, data):
        """ Clear and Add Operation """
        self.acc = self.get_memint(data)

    def opcode_2(self, data):
        """ Add Operation """
        self.acc += self.get_memint(data)

    def opcode_3(self, data):
        """ Test Accumulator contents Operation """
        if self.acc < 0:
            self.pc = data

    def opcode_4(self, data):
        """ Shift operation """
        x, y = int(math.floor(data / 10)), int(data % 10)
        for i in range(0, x):
            self.acc = (self.acc * 10) % 10000
        for i in range(0, y):
            self.acc = int(math.floor(self.acc / 10))

    def opcode_5(self, data):
        """ Output operation """
        self.stdout(self.mem[data])

    def opcode_6(self, data):
        """ Store operation """
        self.mem[data] = self.acc

    def opcode_7(self, data):
        """ Subtract Operation """
        self.acc -= self.get_memint(data)

    def opcode_8(self, data):
        """ Unconditional Jump operation """
        self.pc = data

    def opcode_9(self, data):
        """ Halt operation """
        self.running = False

    def opcode_10(self, data):
        """ Multiply operation """
        self.acc *= self.get_memint(data)

    def opcode_11(self, data):
        """ Divide operation """
        self.acc /= self.get_memint(data)

    def run(self):
        """ Runs code in memory until halt opcode. """
        self.running = True
        while self.running:
            self.cycle()


class System(VirtualMachine, Memory, IO):
    """
    Composition of the Snake virtual machine, virtual memory, and virtual
    IO.
    """
    pass
