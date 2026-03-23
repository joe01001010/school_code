import re
REGISTER_RE = re.compile(r"x([0-9]|[12][0-9]|3[01])$")


def parse_register(token):
    token = token.strip()
    match = REGISTER_RE.fullmatch(token)
    return int(match.group(1))


def check_imm(value, bits):
    return value & ((1 << bits) - 1)


def encode_r_type(funct7, rs2, rs1, funct3, rd, opcode):
    return (
        ((funct7 & 0x7F) << 25)
        | ((rs2 & 0x1F) << 20)
        | ((rs1 & 0x1F) << 15)
        | ((funct3 & 0x7) << 12)
        | ((rd & 0x1F) << 7)
        | (opcode & 0x7F)
    )


def encode_i_type(imm, rs1, funct3, rd, opcode):
    imm = check_imm(imm, 12)
    return (
        (imm << 20)
        | ((rs1 & 0x1F) << 15)
        | ((funct3 & 0x7) << 12)
        | ((rd & 0x1F) << 7)
        | (opcode & 0x7F)
    )


def encode_s_type(imm, rs2, rs1, funct3, opcode):
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
    return encode_r_type(0x00, rs2, rs1, 0x0, rd, 0x33)


def encode_sub(rd: int, rs1: int, rs2: int) -> int:
    return encode_r_type(0x20, rs2, rs1, 0x0, rd, 0x33)


def encode_and(rd: int, rs1: int, rs2: int) -> int:
    return encode_r_type(0x00, rs2, rs1, 0x7, rd, 0x33)


def encode_or(rd: int, rs1: int, rs2: int) -> int:
    return encode_r_type(0x00, rs2, rs1, 0x6, rd, 0x33)


def encode_addi(rd: int, rs1: int, imm: int) -> int:
    return encode_i_type(imm, rs1, 0x0, rd, 0x13)


def encode_lw(rd: int, rs1: int, imm: int) -> int:
    return encode_i_type(imm, rs1, 0x2, rd, 0x03)


def encode_sw(rs2: int, rs1: int, imm: int) -> int:
    return encode_s_type(imm, rs2, rs1, 0x2, 0x23)


def encode_bne(rs1: int, rs2: int, offset: int) -> int:
    return encode_sb_type(offset, rs2, rs1, 0x1, 0x63)


def parse_mem_operand(token: str) -> tuple[int, int]:
    token = token.strip()
    left = token.index("(")
    right = token.index(")")
    imm = int(token[:left])
    rs1 = parse_register(token[left + 1:right])
    return imm, rs1


def encode_instruction(line, labels = None, pc = 0):
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
    with open(output_path, "wb") as f:
        for inst in encoded_instructions:
            f.write(inst.to_bytes(4, byteorder="little", signed=False))