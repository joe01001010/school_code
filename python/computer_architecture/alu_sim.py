from enum import Enum
import os

import cocotb

from cocotb.clock import Clock
try:
    from cocotb.runner import get_runner
except ModuleNotFoundError:
    from cocotb_tools.runner import get_runner
from cocotb.triggers import NextTimeStep, ReadOnly, ReadWrite, RisingEdge

alu_sim_dir = os.path.abspath(os.path.join('.', 'alu_sim_dir'))

class Funct3(Enum):
    ADD = 0
    SLL = 1
    SLT = 2
    SLTU = 3
    XOR = 4
    SRL = 5
    SRA = 5
    OR = 6
    AND = 7

MASK_32 = 0xFFFFFFFF


async def _tick_and_settle(dut):
    await RisingEdge(dut.clk)
    await ReadOnly()
    await NextTimeStep()


async def perform_not(dut) -> None:
    """
    ~

    :param dut: DUT object from cocotb
    :return: None
    """
    dut.funct3.value = Funct3.XOR.value
    dut.funct7.value = 0
    dut.s2.value = MASK_32
    await _tick_and_settle(dut)


async def perform_negate(dut) -> None:
    """
    Perform the two's complement.

    :param dut: DUT object from cocotb
    :return: None
    """
    await ReadWrite()
    await perform_not(dut)
    not_value = int(dut.d.value) & MASK_32

    dut.funct3.value = Funct3.ADD.value
    dut.funct7.value = 0
    dut.s1.value = not_value
    dut.s2.value = 1
    await _tick_and_settle(dut)


async def perform_sub(dut) -> None:
    """
    sub rd, rs1, rs2

    :param dut: Dut object from cocotb
    :param s1: First value as described in R sub
    :param s2: Second value as described in R sub
    :return: None
    """
    await ReadWrite()
    s1 = int(dut.s1.value) & MASK_32
    s2 = int(dut.s2.value) & MASK_32

    dut.s1.value = s2
    await perform_negate(dut)
    neg_s2 = int(dut.d.value) & MASK_32

    dut.funct3.value = Funct3.ADD.value
    dut.funct7.value = 0
    dut.s1.value = s1
    dut.s2.value = neg_s2
    await _tick_and_settle(dut)


async def set_gt(dut):
    """
    In the same format as slt, rd, rsq, rs2 perform the operation to set the output LSB bit to rs1 > rs2.

    :param dut:
    :return:
    """
    await ReadWrite()
    s1 = int(dut.s1.value) & MASK_32
    s2 = int(dut.s2.value) & MASK_32

    dut.funct3.value = Funct3.SLTU.value
    dut.funct7.value = 0
    dut.s1.value = s2
    dut.s2.value = s1
    await _tick_and_settle(dut)


async def set_gte(dut):
    """
    In the same format as slt rd, rs1, rs2 perform the operation to set the output LSB bit to rs1 >= rs2.

    :param dut: DUT object from cocotb
    :return:
    """
    await ReadWrite()
    s1 = int(dut.s1.value) & MASK_32
    s2 = int(dut.s2.value) & MASK_32

    dut.s1.value = s1
    dut.s2.value = s2
    await set_gt(dut)
    gt = int(dut.d.value) & MASK_32

    dut.funct3.value = Funct3.XOR.value
    dut.funct7.value = 0
    dut.s1.value = s1
    dut.s2.value = s2
    await _tick_and_settle(dut)
    eq = int(dut.zero.value) & 0x1

    dut.funct3.value = Funct3.OR.value
    dut.funct7.value = 0
    dut.s1.value = gt
    dut.s2.value = eq
    await _tick_and_settle(dut)


async def f_set_e(dut):
    """
    In the same format as feq.s rd, rs1, rs2 perform a floating point equal comparison.

    :param dut:
    :return:
    """
    await ReadWrite()
    s1 = int(dut.s1.value) & MASK_32
    s2 = int(dut.s2.value) & MASK_32

    dut.funct3.value = Funct3.XOR.value
    dut.funct7.value = 0
    dut.s1.value = s1
    dut.s2.value = s2
    await _tick_and_settle(dut)
    eq = int(dut.zero.value) & 0x1

    dut.funct3.value = Funct3.ADD.value
    dut.funct7.value = 0
    dut.s1.value = 0
    dut.s2.value = eq
    await _tick_and_settle(dut)


async def f_set_lt(dut):
    """
    In the same format as flt.s rd, rs1, rs2 perform a floating point less than comparison.

    :param dut:
    :return:
    """
    dut.funct3.value = Funct3.SLTU.value
    dut.funct7.value = 0
    await _tick_and_settle(dut)


async def f_set_lte(dut):
    """
    In the same format as fle.s rd, rs1, rs2 perform a floating point less than or equal comparison.

    :param dut:
    :return:
    """
    await ReadWrite()
    s1 = int(dut.s1.value) & MASK_32
    s2 = int(dut.s2.value) & MASK_32

    dut.s1.value = s1
    dut.s2.value = s2
    await f_set_lt(dut)
    lt = int(dut.d.value) & MASK_32

    dut.s1.value = s1
    dut.s2.value = s2
    await f_set_e(dut)
    eq = int(dut.d.value) & MASK_32

    dut.funct3.value = Funct3.OR.value
    dut.funct7.value = 0
    dut.s1.value = lt
    dut.s2.value = eq
    await _tick_and_settle(dut)


async def perform_multiplication(dut):
    """
    In the same format as mul rd, rs1, rs2 perform multiplication.

    :param dut:
    :return:
    """
    await ReadWrite()
    rs1 = int(dut.s1.value) & MASK_32
    rs2 = int(dut.s2.value) & MASK_32

    multiplicand = rs1
    multiplier = rs2
    product = 0

    for _ in range(32):
        dut.funct3.value = Funct3.AND.value
        dut.funct7.value = 0
        dut.s1.value = multiplier
        dut.s2.value = 1
        await _tick_and_settle(dut)
        lsb = int(dut.d.value) & MASK_32

        if lsb:
            dut.funct3.value = Funct3.ADD.value
            dut.funct7.value = 0
            dut.s1.value = product
            dut.s2.value = multiplicand
            await _tick_and_settle(dut)
            product = int(dut.d.value) & MASK_32

        dut.funct3.value = Funct3.SLL.value
        dut.funct7.value = 0
        dut.s1.value = multiplicand
        dut.s2.value = 1
        await _tick_and_settle(dut)
        multiplicand = int(dut.d.value) & MASK_32

        dut.funct3.value = Funct3.SRL.value
        dut.funct7.value = 0
        dut.s1.value = multiplier
        dut.s2.value = 1
        await _tick_and_settle(dut)
        multiplier = int(dut.d.value) & MASK_32

    dut.funct3.value = Funct3.ADD.value
    dut.funct7.value = 0
    dut.s1.value = product
    dut.s2.value = 0
    await _tick_and_settle(dut)


async def perform_division(dut):
    """
    In the same format as mul rd, rs1, rs2 perform multiplication.

    :param dut:
    :return:
    """
    await ReadWrite()
    dividend = int(dut.s1.value) & MASK_32
    divisor = int(dut.s2.value) & MASK_32

    dut.funct3.value = Funct3.XOR.value
    dut.funct7.value = 0
    dut.s1.value = divisor
    dut.s2.value = 0
    await _tick_and_settle(dut)
    if int(dut.zero.value):
        dut.s1.value = 0
        await perform_not(dut)
        return

    quotient = 0
    remainder = 0
    dividend_shift = dividend

    for _ in range(32):
        dut.funct3.value = Funct3.AND.value
        dut.funct7.value = 0
        dut.s1.value = dividend_shift
        dut.s2.value = 0x80000000
        await _tick_and_settle(dut)
        msb = int(dut.d.value) & MASK_32

        dut.s1.value = msb
        dut.s2.value = 0
        await set_gt(dut)
        in_bit = int(dut.d.value) & 0x1

        dut.funct3.value = Funct3.SLL.value
        dut.funct7.value = 0
        dut.s1.value = dividend_shift
        dut.s2.value = 1
        await _tick_and_settle(dut)
        dividend_shift = int(dut.d.value) & MASK_32

        dut.funct3.value = Funct3.SLL.value
        dut.funct7.value = 0
        dut.s1.value = remainder
        dut.s2.value = 1
        await _tick_and_settle(dut)
        remainder = int(dut.d.value) & MASK_32

        dut.funct3.value = Funct3.OR.value
        dut.funct7.value = 0
        dut.s1.value = remainder
        dut.s2.value = in_bit
        await _tick_and_settle(dut)
        remainder = int(dut.d.value) & MASK_32

        dut.funct3.value = Funct3.SLL.value
        dut.funct7.value = 0
        dut.s1.value = quotient
        dut.s2.value = 1
        await _tick_and_settle(dut)
        quotient = int(dut.d.value) & MASK_32

        dut.s1.value = remainder
        dut.s2.value = divisor
        await set_gte(dut)
        take = int(dut.d.value) & 0x1

        if take:
            dut.s1.value = remainder
            dut.s2.value = divisor
            await perform_sub(dut)
            remainder = int(dut.d.value) & MASK_32

            dut.funct3.value = Funct3.OR.value
            dut.funct7.value = 0
            dut.s1.value = quotient
            dut.s2.value = 1
            await _tick_and_settle(dut)
            quotient = int(dut.d.value) & MASK_32

    dut.funct3.value = Funct3.ADD.value
    dut.funct7.value = 0
    dut.s1.value = quotient
    dut.s2.value = 0
    await _tick_and_settle(dut)

@cocotb.test()
async def run_alu_sim(dut):
    clock = Clock(dut.clk, period=10, unit='ns') # This assigns the clock into the ALU
    cocotb.start_soon(clock.start(start_high=False))

    dut.funct3.value = Funct3.ADD.value
    dut.funct7.value = 0
    dut.s1.value = 0
    dut.s2.value = 0
    await _tick_and_settle(dut)

    dut.s1.value = 0x0F0F00FF
    await perform_not(dut)
    got = int(dut.d.value) & MASK_32
    expected = (~0x0F0F00FF) & MASK_32
    assert got == expected, f"perform_not got 0x{got:08X}, expected 0x{expected:08X}"

    dut.s1.value = 0x00003039
    await perform_negate(dut)
    got = int(dut.d.value) & MASK_32
    expected = (-0x00003039) & MASK_32
    assert got == expected, f"perform_negate got 0x{got:08X}, expected 0x{expected:08X}"

    dut.s1.value = 500
    dut.s2.value = 123
    await perform_sub(dut)
    got = int(dut.d.value) & MASK_32
    expected = (500 - 123) & MASK_32
    assert got == expected, f"perform_sub got 0x{got:08X}, expected 0x{expected:08X}"

    dut.s1.value = 9
    dut.s2.value = 8
    await set_gt(dut)
    assert (int(dut.d.value) & 0x1) == 1

    dut.s1.value = 8
    dut.s2.value = 8
    await set_gt(dut)
    assert (int(dut.d.value) & 0x1) == 0

    dut.s1.value = 9
    dut.s2.value = 8
    await set_gte(dut)
    assert (int(dut.d.value) & 0x1) == 1

    dut.s1.value = 8
    dut.s2.value = 8
    await set_gte(dut)
    assert (int(dut.d.value) & 0x1) == 1

    dut.s1.value = 0x3FC00000
    dut.s2.value = 0x3FC00000
    await f_set_e(dut)
    assert (int(dut.d.value) & 0x1) == 1

    dut.s1.value = 0x3FC00000
    dut.s2.value = 0x40200000
    await f_set_lt(dut)
    assert (int(dut.d.value) & 0x1) == 1

    dut.s1.value = 0x40200000
    dut.s2.value = 0x40200000
    await f_set_lte(dut)
    assert (int(dut.d.value) & 0x1) == 1

    mul_s1 = 0x0000ABCD
    mul_s2 = 0x00000011
    dut.s1.value = mul_s1
    dut.s2.value = mul_s2
    await perform_multiplication(dut)
    got = int(dut.d.value) & MASK_32
    expected = (mul_s1 * mul_s2) & MASK_32
    assert got == expected, f"perform_multiplication got 0x{got:08X}, expected 0x{expected:08X}"

    dut.s1.value = 100
    dut.s2.value = 7
    await perform_division(dut)
    got = int(dut.d.value) & MASK_32
    expected = (100 // 7) & MASK_32
    assert got == expected, f"perform_division got 0x{got:08X}, expected 0x{expected:08X}"


def test_via_cocotb():
    """
    Main entry point for cocotb
    """
    verilog_sources = [os.path.abspath(os.path.join('.', 'alu.v'))]
    runner = get_runner("verilator")
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=[],
        hdl_toplevel="RISCALU",
        build_args=["--threads", "2"],
        build_dir=alu_sim_dir,
    )
    runner.test(hdl_toplevel="RISCALU", test_module="alu_sim")

if __name__ == '__main__':
    test_via_cocotb()
