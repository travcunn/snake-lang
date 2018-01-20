""" Test the compiler. """
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import os
import sys

import pytest

sys.path.append(os.path.join('..', '..', 'snake'))
from snake.compiler import Compiler


def test_compile_simple_code():
    """ Test compiling the language into simple SnakeVM assembly. """

    test_file = StringIO("""
int foo = 10;

void main() {
   print(foo);
   print(12);
}
    """)

    compiler = Compiler(test_file)
    compiler.compile()

    assert assembler.generated_records == """
a       DATA    10
b       DATA    12
main    OUT     a
        OUT     b
        JMP     exit
exit    HLT     a
    """
