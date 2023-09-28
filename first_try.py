from simphony.libraries import siepic as si
from simphony.libraries import ideal
from simphony.circuit import Circuit
from simphony.simulation import ClassicalSim
import jax.numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# make some waveguides

gc_input = si.GratingCoupler()
gc_output = si.GratingCoupler()
y_splitter = si.YBranch()
y_recombiner = si.YBranch()
wg_short = si.Waveguide(length=50)
wg_long = si.Waveguide(length=150)

# make a circuit

def diag_stack(s1, s2):
                zeros = np.zeros([s1.shape[0], s1.shape[1], s2.shape[2]])
                zerosT = np.zeros([s1.shape[0], s2.shape[1], s1.shape[2]])
                return np.block([[s1, zeros], [zerosT, s2]])

A = np.array([[[1, 2], [3, 4]]])
B = np.array([[[5, 6], [7, 8]]])
C = diag_stack(A, B)
# print(C)

ckt = Circuit()

coupler = ideal.Coupler(coupling=0.45)
wg0 = ideal.Waveguide(length=1.0)
wg1 = ideal.Waveguide(length=100.0)

# ckt.connect(coupler.o(2), wg0)
# ckt.connect(coupler.o(3), wg1)
# ckt.expose([wg0.o(1), coupler.o(0), wg1.o(1), coupler.o(1)])

ckt.add(coupler)
ckt.add(wg0)   
ckt.add(wg1)

# coupler.rename_oports(["in1", "in2", "con1", "con2"])
# wg0.rename_oports(["con1", "out0"])
# wg1.rename_oports(["con2", "out1"])

# ckt.autoconnect(coupler, wg0)
# ckt.autoconnect(coupler, wg1)
# ckt.plot_networkx()
# plt.show()

s = ckt.s_params([1.55])
np.save("detached_s_params.npy", s)
print(pd.DataFrame(s[0]))