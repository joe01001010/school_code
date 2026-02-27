#!/usr/bin/env python
#
#
# Author: Joe Weibel
# Program: disassembler_assignment.py
# Purpose: This function will read a binary file and assume 32 bit instructions in RISC-V format.
#          This function will then disassemble the machine code into RISC-V assembly code and output the contents to the console and into a text file.
#
# Run instructions:
# 1. Ensure you change the variable in main 'file_to_read' to the correct file path to your file
# 2. pip install -r requirements.txt
# 3. ./disassembler_assignment.py


import numpy as np
import sys


def read_file(file_name, data_type=np.int32):
  """
  This function takes two arguments
  file_name is the path to the file to be read in by numpy using fromFile()
  data_type is an optional argument that will default to int32
  This function attempt to read the file and return the contents
  """
  try:
    return np.fromfile(file_name, dtype=data_type)
  except FileNotFoundError as e:
    print(f"File not found: {file_name}")
    sys.exit(67)


def get_bits(value, start, length):
  """
  This function takes three arguments
  value is the value to get bits from
  start is where we need to start getting bits from
  length is the number of bits we need to grab
  This function will right shift value by start so we are pulling from the right spot
  1 will be left shifted by length, aka multiplying by 2 length times, then subtract 1
  This will then do a logical AND and return the resulting value
  """
  return (value >> start) & ((1 << length) - 1)


def sign_extend(value, bits):
  """
  This function takes two arguments
  value is the value to test if it needs switched to unsigned
  bits is the number of bits to extend to
  This function will first check by left shiftin 1 by the number of bits then logical ANDing with the value
  If it needs extended it will logical OR with -1 left shifted by the number of bits
  else it will just return the value unmodified
  """
  if value & (1 << (bits - 1)):
    return value | ((-1) << bits)
  return value


def decode_load_type(rd, rs1, funct3, imm):
  """
  This function takes 4 arguments
  rd, rs1, funct3, imm are all extracted values from the original instruction that are used to determine the load instruction, then assemble the final instruction
  This function will create a dictionary called load_map that will map the bits to the assembly code
  This function will check if the bit code is in the map and then assemble the string of the load map code and other instruction pieces based on rd and rs1
  This function will return that resulting string or an unknown load string
  """
  """Decode load instructions: opcode=0b0000011"""
  load_map = {
    0b000: "lb",
    0b001: "lh",
    0b010: "lw",
    0b100: "lbu",
    0b101: "lhu",
  }

  if funct3 in load_map:
    return f"{load_map[funct3]} x{rd}, {imm}(x{rs1})"

  print(f"unknown load: funct3={funct3:03b}")
  sys.exit(67)


def decode_i_type(rd, rs1, funct3, imm):
  """
  This function will take 4 arguments: rd, rs1, funct3, imm will all be extracted bits from the original instruction used to map to the assembly for the i type instruction
  This function will return a string of the assembly
  This function sets up an instructions dictionary for mapping bits to the assembly
  This function will first check the funct3 and then also check imm for srai vs srli
  This function will finally check if funct3 is in structions last and then return that assembly code if it is
  """
  instructions = {
    0b000: "addi",
    0b010: "slti",
    0b011: "sltiu",
    0b100: "xori",
    0b110: "ori",
    0b111: "andi",
    0b001: "slli",
    0b101: ("srli", "srai")
  }
  
  if funct3 == 0b001:
    shamt = imm & 0x1F
    return f"slli x{rd}, x{rs1}, {shamt}"
  elif funct3 == 0b101:
    if (imm >> 5) & 1:
      return f"srai x{rd}, x{rs1}, {imm & 0x1F}"
    else:
      return f"srli x{rd}, x{rs1}, {imm & 0x1F}"
  elif funct3 in instructions:
    return f"{instructions[funct3]} x{rd}, x{rs1}, {imm}"
  
  print(f"unknown I-type: funct3={funct3:03b}")
  sys.exit(67)


def decode_s_type(rs1, rs2, funct3, imm):
  """
  This function takes 4 arguments
  rs1, rs2, funct3, imm are all extracted values from the original instruction and will be used to determine the s type instruction assembly
  This function will return a string of the assembly based on the bits that were extracted and sent to this function
  This function will use the store_map dictionary to map the bits to the kind of s type instruction
  """
  store_map = {
    0b000: "sb",
    0b001: "sh",
    0b010: "sw",
  }
  
  if funct3 in store_map:
    return f"{store_map[funct3]} x{rs2}, {imm}(x{rs1})"

  print(f"unknown store: funct3={funct3:03b}")
  sys.exit(67)


def decode_r_type(rd, rs1, rs2, funct3, funct7):
    """
    This function takes five arguments
    This function will take 5 arguments: rd, rs1, rs2, funct3, funct7 that are pulled from the original instruction
    This function will return a string of the assembly based on the bits that were extracted and sent to this function
    This function will use the r_map dictionary to map the bits to the kind of r type instruction
    """
    r_map = {
        (0b0000000, 0b000): "add",
        (0b0100000, 0b000): "sub",
        (0b0000000, 0b001): "sll",
        (0b0000000, 0b010): "slt",
        (0b0000000, 0b011): "sltu",
        (0b0000000, 0b100): "xor",
        (0b0000000, 0b101): "srl",
        (0b0100000, 0b101): "sra",
        (0b0000000, 0b110): "or",
        (0b0000000, 0b111): "and",
    }
    key = (funct7, funct3)
    if key in r_map:
        return f"{r_map[key]} x{rd}, x{rs1}, x{rs2}"
    print(f"unknown R-type: funct7={funct7:07b} funct3={funct3:03b}")
    sys.exit(67)


def decode_b_type(rs1, rs2, funct3, instruction):
  """
  This function takes 4 arguments
  rs1 is the rs1 bit code pulled from the instruction
  rs2 is the same concept as rs1
  same for funct3
  the full instruction is also sent for decoding the b type immediate instruction bits
  This function will extract the immediate bits and do a sign extension
  The branch_map is a dictionary to map the funct3 code to the assembly
  This function will return the branch map with the codes for rs1 rs2 and immediate as a string value
  """
  imm_11 = (instruction >> 7) & 0x1
  imm_4_1 = (instruction >> 8) & 0xF
  imm_10_5 = (instruction >> 25) & 0x3F
  imm_12 = (instruction >> 31) & 0x1
  
  imm = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
  if imm & 0x1000:
    imm |= 0xFFFFE000
  imm = sign_extend(imm, 13)
  
  branch_map = {
    0b000: "beq",
    0b001: "bne",
    0b100: "blt",
    0b101: "bge",
    0b110: "bltu",
    0b111: "bgeu",
  }
  
  if funct3 in branch_map:
    return f"{branch_map[funct3]} x{rs1}, x{rs2}, {imm}"

  print(f"unknown branch: funct3={funct3:03b}") 
  sys.exit(67)


def decode_instruction(instruction):
  """
  This function takes an instruction as an argument
  This function will return the decoding of the instruction in assembly format
  This function will first break the instruction apart using right shifts and extracting the value using logical AND operations
  This function will the pull the immediate bit and sign extend to 12 bits
  If it is an s type instruction it will pull the immediate bits and sign extend
  This function will then decode off of the opcode and funct3 bit sections
  This function will call the appropriate decoding function for the kind of instruction and return the assembly
  """
  # Take the instruction and shift if needed and then do a logical AND with all ones for the bits we care about to extract
  opcode = instruction & (2**7 - 1)
  rd     = (instruction >> 7) & (2**5 - 1)
  funct3 = (instruction >> 12) & (2**3 - 1)
  rs1    = (instruction >> 15) & (2**5 - 1)
  rs2    = (instruction >> 20) & (2**5 - 1)
  funct7 = (instruction >> 25) & (2**7 - 1)

  imm_i = instruction >> 20
  imm_i = sign_extend(imm_i, 12)
  if imm_i & 0x800:
    imm_i |= 0xFFFFF000

  imm_s = (get_bits(instruction, 25, 7) << 5) | get_bits(instruction, 7, 5)
  if imm_s & 0x800:
    imm_s |= 0xFFFFF000

  if opcode == 0b0110011:
    return decode_r_type(rd, rs1, rs2, funct3, funct7)
  elif opcode == 0b0010011:
    return decode_i_type(rd, rs1, funct3, imm_i)
  elif opcode == 0b0000011:
    return decode_load_type(rd, rs1, funct3, imm_i)
  elif opcode == 0b0100011:
    return decode_s_type(rs1, rs2, funct3, imm_s)
  elif opcode == 0b1100011:
    return decode_b_type(rs1, rs2, funct3, instruction)
  else:
    print(f"unknown: {opcode:07b}")
    sys.exit(67)


def main():
  """
  This function takes no arguments and doesnt return anything
  This is the main logic for the program and will read the binary file
  This function will iterate over the instructions while keeping track of the iterations as well
  This function will then call decode instruction and send the instruction as an argument
  This function will then take the response and output the disassembled instructions in a format of RISC-V assembly
  This function will also output the assembly instructions into a txt file
  """
  file_to_read  = 'risc-v_instructions.bin'
  file_to_write = 'risc-v_instructions.txt'
  instructions = read_file(file_to_read)

  if len(instructions) < 1:
    print(f"{file_to_read} was found but had no instructions to decode. Exiting with 0")
    sys.exit(0)

  print(f"Beginning disassembly of instructions from {file_to_read}", end='\n\n')

  with open(file_to_write, 'w', encoding='utf-8') as write_file:
    write_file.write(f'RISC-V assembly instructions from {file_to_read}\n')

  for index, instruction in enumerate(instructions):
    instruction = int(instruction)
    if instruction < 0:
      instruction = instruction & (2**32 - 1)

    assembly = decode_instruction(instruction)
    print(f"0x{index*4:08x}: 0x{instruction:08x} {assembly}")

    with open(file_to_write, 'a', encoding='utf-8') as write_file:
      write_file.write(f"0x{index*4:08x}: 0x{instruction:08x} {assembly}\n")
  print()

  print(f"All instructions from {file_to_read} disassembled successfully.")
  print("Ending program with code 0")
  sys.exit(0)

if __name__ == '__main__':
  main()
