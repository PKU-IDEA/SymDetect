.subckt OTA_FF_2s_v3 avdd avss ibin in ip on op vcas vcmi
m35 net057 ibin avdd avdd pfet_lvt w=8e-6 l=120e-9 nf=2
m34 cmfb vcmo net057 net057 pfet_lvt w=4e-6 l=120e-9 nf=1
m33 net044 vcmi net057 net057 pfet_lvt w=4e-6 l=120e-9 nf=1
m62 avdd ibin avdd avdd pfet_lvt w=16e-6 l=120e-9 nf=8
m54 net59 net59 net59 net59 pfet_lvt w=12e-6 l=120e-9 nf=6
m43 net5 net5 net5 net5 pfet_lvt w=12e-6 l=120e-9 nf=6
m53 avdd ibin avdd avdd pfet_lvt w=12e-6 l=120e-9 nf=6
m57 avdd ibin avdd avdd pfet_lvt w=16e-6 l=120e-9 nf=8
m37 op in net59 net59 pfet_lvt w=24e-6 l=120e-9 nf=6
m23 on ip net59 net59 pfet_lvt w=24e-6 l=120e-9 nf=6
m63 net75 vcas net75 net75 pfet_lvt w=16e-6 l=120e-9 nf=8
m58 net057 vcmo net057 net057 pfet_lvt w=4e-6 l=120e-9 nf=2
m36 net59 ibin avdd avdd pfet_lvt w=48e-6 l=120e-9 nf=12
m41 avdd ibin avdd avdd pfet_lvt w=12e-6 l=120e-9 nf=6
m16 ibin vcas net75 net75 pfet_lvt w=8e-6 l=120e-9 nf=2
m50 on1 ip net5 net5 pfet_lvt w=8e-6 l=120e-9 nf=2
m48 net057 vcmi net057 net057 pfet_lvt w=12e-6 l=120e-9 nf=6
m6 net75 ibin avdd avdd pfet_lvt w=8e-6 l=120e-9 nf=2
m4 net5 ibin avdd avdd pfet_lvt w=16e-6 l=120e-9 nf=4
m20 op1 in net5 net5 pfet_lvt w=8e-6 l=120e-9 nf=2
m11 avss on1 avss avss nfet_lvt w=8e-6 l=1e-6 nf=4
m10 avss op1 avss avss nfet_lvt w=8e-6 l=1e-6 nf=4
m1 avss avss avss avss nfet_lvt w=6e-6 l=120e-9 nf=6
m0 avss cmfb avss avss nfet_lvt w=6e-6 l=120e-9 nf=6
m66 avss on1 avss avss nfet_lvt w=2e-6 l=120e-9 nf=2
m64 avss op1 avss avss nfet_lvt w=2e-6 l=120e-9 nf=2
m55 avss avss avss avss nfet_lvt w=2e-6 l=120e-9 nf=2
m21 on op1 avss avss nfet_lvt w=6e-6 l=120e-9 nf=6
m19 op on1 avss avss nfet_lvt w=6e-6 l=120e-9 nf=6
m29 cmfb cmfb avss avss nfet_lvt w=1e-6 l=120e-9 nf=1
m14 op1 cmfb avss avss nfet_lvt w=2e-6 l=120e-9 nf=2
m13 on1 cmfb avss avss nfet_lvt w=2e-6 l=120e-9 nf=2
m59 avss net044 avss avss nfet_lvt w=2e-6 l=120e-9 nf=2
m30 net044 net044 avss avss nfet_lvt w=1e-6 l=120e-9 nf=1
m56 avss cmfb avss avss nfet_lvt w=2e-6 l=120e-9 nf=2
xc4 on vcmo avss cap
xc5 op vcmo avss cap
xr12 vcmo op avss res
xr13 on vcmo avss res
.ends OTA_FF_2s_v3