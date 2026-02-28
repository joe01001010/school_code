// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_threads.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final {
  public:

    // DESIGN SPECIFIC STATE
    VlUnpacked<IData/*31:0*/, 32> RISC_REGISTER_FILE__DOT__register_file;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    CData/*0:0*/ __VdlySet__RISC_REGISTER_FILE__DOT__register_file__v0;
    CData/*4:0*/ __VdlyDim0__RISC_REGISTER_FILE__DOT__register_file__v0;
    IData/*31:0*/ __VdlyVal__RISC_REGISTER_FILE__DOT__register_file__v0;
    CData/*4:0*/ RISC_REGISTER_FILE__DOT__rd;
    CData/*0:0*/ RISC_REGISTER_FILE__DOT__write_enable;
    IData/*31:0*/ RISC_REGISTER_FILE__DOT__rd_data;
    VL_OUT(rs2_data,31,0);
    IData/*31:0*/ RISC_REGISTER_FILE__DOT__rs2_data;
    CData/*4:0*/ RISC_REGISTER_FILE__DOT__rs2;
    CData/*0:0*/ RISC_REGISTER_FILE__DOT__read_enable;
    CData/*4:0*/ RISC_REGISTER_FILE__DOT__rs1;
    IData/*31:0*/ RISC_REGISTER_FILE__DOT__rs1_data;
    VL_OUT(rs1_data,31,0);
    VL_IN8(clk,0,0);
    VL_IN8(rs1,4,0);
    VL_IN8(rs2,4,0);
    VL_IN8(read_enable,0,0);
    VL_IN8(rd,4,0);
    VL_IN8(write_enable,0,0);
    CData/*0:0*/ RISC_REGISTER_FILE__DOT__clk;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__RISC_REGISTER_FILE__DOT__clk__0;
    VL_IN(rd_data,31,0);
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VicoTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlMTaskVertex __Vm_mtaskstate_4;
    VlMTaskVertex __Vm_mtaskstate_final__0nba;

    // INTERNAL VARIABLES
    Vtop__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* namep);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
