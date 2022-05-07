.subckt NRZ_TRI_DAC_v3_dnw dinn dinnb dinp dinpb ein einb gnd ioutn ioutp vbn1 vbn2 vbp1 vbp2 vcm vdddac
xm20 vdddac vdddac vdddac vdddac pfet w=1.6e-6 l=40e-9 nf=4
xm16 vbp2 vbp2 vbp2 vdddac pfet w=4e-6 l=500e-9 nf=4
xm10 vdddac vdddac vdddac vdddac pfet w=1e-6 l=200e-9 nf=1
xm8 vdddac vdddac vdddac vdddac pfet w=1e-6 l=200e-9 nf=1
xm11 vdddac vdddac vdddac vdddac pfet w=1e-6 l=200e-9 nf=1
xm7 vcm einb vcm2 vdddac pfet w=800e-9 l=40e-9 nf=2
xm2 vcm2 vbp2 v2 vdddac pfet w=4e-6 l=500e-9 nf=4
xm17 ioutp dinnb vcm2 vdddac pfet w=800e-9 l=40e-9 nf=2
xm6 ioutn dinpb vcm2 vdddac pfet w=800e-9 l=40e-9 nf=2
xm9 vdddac vdddac vdddac vdddac pfet w=1e-6 l=200e-9 nf=1
xm3 v2 vbp1 vdddac vdddac pfet w=6e-6 l=1.5e-6 nf=6
xm12 v1 vbn1 gnd gnd nfet w=2.1e-6 l=1.5e-6 nf=6
xm13 vcm1 vbn2 v1 gnd nfet w=4e-6 l=500e-9 nf=4
xm22 gnd gnd gnd gnd nfet w=350e-9 l=200e-9 nf=1
xm24 gnd gnd gnd gnd nfet w=350e-9 l=200e-9 nf=1
xm21 vbn2 vbn2 vbn2 gnd nfet w=4e-6 l=500e-9 nf=4
xm25 gnd gnd gnd gnd nfet w=1e-6 l=200e-9 nf=1
xm23 gnd gnd gnd gnd nfet w=1e-6 l=200e-9 nf=1
xm19 gnd gnd gnd gnd nfet w=800e-9 l=40e-9 nf=4
xm18 ioutp dinp vcm1 gnd nfet w=400e-9 l=40e-9 nf=2
xm15 ioutn dinn vcm1 gnd nfet w=400e-9 l=40e-9 nf=2
xm14 vcm ein vcm1 gnd nfet w=400e-9 l=40e-9 nf=2
.ends NRZ_TRI_DAC_v3_dnw

