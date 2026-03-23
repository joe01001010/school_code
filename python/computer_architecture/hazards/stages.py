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
        """
        This function takes 1 argument
        instruction is an Instruction that represents the decoded instruction entering the pipeline
        This function will build the control signals needed for the supported instruction type
        This function will return a ControlSignals
        """
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
        """
        This function takes 0 arguments
        This function will initialize the pipeline state, register file, data memory, and bookkeeping values for the simulator
        This function doesn't return anything
        """
        self.program_counter = 0
        self.counter = 0
        self.last_two_instructions = []
        self.data_memory = {}
        self.registers = [0] * 32
        self.counter_register = 5


    def bubble_entry(self):
        """
        This function takes 0 arguments
        This function will create a nop pipeline entry that represents an empty stage
        This function will return a PipelineEntry
        """
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
        """
        This function takes 1 argument
        entry is a PipelineEntry that represents the stage data being checked for register writes
        This function will determine whether the pipeline entry should write a value into the register file
        This function will return a bool
        """
        return (
            not entry.instruction.is_nop
            and entry.control.reg_write
            and entry.instruction.rd is not None
            and entry.instruction.rd != 0
        )

    def stage_value(self, entry):
        """
        This function takes 1 argument
        entry is a PipelineEntry that represents the stage data being checked for a write-back value
        This function will choose whether the pipeline entry should use memory data or the alu result
        This function will return an int
        """
        if entry.control.wb_sel == "mem":
            return entry.mem_data
        return entry.alu_result

    def resolve_forwarding(self, rs, default_value):
        """
        This function takes 2 arguments
        rs is an int that represents the source register being checked for forwarding
        default_value is an int that represents the original register value before forwarding
        This function will determine whether a forwarded value should replace the default operand value
        This function will return a tuple
        """
        if rs is None or rs == 0:
            return "", default_value

        if self.writes_register(self.ex_mem) and self.ex_mem.instruction.rd == rs:
            if not self.ex_mem.control.mem_rd:
                return "EX/MEM", self.ex_mem.alu_result

        if self.writes_register(self.mem_wb) and self.mem_wb.instruction.rd == rs:
            return "MEM/WB", self.stage_value(self.mem_wb)

        return "", default_value

    def update_last_two_instructions(self, instruction):
        """
        This function takes 1 argument
        instruction is an Instruction that represents the instruction that just executed
        This function will track the last two non-nop instructions seen by the pipeline
        This function doesn't return anything
        """
        if instruction.is_nop:
            return
        self.last_two_instructions.append(instruction)
        if len(self.last_two_instructions) > 2:
            self.last_two_instructions.pop(0)

    def should_stall(self):
        """
        This function takes 0 arguments
        This function will check whether the current instruction in decode must stall because of a load-use hazard
        This function will return a bool
        """
        if self.if_id.instruction.is_nop:
            return False

        current = self.if_id.instruction
        prev = self.id_ex.instruction

        if prev.is_nop or prev.op != "lw" or prev.rd is None:
            return False

        return current.rs1 == prev.rd or current.rs2 == prev.rd


    def write_back(self):
        """
        This function takes 0 arguments
        This function will write the final pipeline result into the register file when the control signals allow it
        This function doesn't return anything
        """
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
        """
        This function takes 0 arguments
        This function will perform the memory stage behavior for loads and stores and build the next memory to write-back pipeline entry
        This function will return a PipelineEntry
        """
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
        """
        This function takes 0 arguments
        This function will perform operand forwarding, alu work, branch comparison, and build the next execute to memory pipeline entry
        This function will return a PipelineEntry
        """
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
        """
        This function takes 1 argument
        branch_taken is a bool that represents whether the current cycle redirected control flow because of a taken branch
        This function will build the decode to execute pipeline entry and decide whether the pipeline must stall
        This function will return a tuple
        """
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
        """
        This function takes 3 arguments
        stalled is a bool that represents whether fetch should hold the current instruction instead of advancing
        branch_taken is a bool that represents whether the current cycle should fetch from a branch target
        branch_target is an int that represents the program counter to fetch from when the branch is taken
        This function will choose the next fetched instruction and compute the next program counter value
        This function will return a tuple
        """
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