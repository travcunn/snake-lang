""" Test the virtual machine. """
from StringIO import StringIO
import sys
import os

import mock
import pytest

sys.path.append(os.path.join('..', '..', 'snake'))
from snake.vm import MEMORY_SIZE
from snake.vm import System


@pytest.fixture()
def system():
    """ Fixture to load a new VM. """
    return System()


@mock.patch('snake.vm.System.opcode_0')
def test_cycle(mock_opcode_0):
    """ Test a single cycle of bytecode execution. """
    system = System()
    test_file = StringIO("001")
    system.load_file(test_file)
    system.cycle()
    assert mock_opcode_0.called


@mock.patch('snake.vm.System.cycle')
def test_loop(mock_cycle, system):
    """ Test the VM execution loop. """
    test_file = StringIO("001")
    system.load_file(test_file)

    def stop_vm():
        """ Stops the VM. """
        system.running = False

    # Stop the VM after one cycle
    mock_cycle.side_effect = stop_vm
    system.run()
    assert mock_cycle.called


def test_inp_opcode(system):
    """ Test INP opcode. """
    system.reader = ['123']
    system.opcode_0(0)
    assert system.mem[0] == '123'
    system.reader = ['123']
    system.opcode_0(MEMORY_SIZE-1)
    assert system.mem[MEMORY_SIZE-1] == '123'
    system.reader = ['123']
    with pytest.raises(IndexError):
        system.opcode_0(MEMORY_SIZE)
    system.reader = ['123']
    with pytest.raises(IndexError):
        system.opcode_0(MEMORY_SIZE+1)


def test_cla_opcode(system):
    """ Test CLA opcode. """
    assert system.acc == 0
    system.mem[5] = 10
    system.opcode_1(5)
    assert system.acc == 10
    system.mem[6] = 15
    system.opcode_1(6)
    assert system.acc == 15


def test_add_opcode(system):
    """ Test ADD opcode. """
    assert system.acc == 0
    system.acc = 10
    system.mem[30] = 10
    system.opcode_2(30)
    assert system.acc == 20


def test_tac_opcode(system):
    """ Test TAC opcode. """
    assert system.pc == 0
    system.acc = 1
    system.opcode_3(10)
    assert system.pc == 0
    system.acc = 0
    system.opcode_3(10)
    assert system.pc == 0
    system.acc = -1
    system.opcode_3(10)
    assert system.pc == 10


def test_sft_opcode(system):
    """ Test SFT opcode. """
    system.acc = 10
    system.opcode_4(1)
    assert system.acc == 1
    system.acc = 10
    system.opcode_4(10)
    assert system.acc == 100


def test_out_opcode(system):
    """ Test OUT opcode. """
    system.stdout = mock.MagicMock()
    system.mem[5] = 13
    system.opcode_5(5)
    assert system.stdout.called


def test_sto_opcode(system):
    """ Test STO opcode. """
    assert system.mem[5] == 0
    system.acc = 10
    system.opcode_6(5)
    assert system.mem[5] == 10


def test_sub_opcode(system):
    """ Test SUB opcode. """
    system.acc = 10
    system.mem[5] = 4
    system.opcode_7(5)
    assert system.acc == 6


def test_jmp_opcode(system):
    """ Test JMP opcode. """
    assert system.pc == 0
    system.opcode_8(10)
    assert system.pc == 10


def test_hlt_opcode(system):
    """ Test HLT opcode. """
    system.running = True
    system.opcode_9(0)
    assert not system.running


def test_mul_opcode(system):
    """ Test MUL opcode. """
    system.acc = 12
    system.mem[5] = 6
    system.opcode_10(5)
    assert system.acc == 72


def test_div_opcode(system):
    """ Test DIV opcode. """
    system.acc = 72
    system.mem[5] = 6
    system.opcode_11(5)
    assert system.acc == 12
