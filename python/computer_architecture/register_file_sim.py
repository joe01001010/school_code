import os

import cocotb

from cocotb.clock import Clock
from cocotb_tools.runner import get_runner
from cocotb.triggers import RisingEdge

register_file_sim_dir = os.path.abspath(os.path.join('.', 'register_file_sim_dir'))


def reset_sim(dut):
  dut.write_enable.value = 0
  dut.read_enable.value = 0
  dut.rd.value = 0
  dut.rs1.value = 0
  dut.rs2.value = 0


@cocotb.test()
async def run_register_file_sim(dut):
    clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file

    cocotb.start_soon(clock.start(start_high=False))

    for rdi in range(32):
        await RisingEdge(dut.clk)
        dut.rd.value = rdi
        dut.rd_data.value = rdi
        dut.read_enable.value = 0
        dut.write_enable.value = 1

    await RisingEdge(dut.clk)
    dut.write_enable.value = 0

    rs1_values = []
    rs2_values = []

    for rsi in range(32):
        await RisingEdge(dut.clk)
        dut.rs1.value = rsi
        dut.rs2.value = rsi
        dut.read_enable.value = 1
        rs1_values.append(int(dut.rs1_data.value))
        rs2_values.append(int(dut.rs2_data.value))

    await RisingEdge(dut.clk)
    dut.write_enable.value = 0
    dut.read_enable.value = 0
    # Reset the read register locations for next use
    dut.rs1.value = 0
    dut.rs2.value = 0
    rs1_values.append(int(dut.rs1_data.value))
    rs2_values.append(int(dut.rs2_data.value))

    await RisingEdge(dut.clk)
    dut.write_enable.value = 0
    dut.read_enable.value = 0

    await RisingEdge(dut.clk)
    dut.write_enable.value = 0
    dut.read_enable.value = 0
    rs1_values.append(int(dut.rs1_data.value))
    rs2_values.append(int(dut.rs2_data.value))

    for ii in range(32):  # Note the delay in the results of one clock cycle
        assert rs1_values[ii + 1] == ii
        assert rs2_values[ii + 1] == ii


@cocotb.test()
async def secnario_back_to_back_loads(dut):
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))

  temp_memory_one = 55
  temp_memory_two = 99

  await RisingEdge(dut.clk)
  dut.rd.value = 7
  dut.rd_data.value = temp_memory_one
  dut.write_enable.value = 1
  dut.read_enable.value = 0

  await RisingEdge(dut.clk)
  dut.rd.value = 8
  dut.rd_data.value = temp_memory_two
  dut.write_enable.value = 1


@cocotb.test()
async def secnario_back_to_back_alu(dut):
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))


@cocotb.test()
async def secnario_back_to_back_store(dut):
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))


@cocotb.test()
async def secnario_load_alu_store(dut):
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))


@cocotb.test()
async def secnario_memory_swap(dut):
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))


def test_via_cocotb():
    """
    Main entry point for cocotb
    """
    verilog_sources = [os.path.abspath(os.path.join('.', 'register_file.v'))]
    runner = get_runner("verilator")
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=[],
        hdl_toplevel="RISC_REGISTER_FILE",
        build_args=["--threads", "2"],
        build_dir=register_file_sim_dir,
    )
    runner.test(hdl_toplevel="RISC_REGISTER_FILE", test_module="register_file_sim")


if __name__ == '__main__':
    test_via_cocotb()
