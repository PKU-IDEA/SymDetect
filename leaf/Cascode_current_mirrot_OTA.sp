.subckt Cascode_current_mirrot_OTA voutp gnd vbiasn vbiasnd vinn vinp vbiasp vdd!
m25 voutp vbiasn net034 gnd nmos w=27e-9 l=20e-9 nf=24
m24 vbiasnd vbiasn net033 gnd nmos w=27e-9 l=20e-9 nf=24
m17 net16 vinn net24 gnd nmos w=27e-9 l=20e-9 nf=30
m16 net24 net17 gnd gnd nmos w=27e-9 l=20e-9 nf=15
m15 net27 vinp net24 gnd nmos w=27e-9 l=20e-9 nf=30
m14 net17 net17 gnd gnd nmos w=27e-9 l=20e-9 nf=15
m11 net033 vbiasnd gnd gnd nmos w=27e-9 l=20e-9 nf=30
m10 net034 vbiasnd gnd gnd nmos w=27e-9 l=20e-9 nf=30
m1nup vbiasn vbiasn net9b gnd nmos w=270e-9 l=20e-9 nf=3
m1ndown net9b net9b gnd gnd nmos w=270e-9 l=20e-9 nf=5
m1pup net8b net8b vdd! vdd! pmos w=270e-9 l=20e-9 nf=5
m1pdown vbiasp vbiasp net8b net8b pmos w=270e-9 l=20e-9 nf=5
m27 net27 vbiasp net021 net021 pmos w=27e-9 l=20e-9 nf=60
m26 net16 vbiasp net015 net015 pmos w=27e-9 l=20e-9 nf=60
m23 voutp vbiasp net024 net024 pmos w=27e-9 l=20e-9 nf=120
m22 vbiasnd vbiasp net06 net06 pmos w=27e-9 l=20e-9 nf=120
m21 net015 net16 vdd! vdd! pmos w=27e-9 l=20e-9 nf=5
m20 net06 net16 vdd! vdd! pmos w=27e-9 l=20e-9 nf=10
m19 net021 net27 vdd! vdd! pmos w=27e-9 l=20e-9 nf=5
m18 net024 net27 vdd! vdd! pmos w=27e-9 l=20e-9 nf=10
.ends Cascode_current_mirrot_OTA
