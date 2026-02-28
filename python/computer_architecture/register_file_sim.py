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
  """
  This function will verify the functionality of back to back load operations
  This functiopn will modify lw x7 and lw x8
  This function will perform two register writes and then conform both registers contain the correct values
  """
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

  await RisingEdge(dut.clk)
  dut.write_enable.value = 0
  dut.rs1.value = 7
  dut.rs2.value = 8
  dut.read_enable.value = 1

  await RisingEdge(dut.clk)
  assert dut.rs1_data.value == temp_memory_one
  assert dut.rs2_data.value == temp_memory_two


@cocotb.test()
async def secnario_back_to_back_alu(dut):
  """
  This function willl verify the alu operations work on two back to back operations
  This function will add x5, x6, and x7 along with x6, x7, asnd x8
  This function will ensure x5 contains x6 + x7
  This function will ensure x6 contains x7 + x8
  """
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))

  x6_init = 10
  x7_init = 20
  x8_init = 3

  dut.read_enable.value = 0
  dut.rd.value = 6
  dut.rd_data.value = x6_init
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rd.value = 7
  dut.rd_data.value = x7_init
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rd.value = 8
  dut.rd_data.value = x8_init
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rs1.value = 6
  dut.rs2.value = 7
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  x6_read = int(dut.rs1_data.value)
  x7_read = int(dut.rs2_data.value)

  dut.rs1.value = 8
  dut.rs2.value = 0
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  x8_read = int(dut.rs1_data.value)

  assert x6_read == x6_init
  assert x7_read == x7_init
  assert x8_read == x8_init

  add1 = x6_read + x7_read

  dut.read_enable.value = 0
  dut.rd.value = 5
  dut.rd_data.value = add1
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rs1.value = 5
  dut.rs2.value = 0
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  x5_read = int(dut.rs1_data.value)
  assert x5_read == add1
  add2 = x7_init + x8_init

  dut.read_enable.value = 0
  dut.rd.value = 6
  dut.rd_data.value = add2
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rs1.value = 5
  dut.rs2.value = 6
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)

  assert int(dut.rs1_data.value) == (x6_init + x7_init)
  assert int(dut.rs2_data.value) == (x7_init + x8_init)


@cocotb.test()
async def secnario_back_to_back_store(dut):
  """
  This function checks the back to back store operations
  This function will initalize the registers x5 and x6
  This funciton will then store values in those reigsters
  This function will then ensure the proper read behavior is occuring for those registers
  """
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))

  mem_at_x10 = 0
  mem_at_x11 = 0
  x5_val = 67
  x6_val = 420

  dut.read_enable.value = 0
  dut.rd.value = 5
  dut.rd_data.value = x5_val
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rd.value = 6
  dut.rd_data.value = x6_val
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rs1.value = 5
  dut.rs2.value = 6
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  assert int(dut.rs1_data.value) == x5_val
  assert int(dut.rs2_data.value) == x6_val

  dut.rs1.value = 10
  dut.rs2.value = 5
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  mem_at_x10 = int(dut.rs2_data.value)

  dut.rs1.value = 11
  dut.rs2.value = 6
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  mem_at_x11 = int(dut.rs2_data.value)

  assert mem_at_x10 == x5_val
  assert mem_at_x11 == x6_val


@cocotb.test()
async def secnario_load_alu_store(dut):
  """
  This function checks the proper execution of the load alu store pipeline
  This function will load a value into x7 then add x5, x6, x7 and store the result in memeory
  This functino will then ensure the proper value is loaded into memory
  """
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))

  mem_at_x10 = 67
  x6_val = 420

  dut.read_enable.value = 0
  dut.rd.value = 6
  dut.rd_data.value = x6_val
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rd.value = 7
  dut.rd_data.value = mem_at_x10
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rs1.value = 6
  dut.rs2.value = 7
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  x6_read = int(dut.rs1_data.value)
  x7_read = int(dut.rs2_data.value)
  assert x6_read == x6_val
  assert x7_read == mem_at_x10

  add_result = x6_read + x7_read

  dut.read_enable.value = 0
  dut.rd.value = 5
  dut.rd_data.value = add_result
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rs1.value = 5
  dut.rs2.value = 0
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  x5_read = int(dut.rs1_data.value)
  assert x5_read == add_result

  dut.rs1.value = 10
  dut.rs2.value = 5 
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  mem_at_x10 = int(dut.rs2_data.value)

  assert mem_at_x10 == add_result


@cocotb.test()
async def secnario_memory_swap(dut):
  """
  This function will ensure the correct properties of the mem swap
  This functino will create two memory location and swap the values using load and store
  This function wil ensure values are loaded into x28 and x29 and also swap the contents
  Then it will make sure the values are unchanged after the swap
  """
  reset_sim(dut)
  clock = Clock(dut.clk, period=10, unit='ns')  # This assigns the clock into the register file
  cocotb.start_soon(clock.start(start_high=False))

  mem_at_x10 = 67
  mem_at_x11 = 420

  dut.read_enable.value = 0
  dut.rd.value = 28
  dut.rd_data.value = mem_at_x10
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rd.value = 29
  dut.rd_data.value = mem_at_x11
  dut.write_enable.value = 1
  await RisingEdge(dut.clk)
  dut.write_enable.value = 0

  dut.rs1.value = 28
  dut.rs2.value = 29
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  x28_read = int(dut.rs1_data.value)
  x29_read = int(dut.rs2_data.value)
  assert x28_read == 67
  assert x29_read == 420

  dut.rs1.value = 11
  dut.rs2.value = 28
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  mem_at_x11 = int(dut.rs2_data.value)

  dut.rs1.value = 10
  dut.rs2.value = 29
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  mem_at_x10 = int(dut.rs2_data.value)

  assert mem_at_x10 == 420
  assert mem_at_x11 == 67

  dut.rs1.value = 28
  dut.rs2.value = 29
  dut.read_enable.value = 1
  await RisingEdge(dut.clk)
  assert int(dut.rs1_data.value) == 67
  assert int(dut.rs2_data.value) == 420


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
