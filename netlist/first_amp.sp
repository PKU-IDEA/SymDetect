.subckt first_amp VB1 VB2 VB3 VDD VIN VIP VO1N VO1P VSS VTAIL
MPM1 net13 VIP net11 VDD pfet_lvt w=15e-6 l=550e-9 nf=25
MPM0 net11 VTAIL VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=45
MPM2 net21 VIN net11 VDD pfet_lvt w=15e-6 l=550e-9 nf=25
MPM6 VO1P VB2 net23 VDD pfet_lvt w=12e-6 l=550e-9 nf=30
MPM3 net35 VB1 VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=30
MPM4 net23 VB1 VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=30
MPM5 VO1N VB2 net35 VDD pfet_lvt w=12e-6 l=550e-9 nf=30
MNM0 VO1N VB3 net13 VSS nfet_lvt w=13.5e-6 l=500e-9 nf=20
MNM3 net13 VO1N VSS VSS nfet_lvt w=13.5e-6 l=500e-9 nf=8
MNM5 net21 VO1N VSS VSS nfet_lvt w=13.5e-6 l=500e-9 nf=8
MNM6 net21 VO1P VSS VSS nfet_lvt w=13.5e-6 l=500e-9 nf=8
MNM1 VO1P VB3 net21 VSS nfet_lvt w=13.5e-6 l=500e-9 nf=20
MNM4 net13 VO1P VSS VSS nfet_lvt w=13.5e-6 l=500e-9 nf=8
.ends first_amp