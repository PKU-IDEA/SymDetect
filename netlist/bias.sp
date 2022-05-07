.subckt bias VB1 VB2 VB3 VB4 VDD VSS VTAIL
MM0 net10 VTAIL VDD VDD pfet_lvt w=16e-6 l=550e-9 nf=45
MM6 VB2 VB2 net12 VDD pfet_lvt w=2e-6 l=550e-9 nf=30
MM1 net12 VB2 VDD VDD pfet_lvt w=2e-6 l=550e-9 nf=30
MM4 net40 VB1 VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=8
MM7 VB1 VB2 net24 VDD pfet_lvt w=8e-6 l=550e-9 nf=30
MM8 VB3 VB2 net28 VDD pfet_lvt w=12e-6 l=550e-9 nf=8
MM2 net24 VB1 VDD VDD pfet_lvt w=8e-6 l=550e-9 nf=30
MM3 net28 VB1 VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=8
MM9 VB4 VB2 net40 VDD pfet_lvt w=12e-6 l=550e-9 nf=8
MM10 net10 net10 VSS VSS nfet_lvt w=12e-6 l=1e-6 nf=25
MM11 VB2 net10 VSS VSS nfet_lvt w=12e-6 l=1e-6 nf=25
MM12 VB1 net10 VSS VSS nfet_lvt w=12e-6 l=1e-6 nf=25
MM13 VB3 VB3 net67 VSS nfet_lvt w=1e-6 l=500e-9 nf=30
MM16 net63 VB4 VSS VSS nfet_lvt w=1e-6 l=500e-9 nf=60
MM14 net67 VB3 VSS VSS nfet_lvt w=1e-6 l=500e-9 nf=30
MM15 VB4 VB3 net63 VSS nfet_lvt w=1e-6 l=500e-9 nf=60
.ends bias