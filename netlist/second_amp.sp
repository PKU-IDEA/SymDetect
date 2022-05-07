.subckt second_amp VB1 VDD VFB VO1N VO1P VON VOP VSS
MPM0 VOP VFB VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=100
MPM1 VON VFB VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=100
MM0 net36 VB1 VSS VSS nfet_lvt w=13.5e-6 l=500e-9 nf=100
MNM1 VON VO1P net36 VSS nfet_lvt w=13.5e-6 l=500e-9 nf=100
MNM0 VOP VO1N net36 VSS nfet_lvt w=13.5e-6 l=500e-9 nf=100
.ends second_amp