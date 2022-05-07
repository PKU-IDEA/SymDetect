.subckt CP_branch_LVT_v5 dn dnb iout up upb vbn_cm vbn_cs vbp_cm vbp_cs vdd vdm vss vss_sub
xm41 vdm up net38 vdd pfet w=800e-9 l=40e-9 nf=4
xm39 iout upb net38 vdd pfet w=800e-9 l=40e-9 nf=4
xm3 vdm dnb net37 vss nfet w=800e-9 l=40e-9 nf=4
xm4 iout dn net37 vss nfet w=800e-9 l=40e-9 nf=4
xm10 net41 vbn_cm vss vss nfet_lvt w=2.2e-6 l=2e-6 nf=2
xm9 net37 vbn_cs net41 vss nfet_lvt w=2e-6 l=80e-9 nf=4
xm13 net40 vbp_cm vdd vdd pfet_lvt w=11.4e-6 l=2e-6 nf=2
xm36 net38 vbp_cs net40 vdd pfet_lvt w=11.2e-6 l=80e-9 nf=8
.ends CP_branch_LVT_v5

