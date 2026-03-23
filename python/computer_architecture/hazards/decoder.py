from dataclasses import dataclass


@dataclass
class Instruction:
    raw: int
    op: str
    rd: int | None = None
    rs1: int | None = None
    rs2: int | None = None
    funct3: int | None = None
    funct7: int | None = None
    imm: int | None = None
    is_nop: bool = False


def sign_extend(value, bits):
    """
    This function takes 2 arguments
    value is an int that represents the immediate value before sign extension
    bits is an int that represents the number of bits in the original immediate field
    This function will convert the provided immediate value into its signed integer form
    This function will return an int
    """
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)


def decode_instruction(inst):
    """
    This function takes 1 argument
    inst is an int that represents a 32-bit RISC-V instruction word
    This function will decode the instruction bits into an Instruction dataclass for the supported operations
    This function will return an Instruction
    """
    opcode = inst & 0x7F
    rd = (inst >> 7) & 0x1F
    funct3 = (inst >> 12) & 0x7
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    funct7 = (inst >> 25) & 0x7F

    if opcode == 0x33:
        if funct3 == 0x0 and funct7 == 0x00:
            return Instruction(inst, "add", rd=rd, rs1=rs1, rs2=rs2, funct3=funct3, funct7=funct7)
        if funct3 == 0x0 and funct7 == 0x20:
            return Instruction(inst, "sub", rd=rd, rs1=rs1, rs2=rs2, funct3=funct3, funct7=funct7)
        if funct3 == 0x7 and funct7 == 0x00:
            return Instruction(inst, "and", rd=rd, rs1=rs1, rs2=rs2, funct3=funct3, funct7=funct7)
        if funct3 == 0x6 and funct7 == 0x00:
            return Instruction(inst, "or", rd=rd, rs1=rs1, rs2=rs2, funct3=funct3, funct7=funct7)

    elif opcode == 0x13:
        imm = sign_extend((inst >> 20) & 0xFFF, 12)
        if funct3 == 0x0:
            return Instruction(inst, "addi", rd=rd, rs1=rs1, funct3=funct3, imm=imm)

    elif opcode == 0x03:
        imm = sign_extend((inst >> 20) & 0xFFF, 12)
        if funct3 == 0x2:
            return Instruction(inst, "lw", rd=rd, rs1=rs1, funct3=funct3, imm=imm)

    elif opcode == 0x23:
        imm = ((inst >> 25) << 5) | ((inst >> 7) & 0x1F)
        imm = sign_extend(imm, 12)
        if funct3 == 0x2:
            return Instruction(inst, "sw", rs1=rs1, rs2=rs2, funct3=funct3, imm=imm)

    elif opcode == 0x63:
        imm12 = (inst >> 31) & 0x1
        imm10_5 = (inst >> 25) & 0x3F
        imm4_1 = (inst >> 8) & 0xF
        imm11 = (inst >> 7) & 0x1
        imm = (imm12 << 12) | (imm11 << 11) | (imm10_5 << 5) | (imm4_1 << 1)
        imm = sign_extend(imm, 13)
        if funct3 == 0x1:
            return Instruction(inst, "bne", rs1=rs1, rs2=rs2, funct3=funct3, imm=imm)

    raise ValueError(f"Unsupported instruction: 0x{inst:08x}")


def load_instructions_from_bin(file_path):
    """
    This function takes 1 argument
    file_path is a str that represents the path to the binary instruction file
    This function will read the binary file four bytes at a time and load the decoded instructions into instruction memory
    This function will return a dict
    """
    instruction_memory = {}

    with open(file_path, "rb") as f:
        pc = 0
        while True:
            chunk = f.read(4)
            if not chunk:
                break
            if len(chunk) != 4:
                raise ValueError("Binary file ended with incomplete instruction")
            inst = int.from_bytes(chunk, byteorder="little", signed=False)
            instruction_memory[pc] = decode_instruction(inst)
            pc += 4

    return instruction_memory