import re
REGISTER_RE = re.compile(r"x([0-9]|[12][0-9]|3[01])$")


def parse_register(token):
    """
    This function takes 1 argument
    token is a str that represents a register token from assembly text
    This function will strip the token and convert the register name into its numeric register index
    This function will return an int
    """
    token = token.strip()
    match = REGISTER_RE.fullmatch(token)
    return int(match.group(1))


def check_imm(value, bits):
    """
    This function takes 2 arguments
    value is an int that represents an immediate value before masking
    bits is an int that represents the width of the immediate field
    This function will mask the immediate value so it fits within the requested number of bits
    This function will return an int
    """
    return value & ((1 << bits) - 1)


def encode_r_type(funct7, rs2, rs1, funct3, rd, opcode):
    """
    This function takes 6 arguments
    funct7 is an int that represents the funct7 field for the instruction
    rs2 is an int that represents the source register two field
    rs1 is an int that represents the source register one field
    funct3 is an int that represents the funct3 field for the instruction
    rd is an int that represents the destination register field
    opcode is an int that represents the opcode field for the instruction
    This function will assemble the provided R-type fields into a 32-bit instruction word
    This function will return an int
    """
    return (
        ((funct7 & 0x7F) << 25)
        | ((rs2 & 0x1F) << 20)
        | ((rs1 & 0x1F) << 15)
        | ((funct3 & 0x7) << 12)
        | ((rd & 0x1F) << 7)
        | (opcode & 0x7F)
    )


def encode_i_type(imm, rs1, funct3, rd, opcode):
    """
    This function takes 5 arguments
    imm is an int that represents the immediate field for the instruction
    rs1 is an int that represents the source register one field
    funct3 is an int that represents the funct3 field for the instruction
    rd is an int that represents the destination register field
    opcode is an int that represents the opcode field for the instruction
    This function will assemble the provided I-type fields into a 32-bit instruction word
    This function will return an int
    """
    imm = check_imm(imm, 12)
    return (
        (imm << 20)
        | ((rs1 & 0x1F) << 15)
        | ((funct3 & 0x7) << 12)
        | ((rd & 0x1F) << 7)
        | (opcode & 0x7F)
    )


def encode_s_type(imm, rs2, rs1, funct3, opcode):
    """
    This function takes 5 arguments
    imm is an int that represents the immediate field for the instruction
    rs2 is an int that represents the source register two field
    rs1 is an int that represents the base register field
    funct3 is an int that represents the funct3 field for the instruction
    opcode is an int that represents the opcode field for the instruction
    This function will assemble the provided S-type fields into a 32-bit instruction word
    This function will return an int
    """
    imm = check_imm(imm, 12)
    imm_11_5 = (imm >> 5) & 0x7F
    imm_4_0 = imm & 0x1F

    return (
        (imm_11_5 << 25)
        | ((rs2 & 0x1F) << 20)
        | ((rs1 & 0x1F) << 15)
        | ((funct3 & 0x7) << 12)
        | (imm_4_0 << 7)
        | (opcode & 0x7F)
    )


def encode_sb_type(offset, rs2, rs1, funct3, opcode):
    """
    This function takes 5 arguments
    offset is an int that represents the signed branch offset
    rs2 is an int that represents the source register two field
    rs1 is an int that represents the source register one field
    funct3 is an int that represents the funct3 field for the branch instruction
    opcode is an int that represents the opcode field for the branch instruction
    This function will assemble the provided SB-type fields into a 32-bit instruction word
    This function will return an int
    """

    imm = check_imm(offset, 13)
    bit12 = (imm >> 12) & 0x1
    bit11 = (imm >> 11) & 0x1
    bits10_5 = (imm >> 5) & 0x3F
    bits4_1 = (imm >> 1) & 0xF

    return (
        (bit12 << 31)
        | (bits10_5 << 25)
        | ((rs2 & 0x1F) << 20)
        | ((rs1 & 0x1F) << 15)
        | ((funct3 & 0x7) << 12)
        | (bits4_1 << 8)
        | (bit11 << 7)
        | (opcode & 0x7F)
    )


def encode_add(rd: int, rs1: int, rs2: int) -> int:
    """
    This function takes 3 arguments
    rd is an int that represents the destination register for the add instruction
    rs1 is an int that represents the first source register for the add instruction
    rs2 is an int that represents the second source register for the add instruction
    This function will encode an add instruction
    This function will return an int
    """
    return encode_r_type(0x00, rs2, rs1, 0x0, rd, 0x33)


def encode_sub(rd: int, rs1: int, rs2: int) -> int:
    """
    This function takes 3 arguments
    rd is an int that represents the destination register for the sub instruction
    rs1 is an int that represents the first source register for the sub instruction
    rs2 is an int that represents the second source register for the sub instruction
    This function will encode a sub instruction
    This function will return an int
    """
    return encode_r_type(0x20, rs2, rs1, 0x0, rd, 0x33)


def encode_and(rd: int, rs1: int, rs2: int) -> int:
    """
    This function takes 3 arguments
    rd is an int that represents the destination register for the and instruction
    rs1 is an int that represents the first source register for the and instruction
    rs2 is an int that represents the second source register for the and instruction
    This function will encode an and instruction
    This function will return an int
    """
    return encode_r_type(0x00, rs2, rs1, 0x7, rd, 0x33)


def encode_or(rd: int, rs1: int, rs2: int) -> int:
    """
    This function takes 3 arguments
    rd is an int that represents the destination register for the or instruction
    rs1 is an int that represents the first source register for the or instruction
    rs2 is an int that represents the second source register for the or instruction
    This function will encode an or instruction
    This function will return an int
    """
    return encode_r_type(0x00, rs2, rs1, 0x6, rd, 0x33)


def encode_addi(rd: int, rs1: int, imm: int) -> int:
    """
    This function takes 3 arguments
    rd is an int that represents the destination register for the addi instruction
    rs1 is an int that represents the source register for the addi instruction
    imm is an int that represents the immediate value for the addi instruction
    This function will encode an addi instruction
    This function will return an int
    """
    return encode_i_type(imm, rs1, 0x0, rd, 0x13)


def encode_lw(rd: int, rs1: int, imm: int) -> int:
    """
    This function takes 3 arguments
    rd is an int that represents the destination register for the lw instruction
    rs1 is an int that represents the base register for the lw instruction
    imm is an int that represents the byte offset for the lw instruction
    This function will encode an lw instruction
    This function will return an int
    """
    return encode_i_type(imm, rs1, 0x2, rd, 0x03)


def encode_sw(rs2: int, rs1: int, imm: int) -> int:
    """
    This function takes 3 arguments
    rs2 is an int that represents the source register containing the store data
    rs1 is an int that represents the base register for the sw instruction
    imm is an int that represents the byte offset for the sw instruction
    This function will encode an sw instruction
    This function will return an int
    """
    return encode_s_type(imm, rs2, rs1, 0x2, 0x23)


def encode_bne(rs1: int, rs2: int, offset: int) -> int:
    """
    This function takes 3 arguments
    rs1 is an int that represents the first source register for the bne instruction
    rs2 is an int that represents the second source register for the bne instruction
    offset is an int that represents the signed branch offset for the bne instruction
    This function will encode a bne instruction
    This function will return an int
    """
    return encode_sb_type(offset, rs2, rs1, 0x1, 0x63)


def parse_mem_operand(token: str) -> tuple[int, int]:
    """
    This function takes 1 argument
    token is a str that represents a memory operand in offset base register format
    This function will split the memory operand into its immediate offset and base register pieces
    This function will return a tuple
    """
    token = token.strip()
    left = token.index("(")
    right = token.index(")")
    imm = int(token[:left])
    rs1 = parse_register(token[left + 1:right])
    return imm, rs1


def encode_instruction(line, labels = None, pc = 0):
    """
    This function takes 3 arguments
    line is a str that represents one line of assembly code
    labels is a dict that represents the known label addresses for branch encoding
    pc is an int that represents the current program counter for the instruction being encoded
    This function will parse the assembly line and dispatch to the matching encoder for the supported instruction
    This function will return an int
    """
    labels = labels or {}
    line = line.split("#", 1)[0].strip()

    parts = [p.strip() for p in line.replace(",", " ").split()]
    op = parts[0]

    if op == "lw":
        rd = parse_register(parts[1])
        imm, rs1 = parse_mem_operand(parts[2])
        return encode_lw(rd, rs1, imm)

    if op == "sw":
        rs2 = parse_register(parts[1])
        imm, rs1 = parse_mem_operand(parts[2])
        return encode_sw(rs2, rs1, imm)

    if op == "addi":
        rd = parse_register(parts[1])
        rs1 = parse_register(parts[2])
        imm = int(parts[3])
        return encode_addi(rd, rs1, imm)

    if op == "add":
        rd = parse_register(parts[1])
        rs1 = parse_register(parts[2])
        rs2 = parse_register(parts[3])
        return encode_add(rd, rs1, rs2)

    if op == "sub":
        rd = parse_register(parts[1])
        rs1 = parse_register(parts[2])
        rs2 = parse_register(parts[3])
        return encode_sub(rd, rs1, rs2)

    if op == "and":
        rd = parse_register(parts[1])
        rs1 = parse_register(parts[2])
        rs2 = parse_register(parts[3])
        return encode_and(rd, rs1, rs2)

    if op == "or":
        rd = parse_register(parts[1])
        rs1 = parse_register(parts[2])
        rs2 = parse_register(parts[3])
        return encode_or(rd, rs1, rs2)

    if op == "bne":
        rs1 = parse_register(parts[1])
        rs2 = parse_register(parts[2])
        label = parts[3]
        offset = labels[label] - pc
        return encode_bne(rs1, rs2, offset)


def assemble_lines(lines):
    """
    This function takes 1 argument
    lines is a list that represents the assembly program lines to encode
    This function will collect labels and encode each supported instruction line into machine code
    This function will return a list
    """
    labels = {}
    instructions = []
    pc = 0

    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue

        if line.endswith(":"):
            label = line[:-1].strip()
            labels[label] = pc
        else:
            instructions.append(line)
            pc += 4

    encoded = []
    pc = 0
    for line in instructions:
        encoded.append(encode_instruction(line, labels, pc))
        pc += 4

    return encoded


def write_binary_file(encoded_instructions, output_path):
    """
    This function takes 2 arguments
    encoded_instructions is a list that represents the encoded 32-bit instruction words
    output_path is a str that represents the path to the binary output file
    This function will write the encoded instructions to a binary file in little-endian byte order
    This function doesn't return anything
    """
    with open(output_path, "wb") as f:
        for inst in encoded_instructions:
            f.write(inst.to_bytes(4, byteorder="little", signed=False))