.subckt 2019_10_01_5t_OTA gnd vout vdd
m5 net2 net2 net5s gnd nmos w=270e-9 l=20e-9 nf=10
m5s net5s net2 gnd gnd nmos w=270e-9 l=20e-9 nf=10
m4 net10 net2 net4s gnd nmos w=270e-9 l=20e-9 nf=40
m4s net4s net2 gnd gnd nmos w=270e-9 l=20e-9 nf=40
m3 vout net15 net3s gnd nmos w=270e-9 l=20e-9 nf=160
m3s net3s net15 net10 gnd nmos w=270e-9 l=20e-9 nf=160
m0 net8 net17 net0s gnd nmos w=270e-9 l=20e-9 nf=160
m0s net0s net17 net10 gnd nmos w=270e-9 l=20e-9 nf=160
m2 vout net8 net2s vdd pmos w=270e-9 l=20e-9 nf=100
m2s net2s net8 vdd vdd pmos w=270e-9 l=20e-9 nf=100
m1 net8 net8 net1s vdd pmos w=270e-9 l=20e-9 nf=100
m1s net1s net8 vdd vdd pmos w=270e-9 l=20e-9 nf=100
.ends 2019_10_01_5t_OTA
