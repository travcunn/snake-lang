""" Test the virtual IO system. """
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import sys
import os

import pytest

sys.path.append(os.path.join('..', '..', 'snake'))
from snake.assembler import Assembler
from snake.assembler import InstructionError


def test_generate_code():
    """ Test assembling assembly into snake bytecode. """

    test_file = StringIO("""
a       DATA    4
b       DATA    2
result  DATA    0

        ADD     a
        ADD     b
        STO     result
        OUT     result
        JMP     exit

exit    HLT     a
        
    """)

    assembler = Assembler(test_file)
    assembler.assemble()

    assert assembler.generated_records == [
        '002', '800', '004', '4', '005', '2', '006', '0', '010', '204',
        '011', '205', '012', '606', '013', '506', '014', '815', '015', 
        '904', '002', '810'
    ]


def test_invalid_instructions():
    """ Test assembling invalid assembly. """

    test_file = StringIO("""
        ABC     a
        ADD     b
        STO     result
        OUT     result
        JMP     exit
        
    """)

    assembler = Assembler(test_file)
    with pytest.raises(InstructionError):
        assembler.assemble()
