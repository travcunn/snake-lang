""" Test the virtual IO system. """
from io import BytesIO
import sys
import os

from mock import call
from mock import patch
import pytest

sys.path.append(os.path.join('..', '..', 'snake'))
from snake.vm import System


@pytest.fixture()
def system():
    """ Fixture to load a new VM. """
    return System()


def test_io_load_file(system):
    """ Test loading a file. """

    test_file = BytesIO("hello world")

    system.load_file(test_file)

    assert system.get_input() == 'hello world'


def test_io_stdout(system):
    """ Test IO output. """

    with patch('__builtin__.print') as mock_print:
        system.stdout('hello world')
        mock_print.assert_has_calls([
            call('hello world')
        ])
