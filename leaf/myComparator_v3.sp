.subckt myComparator_v3 clk gnd outm outp vdd _net0 _net1
xm0 gnd intern gnd gnd nfet_lvt w=1.05e-6 l=1e-6 nf=1
xm22 gnd interp gnd gnd nfet_lvt w=1.05e-6 l=1e-6 nf=1
xm16 outm crossp gnd gnd nfet_lvt w=1.44e-6 l=40e-9 nf=4
xm17 outp crossn gnd gnd nfet_lvt w=1.44e-6 l=40e-9 nf=4
xm4 crossn crossp intern gnd nfet_lvt w=1.92e-6 l=40e-9 nf=4
xm3 crossp crossn interp gnd nfet_lvt w=1.92e-6 l=40e-9 nf=4
xm7 net069 clk gnd gnd nfet_lvt w=6.9e-6 l=40e-9 nf=15
xm5 intern _net0 net069 gnd nfet_lvt w=14.4e-6 l=40e-9 nf=15
xm6 interp _net1 net069 gnd nfet_lvt w=14.4e-6 l=40e-9 nf=15
xm8 outm crossp vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=4
xm18 intern clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=4
xm15 outp crossn vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=4
xm2 interp clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=4
xm1 crossn clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=4
xm12 crossp clk vdd vdd pfet_lvt w=1.92e-6 l=40e-9 nf=4
xm14 crossn crossp vdd vdd pfet_lvt w=3.84e-6 l=40e-9 nf=8
xm13 crossp crossn vdd vdd pfet_lvt w=3.84e-6 l=40e-9 nf=8
.ends myComparator_v3