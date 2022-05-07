.subckt Gm1_v5_Practice ibias vdd vim vip vom vop vss
xm8 net074 ntail1 vss vss nfet_lvt w=3.22e-6 l=120e-9 nf=4
xm2 vdd ibias vdd vdd pfet_lvt w=2.95e-6 l=3.3e-6 nf=1
xm4 vdd ibias vdd vdd pfet_lvt w=2.95e-6 l=3.3e-6 nf=1
xm12 ibias ibias vdd vdd pfet_lvt w=585e-9 l=120e-9 nf=1
xm11 vom ibias vdd vdd pfet_lvt w=2.34e-6 l=120e-9 nf=4
xm15 ibias ibias vdd vdd pfet_lvt w=585e-9 l=120e-9 nf=1
xm14 vop ibias vdd vdd pfet_lvt w=2.34e-6 l=120e-9 nf=4
xm26 vop vim net074 net074 nfet_lvt w=1.7e-6 l=120e-9 nf=4
xm27 vom vip net074 net074 nfet_lvt w=1.7e-6 l=120e-9 nf=4
xc21 ntail1 vom vss cap
xc22 vop ntail1 vss cap
xr12 ntail1 vop vss res
xr11 vom ntail1 vss res
xm3 vss ntail1 vss vss nfet_lvt w=2.5e-6 l=2.2e-6 nf=1
xm0 vss ntail1 vss vss nfet_lvt w=2.5e-6 l=2.2e-6 nf=1
d0 net074 vdd diode
d1 vss vdd diode
.ends Gm1_v5_Practice

