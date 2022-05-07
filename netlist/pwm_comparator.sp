.subckt pwm_comparator VDD VSS out_pwm vn_pwm vp_pwm
MM0 net47 net13 VSS VSS nfet_lvt nf=2 l=1e-6 w=4e-6
MM13 net13 net13 VSS VSS nfet_lvt nf=2 l=1e-6 w=4e-6
MM3 net47 net47 net13 net13 nfet_lvt nf=1 l=1e-6 w=4e-6
MM6 net20 net20 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM7 net20 net13 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM8 net33 net33 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM9 net33 net13 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM10 net37 net33 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM14 net41 net20 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM17 out_pwm net41 VSS VSS nfet_lvt nf=1 l=1e-6 w=4e-6
MM16 net13 net47 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM1 net47 net47 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM2 net61 net47 VDD VDD pfet_lvt nf=1 l=1e-6 w=20e-6
MM4 net20 vp_pwm net61 net61 pfet_lvt nf=1 l=1e-6 w=40e-6
MM5 net33 vn_pwm net61 net61 pfet_lvt nf=1 l=1e-6 w=40e-6
MM11 net37 net37 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM12 net41 net37 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
MM15 out_pwm net41 VDD VDD pfet_lvt nf=1 l=1e-6 w=10e-6
.ends pwm_comparator

