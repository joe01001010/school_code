from dataclasses import dataclass
from decoder import Instruction


@dataclass
class ControlSignals:
    reg_write: bool = False
    alu_src: bool = False
    mem_rd: bool = False
    mem_wr: bool = False
    wb_sel: str = "alu"
    bne: bool = False

    @classmethod
    def from_instruction(cls, instruction):
        op = instruction.op

        if op == "lw":
            return cls(reg_write=True, alu_src=True, mem_rd=True, wb_sel="mem")
        if op == "sw":
            return cls(alu_src=True, mem_wr=True)
        if op == "addi":
            return cls(reg_write=True, alu_src=True, wb_sel="alu")
        if op in ("add", "sub", "and", "or"):
            return cls(reg_write=True, alu_src=False, wb_sel="alu")
        if op == "bne":
            return cls(bne=True)

        return cls()


@dataclass
class PipelineEntry:
    instruction: Instruction
    control: ControlSignals
    pc: int = 0
    rs1_val: int = 0
    rs2_val: int = 0
    alu_result: int = 0
    mem_data: int = 0
    store_data: int = 0
    branch_taken: bool = False
    branch_target: int = 0
    fwd_a: str = ""
    fwd_b: str = ""


class Stages:
    PipelineEntry = PipelineEntry
    ControlSignals = ControlSignals

    def __init__(self):
        self.program_counter = 0
        self.counter = 0
        self.last_two_instructions = []
        self.data_memory = {}
        self.registers = [0] * 32
        self.counter_register = 5


    def bubble_entry(self):
        return self.PipelineEntry(
            instruction=Instruction(raw=0, op="nop", is_nop=True),
            control=self.ControlSignals(),
            pc=0,
            rs1_val=0,
            rs2_val=0,
            alu_result=0,
            mem_data=0,
            store_data=0,
            branch_taken=False,
            branch_target=0,
            fwd_a="",
            fwd_b="",
        )

    def writes_register(self, entry):
        return (
            not entry.instruction.is_nop
            and entry.control.reg_write
            and entry.instruction.rd is not None
            and entry.instruction.rd != 0
        )

    def stage_value(self, entry):
        if entry.control.wb_sel == "mem":
            return entry.mem_data
        return entry.alu_result

    def resolve_forwarding(self, rs, default_value):
        if rs is None or rs == 0:
            return "", default_value

        if self.writes_register(self.ex_mem) and self.ex_mem.instruction.rd == rs:
            if not self.ex_mem.control.mem_rd:
                return "EX/MEM", self.ex_mem.alu_result

        if self.writes_register(self.mem_wb) and self.mem_wb.instruction.rd == rs:
            return "MEM/WB", self.stage_value(self.mem_wb)

        return "", default_value

    def update_last_two_instructions(self, instruction):
        if instruction.is_nop:
            return
        self.last_two_instructions.append(instruction)
        if len(self.last_two_instructions) > 2:
            self.last_two_instructions.pop(0)

    def should_stall(self):
        if self.if_id.instruction.is_nop:
            return False

        current = self.if_id.instruction
        prev = self.id_ex.instruction

        if prev.is_nop or prev.op != "lw" or prev.rd is None:
            return False

        return current.rs1 == prev.rd or current.rs2 == prev.rd


    def write_back(self):
        entry = self.mem_wb
        instruction = entry.instruction
        if not self.writes_register(entry):
            return

        result = self.stage_value(entry)
        assert instruction.rd is not None
        self.registers[instruction.rd] = result
        self.registers[0] = 0

        if instruction.rd == self.counter_register:
            self.counter = result


    def memory(self):
        entry = self.ex_mem
        if entry.instruction.is_nop:
            return self.bubble_entry()

        mem_data = entry.mem_data
        if entry.control.mem_rd:
            mem_data = self.data_memory.get(entry.alu_result, 0)
        elif entry.control.mem_wr:
            self.data_memory[entry.alu_result] = entry.store_data

        return self.PipelineEntry(
            instruction=entry.instruction,
            control=entry.control,
            pc=entry.pc,
            rs1_val=entry.rs1_val,
            rs2_val=entry.rs2_val,
            alu_result=entry.alu_result,
            mem_data=mem_data,
            store_data=entry.store_data,
            branch_taken=entry.branch_taken,
            branch_target=entry.branch_target,
            fwd_a=entry.fwd_a,
            fwd_b=entry.fwd_b,
        )


    def execute(self):
        entry = self.id_ex
        instruction = entry.instruction
        if instruction.is_nop:
            return self.bubble_entry()

        fwd_a, operand_a = self.resolve_forwarding(instruction.rs1, entry.rs1_val)
        fwd_b, operand_b = self.resolve_forwarding(instruction.rs2, entry.rs2_val)

        branch_taken = False
        branch_target = entry.pc + (instruction.imm or 0)
        alu_result = 0
        store_data = operand_b

        if instruction.op == "lw":
            alu_result = operand_a + (instruction.imm or 0)
        elif instruction.op == "sw":
            alu_result = operand_a + (instruction.imm or 0)
        elif instruction.op == "addi":
            alu_result = operand_a + (instruction.imm or 0)
        elif instruction.op == "add":
            alu_result = operand_a + operand_b
        elif instruction.op == "sub":
            alu_result = operand_a - operand_b
        elif instruction.op == "and":
            alu_result = operand_a & operand_b
        elif instruction.op == "or":
            alu_result = operand_a | operand_b
        elif instruction.op == "bne":
            branch_taken = operand_a != operand_b
        else:
            raise ValueError(f"Unsupported execute operation: {instruction.op}")

        self.update_last_two_instructions(instruction)

        return self.PipelineEntry(
            instruction=instruction,
            control=entry.control,
            pc=entry.pc,
            rs1_val=entry.rs1_val,
            rs2_val=entry.rs2_val,
            alu_result=alu_result,
            mem_data=0,
            store_data=store_data,
            branch_taken=branch_taken,
            branch_target=branch_target,
            fwd_a=fwd_a,
            fwd_b=fwd_b,
        )

    def decode(self, branch_taken):
        if branch_taken:
            return self.bubble_entry(), False

        if self.should_stall():
            return self.bubble_entry(), True

        instruction = self.if_id.instruction
        if instruction.is_nop:
            return self.bubble_entry(), False

        return self.PipelineEntry(
            instruction=instruction,
            control=self.ControlSignals.from_instruction(instruction),
            pc=self.if_id.pc,
            rs1_val=self.registers[instruction.rs1] if instruction.rs1 is not None else 0,
            rs2_val=self.registers[instruction.rs2] if instruction.rs2 is not None else 0,
        ), False

    def fetch(self, stalled, branch_taken, branch_target):
        if stalled:
            return self.if_id, self.program_counter

        fetch_pc = branch_target if branch_taken else self.program_counter
        instruction = self.instruction_memory.get(fetch_pc)
        if instruction is None:
            return self.bubble_entry(), fetch_pc

        return (
            self.PipelineEntry(
                instruction=instruction,
                control=self.ControlSignals.from_instruction(instruction),
                pc=fetch_pc,
            ),
            fetch_pc + 4,
        )