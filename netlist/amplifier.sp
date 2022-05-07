.subckt amplifier V+ V- VDD VSS Vout ibilas
XC net062 Vout cap
MMA9 net068 ibilas VSS VSS nfet_lvt_lvt w=8.8e-6 l=2e-6 nf=9
MMA10 ibilas ibilas VSS VSS nfet_lvt_lvt w=8.8e-6 l=2e-6 nf=9
MMA7 Vout net062 VSS VSS nfet_lvt_lvt w=8.8e-6 l=2e-6 nf=9
MMA3 net066 net066 VSS VSS nfet_lvt_lvt w=11e-6 l=1.4e-6 nf=3
MMA4 net062 net066 VSS VSS nfet_lvt_lvt w=11e-6 l=1.4e-6 nf=3
MMA1 net066 V- net0135 VDD pfet_lvt w=20e-6 l=1e-6 nf=1
MMA2 net062 V+ net0135 VDD pfet_lvt w=20e-6 l=1e-6 nf=1
MMA8 net068 net068 VDD VDD pfet_lvt w=5e-6 l=2e-6 nf=8
MMA5 net0135 net068 VDD VDD pfet_lvt w=5e-6 l=2e-6 nf=8
MMA6 Vout net068 VDD VDD pfet_lvt w=5e-6 l=2e-6 nf=8
.ends amplifier



