""" Test the CLI application. """
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import os
import sys


from mock import mock_open
from mock import patch
import pytest

sys.path.append(os.path.join('..', '..', 'snake'))
from snake.cli import assembler
from snake.cli import assemble_from_args
from snake.cli import assemble_from_stdin
from snake.cli import create_assembler_parser
from snake.cli import create_vm_parser
from snake.cli import vm
from snake.cli import vm_from_args
from snake.cli import vm_from_stdin


@pytest.fixture()
def assembler_parser():
    """ Create a ArgumentParser. """
    return create_assembler_parser()


@pytest.fixture()
def vm_parser():
    """ Create a ArgumentParser. """
    return create_vm_parser()


def test_assembler_with_empty_args(assembler_parser):
    """ Test the assembler with empty CLI args. """

    with pytest.raises(SystemExit):
        assembler_parser.parse_args([])


def test_assembler_with_valid_in_and_out_file(assembler_parser):
    """ Test the assembler with input and output file CLI args. """

    args = assembler_parser.parse_args(['-o', 'outfile', 'infile'])

    m = mock_open()
    with patch('snake.cli.open', m, create=True):
        assemble_from_args(args.file, args.outfile)


def test_assembler_with_invalid_in_file(assembler_parser):
    """ Test the assembler with an invalid in file. """

    args = assembler_parser.parse_args(['-o', 'outfile', 'infile'])

    with pytest.raises(IOError):
        assemble_from_args(args.file, args.outfile)


def test_assembler_with_blank_out_file(assembler_parser):
    """ Test the assembler without specifying an out file. """

    args = assembler_parser.parse_args(['infile'])

    m = mock_open()
    with patch('snake.cli.open', m, create=True):
        assemble_from_args(args.file, args.outfile)


@patch('snake.cli.sys')
def test_assembler_with_pipe(mock_sys):
    """ Test piping a program into the assembler. """

    assemble_from_stdin()


@patch('snake.cli.create_assembler_parser')
@patch('snake.cli.assemble_from_stdin')
def test_assembler_entrypoint_stdin(mock_assemble_from_stdin,
                                    mock_assembler_parser):
    """ Test the assembler entrypoint with stdin input. """
    test_program = StringIO("""
A   DATA    0
    HLT     A
    """)
    with patch("sys.stdin", test_program):
        with patch("sys.stdout", new_callable=StringIO):
            assembler()
    assert mock_assemble_from_stdin.called


@patch('snake.cli.create_assembler_parser')
@patch('snake.cli.sys')
@patch('snake.cli.assemble_from_args')
def test_assembler_entrypoint_args(mock_assemble_from_args,
                                   mock_sys,
                                   mock_assembler_parser):
    """ Test the assembler entrypoint with arguments. """
    test_program = StringIO("""
A   DATA    0
    HLT     A
    """)
    with patch("sys.stdin", test_program):
        with patch("sys.stdout", new_callable=StringIO):
            assembler()
    assert mock_assemble_from_args.called


def test_vm_with_empty_args(vm_parser):
    """ Test the VM with empty CLI args. """

    with pytest.raises(SystemExit):
        vm_parser.parse_args([])


def test_vm_with_valid_in_file(vm_parser):
    """ Test the VM with input file CLI args. """

    args = vm_parser.parse_args(['infile'])

    m = mock_open()
    with patch('snake.cli.open', m, create=True):
        with pytest.raises(IndexError):
            vm_from_args(args.file)


@patch('snake.cli.sys')
def test_vm_with_pipe(mock_sys):
    """ Test piping a program into the VM. """

    with pytest.raises(IndexError):
        vm_from_stdin()


@patch('snake.cli.create_vm_parser')
@patch('snake.cli.vm_from_stdin')
def test_vm_entrypoint_stdin(mock_vm_from_stdin,
                             mock_vm_parser):
    """ Test the vm entrypoint with stdin input. """
    test_program = StringIO("""
A   DATA    0
    HLT     A
    """)
    with patch("sys.stdin", test_program):
        with patch("sys.stdout", new_callable=StringIO):
            vm()
    assert mock_vm_from_stdin.called


@patch('snake.cli.create_vm_parser')
@patch('snake.cli.sys')
@patch('snake.cli.vm_from_args')
def test_vm_entrypoint_args(mock_vm_parser, mock_sys, mock_vm_from_args):
    """ Test the vm entrypoint with arguments. """
    test_program = StringIO("""
A   DATA    0
    HLT     A
    """)
    with patch("sys.stdin", test_program):
        with patch("sys.stdout", new_callable=StringIO):
            vm()

    assert mock_vm_from_args.called
