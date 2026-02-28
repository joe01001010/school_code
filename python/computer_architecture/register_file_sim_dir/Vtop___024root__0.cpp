// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

void Vtop___024root___eval_triggers__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered
                                      [0U]) | (IData)((IData)(vlSelfRef.__VicoFirstIteration)));
    vlSelfRef.__VicoFirstIteration = 0U;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
}

bool Vtop___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__ico\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.RISC_REGISTER_FILE__DOT__clk = vlSelfRef.clk;
    vlSelfRef.RISC_REGISTER_FILE__DOT__rd = vlSelfRef.rd;
    vlSelfRef.RISC_REGISTER_FILE__DOT__rd_data = vlSelfRef.rd_data;
    vlSelfRef.RISC_REGISTER_FILE__DOT__write_enable 
        = vlSelfRef.write_enable;
    vlSelfRef.RISC_REGISTER_FILE__DOT__rs1 = vlSelfRef.rs1;
    vlSelfRef.RISC_REGISTER_FILE__DOT__rs2 = vlSelfRef.rs2;
    vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable 
        = vlSelfRef.read_enable;
    vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data = (
                                                   ((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                                                    & (0U 
                                                       != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs1)))
                                                    ? 
                                                   vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
                                                   [vlSelfRef.RISC_REGISTER_FILE__DOT__rs1]
                                                    : 0U);
    vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data = (
                                                   ((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                                                    & (0U 
                                                       != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs2)))
                                                    ? 
                                                   vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
                                                   [vlSelfRef.RISC_REGISTER_FILE__DOT__rs2]
                                                    : 0U);
    vlSelfRef.rs1_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data;
    vlSelfRef.rs2_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data;
}

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered[0U])) {
        vlSelfRef.RISC_REGISTER_FILE__DOT__clk = vlSelfRef.clk;
        vlSelfRef.RISC_REGISTER_FILE__DOT__rd = vlSelfRef.rd;
        vlSelfRef.RISC_REGISTER_FILE__DOT__rd_data 
            = vlSelfRef.rd_data;
        vlSelfRef.RISC_REGISTER_FILE__DOT__write_enable 
            = vlSelfRef.write_enable;
        vlSelfRef.RISC_REGISTER_FILE__DOT__rs1 = vlSelfRef.rs1;
        vlSelfRef.RISC_REGISTER_FILE__DOT__rs2 = vlSelfRef.rs2;
        vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable 
            = vlSelfRef.read_enable;
        vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data 
            = (((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                & (0U != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs1)))
                ? vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
               [vlSelfRef.RISC_REGISTER_FILE__DOT__rs1]
                : 0U);
        vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data 
            = (((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                & (0U != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs2)))
                ? vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
               [vlSelfRef.RISC_REGISTER_FILE__DOT__rs2]
                : 0U);
        vlSelfRef.rs1_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data;
        vlSelfRef.rs2_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data;
    }
}

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = Vtop___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

void Vtop___024root___eval_triggers__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                    ((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__clk) 
                                                     & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__RISC_REGISTER_FILE__DOT__clk__0)))));
    vlSelfRef.__Vtrigprevexpr___TOP__RISC_REGISTER_FILE__DOT__clk__0 
        = vlSelfRef.RISC_REGISTER_FILE__DOT__clk;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
}

bool Vtop___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdlySet__RISC_REGISTER_FILE__DOT__register_file__v0 = 0U;
}

void Vtop___024root__nba_mtask0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__nba_mtask0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Verilated::mtaskId(0);
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        vlSelfRef.__VdlySet__RISC_REGISTER_FILE__DOT__register_file__v0 = 0U;
    }
    Verilated::endOfThreadMTask(vlSymsp->__Vm_evalMsgQp);
}

void Vtop___024root___nba_sequent__TOP__1(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__1\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.RISC_REGISTER_FILE__DOT__write_enable) {
        if ((0U != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rd))) {
            vlSelfRef.__VdlyVal__RISC_REGISTER_FILE__DOT__register_file__v0 
                = vlSelfRef.RISC_REGISTER_FILE__DOT__rd_data;
            vlSelfRef.__VdlyDim0__RISC_REGISTER_FILE__DOT__register_file__v0 
                = vlSelfRef.RISC_REGISTER_FILE__DOT__rd;
            vlSelfRef.__VdlySet__RISC_REGISTER_FILE__DOT__register_file__v0 = 1U;
        }
    }
}

void Vtop___024root__nba_mtask1(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__nba_mtask1\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Verilated::mtaskId(1);
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        if (vlSelfRef.RISC_REGISTER_FILE__DOT__write_enable) {
            if ((0U != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rd))) {
                vlSelfRef.__VdlyVal__RISC_REGISTER_FILE__DOT__register_file__v0 
                    = vlSelfRef.RISC_REGISTER_FILE__DOT__rd_data;
                vlSelfRef.__VdlyDim0__RISC_REGISTER_FILE__DOT__register_file__v0 
                    = vlSelfRef.RISC_REGISTER_FILE__DOT__rd;
                vlSelfRef.__VdlySet__RISC_REGISTER_FILE__DOT__register_file__v0 = 1U;
            }
        }
    }
    Verilated::endOfThreadMTask(vlSymsp->__Vm_evalMsgQp);
}

void Vtop___024root___nba_sequent__TOP__2(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__2\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSelfRef.__VdlySet__RISC_REGISTER_FILE__DOT__register_file__v0) {
        vlSelfRef.RISC_REGISTER_FILE__DOT__register_file[vlSelfRef.__VdlyDim0__RISC_REGISTER_FILE__DOT__register_file__v0] 
            = vlSelfRef.__VdlyVal__RISC_REGISTER_FILE__DOT__register_file__v0;
    }
}

void Vtop___024root__nba_mtask2(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__nba_mtask2\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Verilated::mtaskId(2);
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        if (vlSelfRef.__VdlySet__RISC_REGISTER_FILE__DOT__register_file__v0) {
            vlSelfRef.RISC_REGISTER_FILE__DOT__register_file[vlSelfRef.__VdlyDim0__RISC_REGISTER_FILE__DOT__register_file__v0] 
                = vlSelfRef.__VdlyVal__RISC_REGISTER_FILE__DOT__register_file__v0;
        }
    }
    Verilated::endOfThreadMTask(vlSymsp->__Vm_evalMsgQp);
}

void Vtop___024root___nba_sequent__TOP__3(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__3\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data = (
                                                   ((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                                                    & (0U 
                                                       != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs1)))
                                                    ? 
                                                   vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
                                                   [vlSelfRef.RISC_REGISTER_FILE__DOT__rs1]
                                                    : 0U);
}

void Vtop___024root__nba_mtask3(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__nba_mtask3\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Verilated::mtaskId(3);
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data 
            = (((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                & (0U != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs1)))
                ? vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
               [vlSelfRef.RISC_REGISTER_FILE__DOT__rs1]
                : 0U);
    }
    Verilated::endOfThreadMTask(vlSymsp->__Vm_evalMsgQp);
}

void Vtop___024root___nba_sequent__TOP__4(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__4\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data = (
                                                   ((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                                                    & (0U 
                                                       != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs2)))
                                                    ? 
                                                   vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
                                                   [vlSelfRef.RISC_REGISTER_FILE__DOT__rs2]
                                                    : 0U);
}

void Vtop___024root__nba_mtask4(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__nba_mtask4\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Verilated::mtaskId(4);
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data 
            = (((IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__read_enable) 
                & (0U != (IData)(vlSelfRef.RISC_REGISTER_FILE__DOT__rs2)))
                ? vlSelfRef.RISC_REGISTER_FILE__DOT__register_file
               [vlSelfRef.RISC_REGISTER_FILE__DOT__rs2]
                : 0U);
    }
    Verilated::endOfThreadMTask(vlSymsp->__Vm_evalMsgQp);
}

void Vtop___024root___nba_sequent__TOP__5(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__5\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.rs1_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data;
}

void Vtop___024root__nba_mtask5(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__nba_mtask5\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Verilated::mtaskId(5);
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        vlSelfRef.rs1_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs1_data;
    }
    Verilated::endOfThreadMTask(vlSymsp->__Vm_evalMsgQp);
}

void Vtop___024root___nba_sequent__TOP__6(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__6\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.rs2_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data;
}

void Vtop___024root__nba_mtask6(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__nba_mtask6\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Verilated::mtaskId(6);
    if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
        vlSelfRef.rs2_data = vlSelfRef.RISC_REGISTER_FILE__DOT__rs2_data;
    }
    Verilated::endOfThreadMTask(vlSymsp->__Vm_evalMsgQp);
}

void Vtop___024root____Vthread__nba__s0__t0(void* voidSelf, bool even_cycle);
void Vtop___024root____Vthread__nba__s0__t1(void* voidSelf, bool even_cycle);

void Vtop___024root___eval_nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSymsp->__Vm_even_cycle__nba = !vlSymsp->__Vm_even_cycle__nba;
    vlSymsp->__Vm_threadPoolp->workerp(0)->addTask(&Vtop___024root____Vthread__nba__s0__t0, vlSelf, vlSymsp->__Vm_even_cycle__nba);
    Vtop___024root____Vthread__nba__s0__t1(vlSelf, vlSymsp->__Vm_even_cycle__nba);
    vlSelf->__Vm_mtaskstate_final__0nba.waitUntilUpstreamDone(vlSymsp->__Vm_even_cycle__nba);
    Verilated::mtaskId(0);
}

void Vtop___024root___trigger_orInto__act(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_orInto__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vtop___024root___eval_phase__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vtop___024root___eval_triggers__act(vlSelf);
    Vtop___024root___trigger_orInto__act(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vtop___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vtop___024root___eval_phase__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vtop___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vtop___024root___eval_nba(vlSelf);
        Vtop___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("/home/weibelj/git/school_code/python/computer_architecture/register_file.v", 3, "", "Input combinational region did not converge after 100 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
    } while (Vtop___024root___eval_phase__ico(vlSelf));
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("/home/weibelj/git/school_code/python/computer_architecture/register_file.v", 3, "", "NBA region did not converge after 100 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00000064U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vtop___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("/home/weibelj/git/school_code/python/computer_architecture/register_file.v", 3, "", "Active region did not converge after 100 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
        } while (Vtop___024root___eval_phase__act(vlSelf));
    } while (Vtop___024root___eval_phase__nba(vlSelf));
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.rs1 & 0xe0U)))) {
        Verilated::overWidthError("rs1");
    }
    if (VL_UNLIKELY(((vlSelfRef.rs2 & 0xe0U)))) {
        Verilated::overWidthError("rs2");
    }
    if (VL_UNLIKELY(((vlSelfRef.read_enable & 0xfeU)))) {
        Verilated::overWidthError("read_enable");
    }
    if (VL_UNLIKELY(((vlSelfRef.rd & 0xe0U)))) {
        Verilated::overWidthError("rd");
    }
    if (VL_UNLIKELY(((vlSelfRef.write_enable & 0xfeU)))) {
        Verilated::overWidthError("write_enable");
    }
}
#endif  // VL_DEBUG

void Vtop___024root____Vthread__nba__s0__t0(void* voidSelf, bool even_cycle) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root____Vthread__nba__s0__t0\n"); );
    // Body
    Vtop___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtop___024root*>(voidSelf);
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    Vtop___024root__nba_mtask0((&vlSymsp->TOP));
    Vtop___024root__nba_mtask1((&vlSymsp->TOP));
    Vtop___024root__nba_mtask2((&vlSymsp->TOP));
    vlSelf->__Vm_mtaskstate_4.signalUpstreamDone(even_cycle);
    Vtop___024root__nba_mtask3((&vlSymsp->TOP));
    Vtop___024root__nba_mtask5((&vlSymsp->TOP));
    vlSelf->__Vm_mtaskstate_final__0nba.signalUpstreamDone(even_cycle);
}

void Vtop___024root____Vthread__nba__s0__t1(void* voidSelf, bool even_cycle) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root____Vthread__nba__s0__t1\n"); );
    // Body
    Vtop___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtop___024root*>(voidSelf);
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    vlSelf->__Vm_mtaskstate_4.waitUntilUpstreamDone(even_cycle);
    Vtop___024root__nba_mtask4((&vlSymsp->TOP));
    Vtop___024root__nba_mtask6((&vlSymsp->TOP));
    vlSelf->__Vm_mtaskstate_final__0nba.signalUpstreamDone(even_cycle);
}
