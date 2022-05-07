.subckt DAC dn dp ion iop vrefn vrefp vss_dac
xm11 net09 dn vrefn vss_dac nfet_lvt w=200e-9 l=40e-9 nf=1
xm7 net016 dp vrefn vss_dac nfet_lvt w=200e-9 l=40e-9 nf=1
xm1 net018 net016 vrefn vss_dac nfet_lvt w=400e-9 l=40e-9 nf=1
xm0 net010 net09 vrefn vss_dac nfet_lvt w=400e-9 l=40e-9 nf=1
xm10 net016 dp vrefp vrefp pfet_lvt w=300e-9 l=40e-9 nf=1
xm3 net018 net016 vrefp vrefp pfet_lvt w=600e-9 l=40e-9 nf=1
xm2 net010 net09 vrefp vrefp pfet_lvt w=600e-9 l=40e-9 nf=1
xm12 net09 dn vrefp vrefp pfet_lvt w=300e-9 l=40e-9 nf=1
xr2 iop net018 res
xr0 net010 ion res
.ends DAC
