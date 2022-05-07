.subckt Current_mirror_OTA voutp gnd vinn id vinp vbiasnd vdd!
m17 net16 vinn net24 gnd nmos w=27e-9 l=20e-9 nf=28
m16 net24 id gnd gnd nmos w=27e-9 l=20e-9 nf=10
m15 net27 vinp net24 gnd nmos w=27e-9 l=20e-9 nf=28
m14 id id gnd gnd nmos w=27e-9 l=20e-9 nf=10
m11 vbiasnd vbiasnd gnd gnd nmos w=27e-9 l=20e-9 nf=24
m10 voutp vbiasnd gnd gnd nmos w=27e-9 l=20e-9 nf=24
m21 net16 net16 vdd! vdd! pmos w=27e-9 l=20e-9 nf=60
m20 m20stack net16 vdd! vdd! pmos w=27e-9 l=20e-9 nf=240
m20s vbiasnd net16 m20stack vdd! pmos w=27e-9 l=20e-9 nf=240
m19 net27 net27 vdd! vdd! pmos w=27e-9 l=20e-9 nf=60
m18 m18stack net27 vdd! vdd! pmos w=27e-9 l=20e-9 nf=240
m18s voutp net27 m18stack vdd! pmos w=27e-9 l=20e-9 nf=240
.ends Current_mirror_OTA
