.subckt feed_forword VB4 VDD VIN VIP VON VOP VSS VTAIL
MM3 VON VB4 VSS VSS nfet_lvt w=10e-6 l=500e-9 nf=12
MM4 VOP VB4 VSS VSS nfet_lvt w=10e-6 l=500e-9 nf=12
MM0 net24 VTAIL VDD VDD pfet_lvt w=12e-6 l=550e-9 nf=50
MM1 VOP VIP net24 VDD pfet_lvt w=12e-6 l=550e-9 nf=40
MM2 VON VIN net24 VDD pfet_lvt w=12e-6 l=550e-9 nf=40
.ends feed_forword