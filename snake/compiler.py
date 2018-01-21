class Token(object):
    def generate(self):
        pass


class Integer(Token):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def generate(self):
        return "%s DATA %s" % (self.name, self.value)


class Print(Token):
    def __init__(self, value):
        self.value = value

    def generate(self):
        return "OUT %s" % (self.value, )


class RunMain(Token):
    def generate(self):
        return "JMP main"


class Noop(Token):
    def generate(self):
        return "NOOP"


class Function(Token):
    def __init__(self, name):
        self.name = name

    def generate(self):
        return "%s NOOP 0" % (self.name, )


class Exit(Token):
    def generate(self):
        return "exit HLT exitdata"


class Compiler(object):
    def __init__(self, inputfile):
        self.contents = [line.rstrip('\n') for line in inputfile.readlines()]

        self.data = []
        self.program = []

        self.generated_lexical = []
        self.generated_records = []

        self.in_function = False

    def first_pass(self):
        """ Parse the program. """
        for line in self.contents:
            line_contents = line.split(" ")

            # Skip empty lines
            if not any(map(bool, line_contents)):
                continue

            # Parse integers
            if line_contents[0] == "int":
                literal = int(line_contents[3].replace(";", ""))
                integer = Integer(line_contents[1], literal)
                self.data.append(integer)

            if line_contents[0].startswith("main()"):
                main = Function("main")
                self.program.append(main)
                self.in_function = "main"

            if self.in_function == "main" and line_contents[0] == "}":
                self.in_function = False
                # Exit the program after running the main function
                self.program.append(Exit())

            if len(line_contents) >= 3:
                if line_contents[2].startswith("print("):
                    value = line_contents[2].split("(")[1].split(")")[0]
                    printer = Print(value)
                    self.program.append(printer)

    def second_pass(self):
        """ Generate a program binary. """
        # Data for exit
        self.generated_lexical.append(Integer('exitdata', 0))

        # Allocate all variables
        for data_literal in self.data:
            self.generated_lexical.append(data_literal)

        # Instruction to start executing the main function
        self.generated_lexical.append(RunMain())

        for program_data in self.program:
            self.generated_lexical.append(program_data)

    def third_pass(self):
        """ Generate assembly from parsed code. """
        for lexical in self.generated_lexical:
            self.generated_records.append(lexical.generate())

    def compile(self):
        self.first_pass()
        self.second_pass()
        self.third_pass()
