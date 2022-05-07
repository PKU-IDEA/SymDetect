.subckt Comparator_1to7_0p7_lvt caln calp clke d db inm<0> inm<1> inp<0> inp<1> vb vdd vss
xm29 vout1p clk vdd vdd pfet_lvt w=1.6e-6 l=40e-9 nf=2
xm32 vout1m clk vdd vdd pfet_lvt w=1.6e-6 l=40e-9 nf=2
xm18 clk net043 vdd vdd pfet_lvt w=3.2e-6 l=40e-9 nf=4
xm19 net043 clke vdd vdd pfet_lvt w=800e-9 l=40e-9 nf=2
xm7 db vout2p vdd vdd pfet_lvt w=600e-9 l=40e-9 nf=1
xm28 vout2p vout2m vdd vdd pfet_lvt w=12.8e-6 l=120e-9 nf=8
xm38 vdd vss vdd vdd pfet_lvt w=800e-9 l=40e-9 nf=2
xm39 vdd vss vdd vdd pfet_lvt w=3.2e-6 l=40e-9 nf=4
xm34 vout2m vout2p vdd vdd pfet_lvt w=12.8e-6 l=120e-9 nf=8
xm25 vout2p clk vdd vdd pfet_lvt w=800e-9 l=40e-9 nf=2
xm8 d vout2m vdd vdd pfet_lvt w=600e-9 l=40e-9 nf=1
xm33 vout2m clk vdd vdd pfet_lvt w=800e-9 l=40e-9 nf=2
xm35 net058 clk net040 vss nfet_lvt w=1e-6 l=40e-9 nf=1
xm10 vout1m inp<0> net058 vss nfet_lvt w=1.2e-6 l=200e-9 nf=1
xm36 net040 vb vss vss nfet_lvt w=1e-6 l=40e-9 nf=1
xm9 d vout2m vss vss nfet_lvt w=400e-9 l=40e-9 nf=1
xm48 vss vdd vss vss nfet_lvt w=2.4e-6 l=160e-9 nf=2
xm41 vss vdd vss vss nfet_lvt w=400e-9 l=40e-9 nf=2
xm43 vss vdd vss vss nfet_lvt w=6e-6 l=40e-9 nf=6
xm42 vss vdd vss vss nfet_lvt w=800e-9 l=40e-9 nf=2
xm11 vout1p inm<0> net058 vss nfet_lvt w=1.2e-6 l=200e-9 nf=1
xm26 clk net043 vss vss nfet_lvt w=800e-9 l=40e-9 nf=2
xm14 vout2p vout2m vout1p vss nfet_lvt w=6.4e-6 l=120e-9 nf=8
xm12 vout1p inm<1> net057 vss nfet_lvt w=1.2e-6 l=200e-9 nf=1
xm37 net041 vb vss vss nfet_lvt w=1e-6 l=40e-9 nf=1
xm40 net057 clk net041 vss nfet_lvt w=1e-6 l=40e-9 nf=1
xm6 db vout2p vss vss nfet_lvt w=400e-9 l=40e-9 nf=1
xm27 net043 clke vss vss nfet_lvt w=400e-9 l=40e-9 nf=2
xm13 vout1m inp<1> net057 vss nfet_lvt w=1.2e-6 l=200e-9 nf=1
xm21 vout2m vout2p vout1m vss nfet_lvt w=6.4e-6 l=120e-9 nf=8
m1 vout2m calp vout2m vout2m pfet_lvt w=16e-6 l=500e-9 nf=2
m2 vout2p vss vout2p vout2p pfet_lvt w=64e-6 l=500e-9 nf=8
m3 vout2p caln vout2p vout2p pfet_lvt w=16e-6 l=500e-9 nf=2
m0 vout2m vss vout2m vout2m pfet_lvt w=64e-6 l=500e-9 nf=8
.ends Comparator_1to7_0p7_lvt

