##
# @file   run.sh
# @author Yibo Lin
# @date   Jan 2020
#
#!/bin/bash

python3 netlist2graph.py \
    netlist/NRZ_TRI_DAC_v3_dnw.sp \
    netlist/COMPARATOR_PRE_AMP.sp \
    netlist/Comparator_1to7_0p7_lvt.sp \
    netlist/OTA_FF_2s_v3e.sp \
    netlist/CP_branch_LVT_v5.sp \
    netlist/Gm1_v5_Practice.sp \
    netlist/CLK_COMP.sp \
    netlist/DAC.sp \
    netlist/myComparator_v3.sp \
    netlist/Retiming_Latch_common.sp \
    netlist/2019_10_01_5t_OTA.sp \
    netlist/Cascode_current_mirrot_OTA.sp \
    netlist/Comparator_not_clocked.sp \
    netlist/Current_mirror_OTA.sp \
    netlist/Telescopic_OTA_stacked_single_ended.sp  
