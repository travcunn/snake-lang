import math

# Set memory to 4k
MEMORY_SIZE = 1024 * 4


class Memory(object):
    """ This class controls the virtual memory space of the simulator. """

    def init_mem(self):
        """ Initialize memory. """
        self.mem = [0 for _ in range(0, MEMORY_SIZE)]
        self.mem[0] = '001'  #: The Cardiac bootstrap operation.

    def get_memint(self, data):
        """ Get memory value. """
        return int(self.mem[data])

    @staticmethod
    def normalize(data):
        """ Normalizes data inserted into memory. """
        return str(data)

    def show_mem(self):
        res = ""
        for addr, value in enumerate(self.mem):
            if addr % 10 == 0:
                res += '\n'
            if not value:
                value = "---"
            if self.pc - 1 == addr:
                res += "%s >%s< " % (self.normalize(addr), value)
            else:
                res += "%s [%s] " % (self.normalize(addr), value)
        print res


class IO(object):
    """ Class for virtual I/O. """

    def init_reader(self):
        """ Initializes the input device. """
        self.reader = []

    def init_output(self):
        """ Initializes output device. """
        self.output = []

    def load_file(self, inputfile):
        """ Load a program into the input device. """
        self.reader = list(line.rstrip('\n') for line in inputfile.readlines())
        self.reader.reverse()

    def format_output(self):
        """ Format the output of this virtual IO device. """
        return '\n'.join(self.output)

    def get_input(self):
        """ Receives input from the IO device. """
        try:
            return self.reader.pop()
        except IndexError:
            # Fall back to raw_input() in the case of EOF on the reader.
            return raw_input('INP: ')[:3]

    def stdout(self, data):
        print(data)


class CPU(object):
    """ CPU class. """

    def __init__(self):
        self.init_cpu()
        self.reset()
        self.step = False
        try:
            self.init_mem()
        except AttributeError:
            raise NotImplementedError('Add a mixin memory-enabled class.')
        try:
            self.init_reader()
            self.init_output()
        except AttributeError:
            raise NotImplementedError('Add a mixin IO-enabled class.')

    def reset(self):
        """ Clear CPU registers. """

        # Program counter register
        self.pc = 0
        # Instruction register
        self.ir = 0
        # Accumulator register
        self.acc = 0
        # Is the CPU running?
        self.running = False

    def init_cpu(self):
        """ Loads all CPU opcodes. """

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

    def fetch(self):
        """
        Retrieve an instruction from memory address pointed to by the program
        counter register.
        Next, increment the program counter.
        """
        self.ir = self.get_memint(self.pc)
        self.pc += 1

    def process(self):
        """ Process a single opcode from the current program counter. """

        self.fetch()

        if self.step:
            self.show_mem()
            if len(self.reader):
                print "top of Input: %s" % self.reader[-1]
            print "IR: %s    PC: %s    Acc: %s\nOutput: %s\n" % (self.normalize(self.ir), \
                self.normalize(self.pc), self.normalize(self.acc), self.format_output())
            raw_input("press enter to continue >>")

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
        self.mem[data] = self.normalize(self.acc)

    def opcode_7(self, data):
        """ Subtract Operation """
        self.acc -= self.get_memint(data)

    def opcode_8(self, data):
        """ Unconditional Jump operation """
        self.mem[99] = '8' + self.normalize(self.pc)
        self.pc = data

    def opcode_9(self, data):
        """ Halt and Reset operation """
        self.reset()
 
    def opcode_10(self, data):
        """ Multiply operation """
        self.acc *= self.get_memint(data)

    def opcode_11(self, data):
        """ Divide operation """
        self.acc /= self.get_memint(data)

    def run(self, pc=None):
        """ Runs code in memory until halt/reset opcode. """
        if pc:
            self.pc = pc
        self.running = True
        while self.running:
            self.process()
        self.init_output()


class System(CPU, Memory, IO):
    pass
