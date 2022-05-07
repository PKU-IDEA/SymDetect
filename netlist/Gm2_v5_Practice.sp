.subckt Gm2_v5_Practice ibias vdd vim vip vom vop vss
xm20 vdd ibias vdd vdd pfet_lvt w=2.8e-6 l=3.6e-6 nf=1
xm18 vdd ibias vdd vdd pfet_lvt w=2.8e-6 l=3.6e-6 nf=1
xm13 vop vim net100 net100 nfet_lvt w=1.16e-6 l=160e-9 nf=4
xm21 vom vip net100 net100 nfet_lvt w=1.16e-6 l=160e-9 nf=4
xm0 ibias ibias vdd vdd pfet_lvt w=700e-9 l=160e-9 nf=2
xm24 ibias ibias vdd vdd pfet_lvt w=700e-9 l=160e-9 nf=2
xm23 vop ibias vdd vdd pfet_lvt w=1.4e-6 l=160e-9 nf=4
xm14 vom ibias vdd vdd pfet_lvt w=1.4e-6 l=160e-9 nf=4
xc22 vop ntail2 vss cap
xc21 ntail2 vom vss cap
xr11 vom ntail2 vss res
xr12 ntail2 vop vss res
xm22 net100 ntail2 vss vss nfet_lvt w=3.12e-6 l=160e-9 nf=4
d1 vss vdd diode
xm12 vss ntail2 vss vss nfet_lvt w=2.1e-6 l=2.2e-6 nf=1
xm11 vss ntail2 vss vss nfet_lvt w=2.1e-6 l=2.2e-6 nf=1
d0 net100 vdd diode
.ends Gm2_v5_Practice