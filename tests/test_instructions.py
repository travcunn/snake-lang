import sys
import os
sys.path.append(os.path.join('..', '..', 'simple_cpu'))

import unittest

import mock
import pytest

from simple_cpu.cpu import MEMORY_SIZE
from simple_cpu.cpu import System


class BaseSystemTest(unittest.TestCase):
    """ Base system test. """
    def setUp(self):
        self.vm = System()


class InpInstructionTest(BaseSystemTest):
    """ Test INP instruction. """
    def test_inp(self):
        self.vm.reader = ['123']
        self.vm.opcode_0(0)
        assert self.vm.mem[0] == '123'
        self.vm.reader = ['123']
        self.vm.opcode_0(MEMORY_SIZE-1)
        assert self.vm.mem[MEMORY_SIZE-1] == '123'
        self.vm.reader = ['123']
        with pytest.raises(IndexError):
            self.vm.opcode_0(MEMORY_SIZE)
        self.vm.reader = ['123']
        with pytest.raises(IndexError):
            self.vm.opcode_0(MEMORY_SIZE+1)


class ClaInstructionTest(BaseSystemTest):
    """ Test CLA instruction. """
    def test_cla(self):
        assert self.vm.acc == 0
        self.vm.mem[5] = 10
        self.vm.opcode_1(5)
        assert self.vm.acc == 10
        self.vm.mem[6] = 15
        self.vm.opcode_1(6)
        assert self.vm.acc == 15


class AddInstructionTest(BaseSystemTest):
    """ Test ADD instruction. """
    def test_add(self):
        assert self.vm.acc == 0
        self.vm.acc = 10
        self.vm.mem[30] = 10
        self.vm.opcode_2(30)
        assert self.vm.acc == 20


class TacInstructionTest(BaseSystemTest):
    """ Test TAC instruction. """
    def test_tac(self):
        assert self.vm.pc == 0
        self.vm.acc = 1
        self.vm.opcode_3(10)
        assert self.vm.pc == 0
        self.vm.acc = 0
        self.vm.opcode_3(10)
        assert self.vm.pc == 0
        self.vm.acc = -1
        self.vm.opcode_3(10)
        assert self.vm.pc == 10


class SftInstructionTest(BaseSystemTest):
    """ Test SFT instruction. """
    def test_sft(self):
        self.vm.acc = 10
        self.vm.opcode_4(1)
        assert self.vm.acc == 1
        self.vm.acc = 10
        self.vm.opcode_4(10)
        assert self.vm.acc == 100


class OutInstructionTest(BaseSystemTest):
    """ Test OUT instruction. """
    def test_out(self):
        self.vm.stdout = mock.MagicMock()
        self.vm.mem[5] = 13
        self.vm.opcode_5(5)
        assert self.vm.stdout.called


class StoInstructionTest(BaseSystemTest):
    """ Test STO instruction. """
    def test_sto(self):
        assert self.vm.mem[5] == 0
        self.vm.acc = 10
        self.vm.opcode_6(5)
        assert self.vm.mem[5] == 10


class SubInstructionTest(BaseSystemTest):
    """ Test SUB instruction. """
    def test_sub(self):
        self.vm.acc = 10
        self.vm.mem[5] = 4
        self.vm.opcode_7(5)
        assert self.vm.acc == 6


class JmpInstructionTest(BaseSystemTest):
    """ Test JMP instruction. """
    def test_jmp(self):
        assert self.vm.pc == 0
        self.vm.opcode_8(10)
        assert self.vm.pc == 10


class HltInstructionTest(BaseSystemTest):
    """ Test HLT instruction. """
    def test_hlt(self):
        self.vm.running = True
        self.vm.opcode_9(0)
        assert not self.vm.running


class MulInstructionTest(BaseSystemTest):
    """ Test MUL instruction. """
    def test_mul(self):
        self.vm.acc = 12
        self.vm.mem[5] = 6
        self.vm.opcode_10(5)
        assert self.vm.acc == 72


class DivInstructionTest(BaseSystemTest):
    """ Test DIV instruction. """
    def test_div(self):
        self.vm.acc = 72
        self.vm.mem[5] = 6
        self.vm.opcode_11(5)
        assert self.vm.acc == 12
