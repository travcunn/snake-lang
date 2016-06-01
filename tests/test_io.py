from StringIO import StringIO
import sys
import os
import unittest

from mock import call
from mock import patch

sys.path.append(os.path.join('..', '..', 'snake'))
from snake.vm import System


class BaseSystemTest(unittest.TestCase):
    """ Base system test. """
    def setUp(self):
        self.vm = System()


class VirtualIOTest(BaseSystemTest):
    """ Test the virtual IO. """

    def test_load_file(self):
        """ Test loading a file. """

        test_file = StringIO("hello world")

        self.vm.load_file(test_file)

        assert self.vm.get_input() == 'hello world'

    def test_stout(self):
        """ Test IO output. """

        with patch('__builtin__.print') as mock_print:
            self.vm.stdout('hello world')
            mock_print.assert_has_calls([
                call('hello world')
            ])
