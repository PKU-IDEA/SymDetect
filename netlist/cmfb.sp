.subckt cmfb VDD VFB VON VOP VREF VSS VTAIL
MM3 VFB net18 VSS VSS nfet_lvt w=10e-6 l=2e-6 nf=6
MM4 net18 net18 VSS VSS nfet_lvt w=10e-6 l=2e-6 nf=6
MM2 VFB VREF net25 VDD pfet_lvt w=10e-6 l=2.2e-6 nf=10
MM0 net25 VTAIL VDD VDD pfet_lvt w=10e-6 l=2.2e-6 nf=10
MM1 net18 net10 net25 VDD pfet_lvt w=10e-6 l=2.2e-6 nf=10
XR2 VON net10 res nf=1 w=290e-9 l=7.69e-6
XR1 VOP net10 res nf=1 w=290e-9 l=7.69e-6
XR0 net10 VSS res nf=1 w=290e-9 l=7.69e-6
.ends cmfb