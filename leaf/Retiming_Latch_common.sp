.subckt Retiming_Latch_common clkb d do dob vdd_d vss_d
xm39 net025 net017 vdd_d vdd_d pfet_lvt w=480e-9 l=40e-9 nf=1
xm31 clk clkb vdd_d vdd_d pfet_lvt w=480e-9 l=40e-9 nf=1
xm33 vdd_d vss_d vdd_d vdd_d pfet_lvt w=480e-9 l=40e-9 nf=1
xm16 do dob vdd_d vdd_d pfet_lvt w=320e-9 l=40e-9 nf=1
xm26 clkn clk vdd_d vdd_d pfet_lvt w=480e-9 l=40e-9 nf=1
xm12 dob do vdd_d vdd_d pfet_lvt w=320e-9 l=40e-9 nf=1
xm1 do clkn net36 vdd_d pfet_lvt w=640e-9 l=40e-9 nf=1
xm0 net36 net025 vdd_d vdd_d pfet_lvt w=640e-9 l=40e-9 nf=1
xm11 dob clkn net39 vdd_d pfet_lvt w=640e-9 l=40e-9 nf=1
xm10 net39 net017 vdd_d vdd_d pfet_lvt w=640e-9 l=40e-9 nf=1
xm37 net017 d vdd_d vdd_d pfet_lvt w=480e-9 l=40e-9 nf=1
xm35 vdd_d vss_d vdd_d vdd_d pfet_lvt w=480e-9 l=40e-9 nf=1
xm38 net025 net017 vss_d vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
xm30 clk clkb vss_d vss_d nfet_lvt w=240e-9 l=40e-9 nf=1
xm17 do clk net37 vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
xm32 vdd_d vss_d vdd_d vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
xm27 clkn clk vss_d vss_d nfet_lvt w=240e-9 l=40e-9 nf=1
xm13 dob clk net38 vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
xm36 net017 d vss_d vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
xm21 dob do vss_d vss_d nfet_lvt w=160e-9 l=40e-9 nf=1
xm20 do dob vss_d vss_d nfet_lvt w=160e-9 l=40e-9 nf=1
xm19 net38 net017 vss_d vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
xm34 vdd_d vss_d vdd_d vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
xm18 net37 net025 vss_d vss_d nfet_lvt w=320e-9 l=40e-9 nf=1
.ends Retiming_Latch_common
