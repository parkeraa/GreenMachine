from simphony.libraries import siepic as si
from simphony.circuit import Circuit
from simphony.simulation import ClassicalSim
import jax.numpy as np
from matplotlib import pyplot as plt

# make some waveguides

gc_input = si.GratingCoupler()
gc_output = si.GratingCoupler()
y_splitter = si.YBranch()
y_recombiner = si.YBranch()
wg_short = si.Waveguide(length=50)
wg_long = si.Waveguide(length=150)

# make a circuit

ckt = Circuit()
ckt.connect(gc_input.o(), y_splitter)
ckt.connect(y_splitter, [wg_short, wg_long])
ckt.connect(gc_output.o(), y_recombiner)
ckt.connect(y_recombiner, [wg_short, wg_long])

gc_input.o(1).rename('input')
gc_output.o(1).rename('output')

print(ckt.port_info())

# make a simulation

wl = np.linspace(1.5, 1.6, 1000)
sim = ClassicalSim(ckt=ckt, wl=wl)
laser = sim.add_laser(ports=ckt.o('input'), power=1.0)
detector = sim.add_detector(ports=ckt.o('output'))

result = sim.run()
wl = result.wl
s = result.s_params

plt.plot(wl, np.abs(s[:, 0])**2)
plt.show()