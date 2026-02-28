// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    , __Vm_threadPoolp{static_cast<VlThreadPool*>(contextp->threadPoolp())}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(250);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-9);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_RISC_REGISTER_FILE = new VerilatedScope{this, "RISC_REGISTER_FILE", "RISC_REGISTER_FILE", "RISC_REGISTER_FILE", -9, VerilatedScope::SCOPE_MODULE};
    __Vscopep_TOP = new VerilatedScope{this, "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    // Set up scope hierarchy
    __Vhier.add(0, __Vscopep_RISC_REGISTER_FILE);
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_RISC_REGISTER_FILE->varInsert("clk", &(TOP.RISC_REGISTER_FILE__DOT__clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("rd", &(TOP.RISC_REGISTER_FILE__DOT__rd), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,4,0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("rd_data", &(TOP.RISC_REGISTER_FILE__DOT__rd_data), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,31,0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("read_enable", &(TOP.RISC_REGISTER_FILE__DOT__read_enable), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("register_file", &(TOP.RISC_REGISTER_FILE__DOT__register_file), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,31 ,31,0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("rs1", &(TOP.RISC_REGISTER_FILE__DOT__rs1), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,4,0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("rs1_data", &(TOP.RISC_REGISTER_FILE__DOT__rs1_data), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,31,0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("rs2", &(TOP.RISC_REGISTER_FILE__DOT__rs2), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,4,0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("rs2_data", &(TOP.RISC_REGISTER_FILE__DOT__rs2_data), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,31,0);
    __Vscopep_RISC_REGISTER_FILE->varInsert("write_enable", &(TOP.RISC_REGISTER_FILE__DOT__write_enable), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("clk", &(TOP.clk), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("rd", &(TOP.rd), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 1 ,4,0);
    __Vscopep_TOP->varInsert("rd_data", &(TOP.rd_data), false, VLVT_UINT32, VLVD_IN|VLVF_PUB_RW, 0, 1 ,31,0);
    __Vscopep_TOP->varInsert("read_enable", &(TOP.read_enable), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("rs1", &(TOP.rs1), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 1 ,4,0);
    __Vscopep_TOP->varInsert("rs1_data", &(TOP.rs1_data), false, VLVT_UINT32, VLVD_OUT|VLVF_PUB_RW, 0, 1 ,31,0);
    __Vscopep_TOP->varInsert("rs2", &(TOP.rs2), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 1 ,4,0);
    __Vscopep_TOP->varInsert("rs2_data", &(TOP.rs2_data), false, VLVT_UINT32, VLVD_OUT|VLVF_PUB_RW, 0, 1 ,31,0);
    __Vscopep_TOP->varInsert("write_enable", &(TOP.write_enable), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
}

Vtop__Syms::~Vtop__Syms() {
    // Tear down scope hierarchy
    __Vhier.remove(0, __Vscopep_RISC_REGISTER_FILE);
    // Clear keys from hierarchy map after values have been removed
    __Vhier.clear();
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_RISC_REGISTER_FILE, __Vscopep_RISC_REGISTER_FILE = nullptr);
    VL_DO_CLEAR(delete __Vscopep_TOP, __Vscopep_TOP = nullptr);
    // Tear down sub module instances
}
