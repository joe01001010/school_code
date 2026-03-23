#!/usr/bin/env python


import argparse
import csv

from decoder import load_instructions_from_bin
from encoder import write_binary_file, assemble_lines
from stages import Stages


INSTRUCTIONS_UNROLLED = [
        "lw x7, 0(x10)",
        "lw x6, 0(x7)",
        "addi x6, x6, 1",
        "sw x6, 0(x7)",
        "lw x6, 4(x7)",
        "addi x6, x6, 1",
        "sw x6, 4(x7)",
        "lw x6, 8(x7)",
        "addi x6, x6, 1",
        "sw x6, 8(x7)",
    ]
INSTRUCTIONS_HAZARDS = [
    "sub x2, x1, x3",
    "and x12, x2, x5",
    "or x13, x6, x2",
    "and x2, x12, x13",
    "add x14, x2, x2",
]
INSTRUCTIONS_BRANCH = [
    "lw x7, 0(x10)",
    "addi x5, x0, 3",
    "Loop:",
    "lw x6, 0(x7)",
    "addi x6, x6, 1",
    "sw x6, 0(x7)",
    "addi x7, x7, 4",
    "addi x5, x5, -1",
    "bne x5, x0, Loop",
]
INSTRUCTIONS_DYNAMIC = [
    "lw x6, 0(x7)",
    "lw x8, 4(x7)",
    "lw x9, 8(x7)",
    "addi x6, x6, 1",
    "addi x8, x8, 1",
    "addi x9, x9, 1",
    "sw x6, 0(x7)",
    "sw x8, 4(x7)",
    "sw x9, 8(x7)",
]


def pipeline_empty(cpu):
    return (
        cpu.if_id.instruction.is_nop
        and cpu.id_ex.instruction.is_nop
        and cpu.ex_mem.instruction.is_nop
        and cpu.mem_wb.instruction.is_nop
    )


def main(file_path):
    rows = []
    
    if 'unrolled' in file_path:
        encoded = assemble_lines(INSTRUCTIONS_UNROLLED)
    elif 'branch' in file_path:
        encoded = assemble_lines(INSTRUCTIONS_BRANCH)
    elif 'hazards' in file_path:
        encoded = assemble_lines(INSTRUCTIONS_HAZARDS)
    elif 'dynamic' in file_path:
        encoded = assemble_lines(INSTRUCTIONS_DYNAMIC)
        with open("dynamic_re-order.txt", "w") as f:
            for line in INSTRUCTIONS_DYNAMIC:
                f.write(line + "\n")
    else:
        raise SystemExit(f"Program does not have logic to support this file name: {file_path}")

    write_binary_file(encoded, file_path)
    

    instruction_memory = load_instructions_from_bin(file_path)
    cpu = Stages()
    cpu.instruction_memory = instruction_memory
    cpu.if_id = cpu.bubble_entry()
    cpu.id_ex = cpu.bubble_entry()
    cpu.ex_mem = cpu.bubble_entry()
    cpu.mem_wb = cpu.bubble_entry()
    cycle = 0

    while True:
        cpu.write_back()
        next_mem_wb = cpu.memory()
        next_ex_mem = cpu.execute()
        next_id_ex, stalled = cpu.decode(next_ex_mem.branch_taken)
        next_if_id, next_pc = cpu.fetch(stalled, next_ex_mem.branch_taken, next_ex_mem.branch_target)

        cpu.mem_wb = next_mem_wb
        cpu.ex_mem = next_ex_mem
        cpu.id_ex = next_id_ex
        cpu.if_id = next_if_id
        cpu.program_counter = next_pc

        inst = next_ex_mem.instruction
        ctrl = next_ex_mem.control
        rows.append({
            "Cycle": cycle,
            "Instr": inst.raw if not inst.is_nop else "",
            "Op": inst.op if not inst.is_nop else "",
            "Fct3": inst.funct3 if inst.funct3 is not None else "",
            "Rd": inst.rd if inst.rd is not None else "",
            "Rs1": inst.rs1 if inst.rs1 is not None else "",
            "Rs2": inst.rs2 if inst.rs2 is not None else "",
            "RegWrite": ctrl.reg_write,
            "ALUSrc": ctrl.alu_src,
            "FwdA": next_ex_mem.fwd_a,
            "FwdB": next_ex_mem.fwd_b,
            "MemRd": ctrl.mem_rd,
            "MemWr": ctrl.mem_wr,
            "WBSel": ctrl.wb_sel,
            "bne": ctrl.bne,
        })
        cycle += 1

        if cpu.program_counter not in cpu.instruction_memory and pipeline_empty(cpu):
            break

    if "unrolled" in file_path:
        csv_name = "unrolled_simulation.csv"
    elif "branch" in file_path:
        csv_name = "branch_simulation.csv"
    elif "hazards" in file_path:
        csv_name = "hazards_simulation.csv"
    elif "dynamic" in file_path:
        csv_name = "dynamic_simulation.csv"
    else:
        csv_name = "simulation.csv"

    with open(csv_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Cycle", "Instr", "Op", "Fct3", "Rd", "Rs1", "Rs2",
            "RegWrite", "ALUSrc", "FwdA", "FwdB", "MemRd", "MemWr", "WBSel", "bne"
        ])
        writer.writeheader()
        writer.writerows(rows)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=str, required=True)
    args = parser.parse_args()
    main(args.filepath)