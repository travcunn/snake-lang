OP_CODES = {
    "inp": 0,
    "cla": 1,
    "add": 2,
    "tac": 3,
    "sft": 4,
    "out": 5,
    "sto": 6,
    "sub": 7,
    "jmp": 8,
    "hlt": 9,
    "mul": 10,
    "div": 11,
}


class InstructionError(Exception):
    pass


class Assembler(object):
    def __init__(self, inputfile):

        self.contents = [line.rstrip('\n') for line in inputfile.readlines()]

        self.generated_records = ["002", "800"]

        self.data_p = 4
        self.code_p = 10

        # key:value => label:addr
        self.symbol_table = {}

    def first_pass(self):
        """ Collect all symbols in the first pass. """

        code_p = self.code_p
        data_p = self.data_p

        for line in self.contents:
            tks = [tk.lower() for tk in line.split()]

            #: pass space or tab
            if not tks:
                continue

            #: label
            if tks[0] not in OP_CODES and len(tks) >= 3:
                label_name = tks[0]
                if tks[1] == 'data':
                    self.symbol_table[label_name] = data_p
                else:
                    self.symbol_table[label_name] = code_p
                tks.remove(tks[0])

            if len(tks) >= 2 and tks[0] in OP_CODES:
                code_p += 1

            if len(tks) >= 2 and tks[0] == 'data':
                data_p += 1

    def second_pass(self):

        for line in self.contents:
            tks = [tk.lower() for tk in line.split()]

            #: pass space or tab
            if not tks:
                continue

            #: label
            if tks[0] not in OP_CODES and len(tks) >= 3:
                tks.remove(tks[0])

            #: data
            if len(tks) >= 2 and tks[0] == 'data':
                self.generated_records.append(self.pad(self.data_p))
                self.generated_records.append(tks[1])
                self.data_p += 1
                continue

            #: instruction
            if len(tks) >= 2 and tks[0] in OP_CODES:
                operation = tks[0]
                address = tks[1]
                op = str(OP_CODES[operation])
                if address in self.symbol_table:
                    address = self.pad(self.symbol_table[address], length=2)
                code = op + address
                self.generated_records.append(self.pad(self.code_p))
                self.generated_records.append(code)
                self.code_p += 1
                continue

            raise InstructionError("Instruction error: %s" % (tks,))

        self.generated_records.append("002")
        self.generated_records.append("810")

    def assemble(self):
        self.first_pass()
        self.second_pass()

    @staticmethod
    def pad(data, length=3):
        """
        Pads either an integer or a number in string format with zeros.
        """
        padding = '0' * length
        data = '%s%s' % (padding, abs(data))
        return data[-length:]
