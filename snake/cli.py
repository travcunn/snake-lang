import argparse
import sys

from .assembler import Assembler
from .vm import System


def create_assembler_parser():
    """ Create an ArgumentParser for the assembler. """
    parser = argparse.ArgumentParser(
        description='A 2 pass assembler.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "file",
        help="file to be assembled."
    )

    parser.add_argument(
        '-o', '--outfile', default=None, required=False,
        help='output file'
    )

    return parser


def create_vm_parser():
    """ Create an ArgumentParser for the VM. """

    parser = argparse.ArgumentParser(
        description='A simple vm.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "file",
        help="bytecode file to be loaded."
    )

    return parser


def assembler():
    """ Assembler entrypoint. """
    # Take action depending on whether or not this is being pipelined
    if sys.stdin.isatty():
        parser = create_assembler_parser()
        args = parser.parse_args()

        assemble_from_args(args.file, args.outfile)
    else:
        assemble_from_stdin()


def assemble_from_args(in_file, out_file):
    """ Read source program from in_file and save to out_file. """

    with open(in_file, 'rb') as f:
        assembler = Assembler(f)
        assembler.assemble()
        output_records = assembler.generated_records

    if out_file is None:
        for record in output_records:
            print(record)
    else:
        with open(out_file, 'wb') as w:
            for record in output_records:
                w.write(record)
                w.write('\n')


def assemble_from_stdin():
    """ Read source program from stdin and run the assembler. """
    assembler = Assembler(sys.stdin)
    assembler.assemble()
    output_records = assembler.generated_records
    for record in output_records:
        print(record)


def vm_from_args(in_file):
    """ Run bytecode program from a file. """
    try:
        system = System()
        with open(in_file, 'rb') as f:
            system.load_file(f)
        system.run()
    except:
        print "IR: %s\nPC: %s\n" % (system.ir, system.pc)
        raise


def vm_from_stdin():
    try:
        system = System()
        system.load_file(sys.stdin)
        system.run()
    except:
        print "IR: %s\nPC: %s\n" % (system.ir, system.pc)
        raise


def vm():
    """ VM entrypoint. """
    # Take action depending on whether or not this is being pipelined
    if sys.stdin.isatty():
        parser = create_vm_parser()
        args = parser.parse_args()

        vm_from_args(args.file)
    else:
        vm_from_stdin()
