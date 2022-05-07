.subckt three_stage_ampfet_lvt VSS IREF VDD VIN+ VIN- VOUT
MPM2 VOUT net224 VOUT VDD pfet_lvt w=10.285e-6 l=10.285e-6 nf=1
MPM6 VOUT net204 VOUT VDD pfet_lvt w=3.43e-6 l=3.43e-6 nf=1
MM18 net200 net200 VSS VSS nfet_lvt l=1e-6 w=1e-6 nf=1
MM11 net204 net228 net256 VSS nfet_lvt l=1e-6 w=1e-6 nf=2
MM14 VOUT net220 VSS VSS nfet_lvt l=1e-6 w=1e-6 nf=1
MM10 net212 net228 net240 VSS nfet_lvt l=1e-6 w=1e-6 nf=2
MM8 net240 net200 VSS VSS nfet_lvt l=1e-6 w=1e-6 nf=2
MM3 net220 net220 VSS VSS nfet_lvt l=1e-6 w=2e-6 nf=1
MM4 net224 net220 VSS VSS nfet_lvt l=1e-6 w=2e-6 nf=1
MM20 net228 net228 net200 VSS nfet_lvt l=1e-6 w=1e-6 nf=1
MM9 net256 net200 VSS VSS nfet_lvt l=1e-6 w=1e-6 nf=2
MM13 net204 net212 VDD VDD pfet_lvt l=1e-6 w=2e-6 nf=1
MM6 net240 net220 net243 VDD pfet_lvt l=1e-6 w=2e-6 nf=2
MM5 net243 IREF VDD VDD pfet_lvt l=1e-6 w=2e-6 nf=8
MM16 IREF IREF VDD VDD pfet_lvt l=1e-6 w=2e-6 nf=1
MM1 net220 VIN+ net255 VDD pfet_lvt l=1e-6 w=2e-6 nf=10
MM7 net256 net224 net243 VDD pfet_lvt l=1e-6 w=2e-6 nf=2
MM2 net224 VIN- net255 VDD pfet_lvt l=1e-6 w=2e-6 nf=10
MM15 VOUT net204 VDD VDD pfet_lvt l=1e-6 w=1e-6 nf=1
MM12 net212 net212 VDD VDD pfet_lvt l=1e-6 w=2e-6 nf=1
MM19 net228 IREF VDD VDD pfet_lvt l=1e-6 w=2e-6 nf=5
MM0 net255 IREF VDD VDD pfet_lvt l=1e-6 w=2e-6 nf=13
.ends three_stage_ampfet_lvt
