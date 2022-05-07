.subckt COMPARATOR_PRE_AMP clk crossn crossp gnd intern interp outm outp vdd _net0 _net1
xm0 gnd intern gnd gnd nfet_lvt w=1.05e-6 l=1e-6 nf=1
xm22 gnd interp gnd gnd nfet_lvt w=1.05e-6 l=1e-6 nf=1
xm16 outm crossp gnd gnd nfet_lvt w=1.44e-6 l=40e-9 nf=12
xm17 outp crossn gnd gnd nfet_lvt w=1.44e-6 l=40e-9 nf=12
xm4 crossn crossp intern gnd nfet_lvt w=1.92e-6 l=40e-9 nf=16
xm3 crossp crossn interp gnd nfet_lvt w=1.92e-6 l=40e-9 nf=16
xm7 net050 clk gnd gnd nfet_lvt w=8.64e-6 l=40e-9 nf=72
xm5 intern _net0 net050 gnd nfet_lvt w=9.6e-6 l=40e-9 nf=10
xm6 interp _net1 net050 gnd nfet_lvt w=9.6e-6 l=40e-9 nf=10
xm8 outm crossp vdd vdd pfet_lvt w=2.88e-6 l=40e-9 nf=6
xm18 intern clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=1
xm15 outp crossn vdd vdd pfet_lvt w=2.88e-6 l=40e-9 nf=6
xm19 interp clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=1
xm10 crossn clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=1
xm12 crossp clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=1
xm14 crossn crossp vdd vdd pfet_lvt w=3.84e-6 l=40e-9 nf=32
xm13 crossp crossn vdd vdd pfet_lvt w=3.84e-6 l=40e-9 nf=32
.ends COMPARATOR_PRE_AMP

