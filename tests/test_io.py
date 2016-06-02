""" Test the virtual IO system. """
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
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

    test_file = StringIO("hello world")

    system.load_file(test_file)

    assert system.get_input() == 'hello world'


def test_io_stdout(system):
    """ Test IO output. """

    with patch('snake.vm.sys.stdout') as mock_stdout:
        system.stdout('hello world')
        mock_stdout.write.assert_has_calls([
            call('hello world\n')
        ])
