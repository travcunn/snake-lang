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


def test_primitives():
    """ Test compiling primitives into SnakeVM IR code. """

    test_file = StringIO("""
int foo = 10;

void main() {
  print(foo);
}
    """)

    compiler = Compiler(test_file)
    compiler.compile()

    assert compiler.generated_records == [
        "exitdata DATA 0",
        "foo DATA 10",
        "JMP main",
        "main NOOP 0",
        "OUT foo",
        "exit HLT exitdata"
    ]

def test_function_return():
    """ Test compiling functions into SnakeVM IR code. """

    test_file = StringIO("""
int foo = 10;

void main() {
  print(foo);
}
    """)

    compiler = Compiler(test_file)
    compiler.compile()

    assert compiler.generated_records == [
        "exitdata DATA 0",
        "foo DATA 10",
        "JMP main",
        "main NOOP 0",
        "OUT foo",
        "exit HLT exitdata"
    ]
