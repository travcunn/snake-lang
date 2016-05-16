import argparse
import sys

from .assembler import Assembler
from .vm import System


def assembler():
    parser = argparse.ArgumentParser(description='A 2 pass assembler.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Take action depending on whether or not this is being pipelined
    if sys.stdin.isatty():
        parser.add_argument("file", help="file to be assembled.")
        parser.add_argument('-o','--outfile', help='output file',
                            default=None, required=False)
        args = parser.parse_args()

        try:
            with open(args.file, 'r') as f:
                a = Assembler(f)
                a.assemble()
                output_records = a.generated_records
        except IOError:
            print("[IO Error]: The source file could not be opened.")
        else:
            try:
                if args.outfile is None:
                    for record in output_records:
                        print(record)
                else:
                    with open(args.outfile, 'w') as w:
                        for record in output_records:
                            w.write(record)
                            w.write('\n')
            except IOError:
                print("[IO Error]: The output file could not be opened.")
    else:
        a = Assembler(sys.stdin)
        try:
            a.assemble()
            output_records = a.generated_records
        except StopIteration:
            print("[IO Error]: The source program could not be read from stdin")
        else:
            for record in output_records:
                print(record)


def vm():
    parser = argparse.ArgumentParser(description='A simple vm.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Take action depending on whether or not this is being pipelined
    if sys.stdin.isatty():
        parser.add_argument("file", help="bytecode file to be loaded.")
        parser.add_argument('-o','--outfile', help='output file',
                            default=None, required=False)
        parser.add_argument('--step', dest='step',
                            help='step through each instruction cycle.',
                            action='store_true')
        parser.set_defaults(step=False)
        args = parser.parse_args()

        try:
            system = System()
            with open(args.file, 'r') as f:
                system.load_file(f)
            system.step = args.step
            system.run()
        except IOError:
            print("[IO Error]: The source file could not be opened.")
        except:
            print "IR: %s\nPC: %s\nOutput: %s\n" % \
                (system.ir, system.pc, system.format_output())
            raise
    else:
        try:
            system = System()
            system.load_file(sys.stdin)
            system.run()
        except StopIteration:
            print("[IO Error]: The source program could not be read from stdin")
        except:
            print "IR: %s\nPC: %s\nOutput: %s\n" % \
                (system.ir, system.pc, system.format_output())
            raise


if __name__ == '__main__':
    assembler()
