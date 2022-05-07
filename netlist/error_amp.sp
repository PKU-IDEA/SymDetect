.subckt error_amp VDD VSS out vn vp
CC3 out VSS cap
MM24 net9 net114 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM25 net114 net48 net9 VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM26 net17 net114 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM27 net56 net48 net17 VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM19 net64 net64 VDD VDD pfet_lvt nf=1 l=2e-6 w=5e-6
MM16 net72 net72 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM8 net84 net72 VDD VDD pfet_lvt nf=1 l=1e-6 w=20e-6
MM10 net100 net64 net0134 net0134 pfet_lvt nf=1 l=1e-6 w=10e-6
MM9 net0134 net72 VDD VDD pfet_lvt nf=1 l=1e-6 w=20e-6
MM11 out net64 net84 net84 pfet_lvt nf=1 l=1e-6 w=10e-6
MM20 net48 net112 net52 VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM21 net52 net104 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM22 net56 net56 VSS VSS nfet_lvt nf=1 l=4e-6 w=4e-6
MM18 net60 net104 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM17 net64 net112 net60 VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM15 net68 net104 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM14 net72 net112 net68 VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM30 net76 net100 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM1 net0134 vp net77 VDD nfet_lvt nf=1 l=1e-6 w=40e-6
MM2 net84 vn net77 VDD nfet_lvt nf=1 l=1e-6 w=40e-6
MM31 out net56 net92 VDD nfet_lvt nf=1 l=1e-6 w=4e-6
MM32 net92 net100 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM3 net77 net104 VSS VSS nfet_lvt nf=1 l=1e-6 w=8e-6
MM6 net100 net56 net76 VDD nfet_lvt nf=1 l=1e-6 w=4e-6
MM12 net104 net112 net108 VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM13 net108 net104 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
RR0 net112 net104 res 
RR1 net114 net48 res 
.ends error_amp