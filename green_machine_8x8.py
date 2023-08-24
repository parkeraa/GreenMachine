from simphony.libraries import ideal
from simphony.circuit import Circuit
import jax.numpy as np
from matplotlib import pyplot as plt



# The ports are labeled as follows:
# jct00 refers to the junction at layer 0 on row 0

# LAYER 0
in0 =  ideal.PhaseShifter()
in1 =  ideal.PhaseShifter()
in2 =  ideal.PhaseShifter()
in3 =  ideal.PhaseShifter()
in4 =  ideal.PhaseShifter()
in5 =  ideal.PhaseShifter()
in6 =  ideal.PhaseShifter()
in7 =  ideal.PhaseShifter()

in0.o().rename("in0")
in1.o().rename("in1")
in2.o().rename("in2")
in3.o().rename("in3")
in4.o().rename("in4")
in5.o().rename("in5")
in6.o().rename("in6")
in7.o().rename("in7")


# LAYER 1 

split_1_01 = ideal.Coupler()
split_1_23 = ideal.Coupler()
split_1_45 = ideal.Coupler()
split_1_67 = ideal.Coupler()

# Connect them together

ckt = Circuit()

ckt.connect(split_1_01, [in0.o(1), in1.o(1)])
ckt.connect(split_1_23, [in2.o(1), in3.o(1)])
ckt.connect(split_1_45, [in4.o(1), in5.o(1)])
ckt.connect(split_1_67, [in6.o(1), in7.o(1)])

# LAYER 2

wg_2_0 = ideal.PhaseShifter()
cross_2_12 = ideal.Coupler(1)
cross_2_34 = ideal.Coupler(1)
cross_2_56 = ideal.Coupler(1)
wg_2_7 = ideal.PhaseShifter()

ckt.connect(split_1_01, [wg_2_0.o(), cross_2_12.o()])
ckt.connect(split_1_23, [cross_2_12.o(), cross_2_34.o()])
ckt.connect(split_1_45, [cross_2_34.o(), cross_2_56.o()])
ckt.connect(split_1_67, [cross_2_56.o(), wg_2_7.o()])

# LAYER 3

wg_3_0 = ideal.PhaseShifter()
wg_3_1 = ideal.PhaseShifter()
cross_3_23 = ideal.Coupler(1)
cross_3_45 = ideal.Coupler(1)
wg_3_6 = ideal.PhaseShifter()
wg_3_7 = ideal.PhaseShifter()

ckt.connect(wg_2_0, wg_3_0)
ckt.connect(cross_2_12, [wg_3_1.o(), cross_3_23.o()])
ckt.connect(cross_2_34, [cross_3_23.o(), cross_3_45.o()])
ckt.connect(cross_2_56, [cross_3_45.o(), wg_3_6.o()])
ckt.connect(wg_2_7, wg_3_7)

# LAYER 4

wg_4_0 = ideal.PhaseShifter()
cross_4_12 = ideal.Coupler(1)
cross_4_34 = ideal.Coupler(1)
cross_4_56 = ideal.Coupler(1)
wg_4_7 = ideal.PhaseShifter()

ckt.connect(wg_3_0, wg_4_0)
ckt.connect(wg_3_1, cross_4_12)
ckt.connect(cross_3_23, [cross_4_12.o(), cross_4_34.o()])
ckt.connect(cross_3_45, [cross_4_34.o(), cross_4_56.o()])
ckt.connect(wg_3_6, cross_4_56)
ckt.connect(wg_3_7, wg_4_7)

# print(ckt.port_info())

# ckt.plot_networkx()
# plt.show()