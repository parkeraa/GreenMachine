from simphony.libraries import ideal
from simphony.circuit import Circuit
import jax.numpy as np
from matplotlib import pyplot as plt



# The ports are labeled as follows:
# jct00 refers to the junction at layer 0 on row 0


def layer_factory(*components):
    """
    makes a layer of the green machine. receives as inputs the components listed 
    from row 0 to 7 and returns a circuit object with the components added and the 
    ports renamed. 

    @param components: a list of components to be added to the circuit. List as
    strings in the order of the ports. 
        "wg" - waveguide
        "ps" - phase shifter
        "bs" - beam splitter
        "x"  - crossover
    """
    ckt = Circuit()
    row = 0
    for comp in components:
        if comp == "wg":
            c = ideal.Waveguide()
            c.rename_oports([f'jct{row}', f'out{row}'])
            c.name = f'wg{layer}_{row}'
            ckt.add(c)
            row += 1
        elif comp == "ps":
            c = ideal.PhaseShifter()
            c.rename_oports([f'jct{row}', f'out{row}'])
            c.name = f'ps{layer}_{row}'
            ckt.add(c)
            row += 1
        elif comp == "bs":
            c = ideal.Coupler()
            c.rename_oports([f'jct{row}', f'jct{row+1}', f'out{row}', f'out{row+1}'])
            c.name = f'bs{layer}_{row}{row+1}'
            ckt.add(c)
            row += 2
        elif comp == "x":
            c = ideal.Coupler(1)
            c.rename_oports([f'jct{row}', f'jct{row+1}', f'out{row}', f'out{row+1}'])
            c.name = f'x{layer}_{row}{row+1}'
            ckt.add(c)
            row += 2
        else:
            print("invalid component")

    return ckt

def add_layer(gm, *components, rename=True):
    """
    adds a new layer to the green machine circuit
    """
    ckt = Circuit()
    lay = layer_factory(*components)
    ckt.autoconnect(gm, lay)
    if rename:
        for i in range(8):
            ckt.expose(lay.o(f'out{i}'))
            ckt.expose(gm.o(f'in{i}'))
            ckt.o(f'out{i}').rename(f'jct{i}')
    return ckt


# LAYER 0
in0 =  ideal.PhaseShifter(name = "in0")
in1 =  ideal.PhaseShifter(name = "in1")
in2 =  ideal.PhaseShifter(name = "in2")
in3 =  ideal.PhaseShifter(name = "in3")
in4 =  ideal.PhaseShifter(name = "in4")
in5 =  ideal.PhaseShifter(name = "in5")
in6 =  ideal.PhaseShifter(name = "in6")
in7 =  ideal.PhaseShifter(name = "in7")




in0.rename_oports(["in0", 'jct0'])
in1.rename_oports(["in1", 'jct1'])
in2.rename_oports(["in2", 'jct2'])
in3.rename_oports(["in3", 'jct3'])
in4.rename_oports(["in4", 'jct4'])
in5.rename_oports(["in5", 'jct5'])
in6.rename_oports(["in6", 'jct6'])
in7.rename_oports(["in7", 'jct7'])

green_machine = Circuit()
green_machine.add(in0)
green_machine.add(in1)
green_machine.add(in2)
green_machine.add(in3)
green_machine.add(in4)
green_machine.add(in5)
green_machine.add(in6)
green_machine.add(in7)


# LAYER 1 
layer = 1
green_machine = add_layer(green_machine, 'bs', 'bs', 'bs', 'bs')
layer = 2
green_machine = add_layer(green_machine, 'ps', 'x', 'x', 'x', 'ps')
layer = 3
green_machine = add_layer(green_machine, 'ps', 'ps', 'x', 'x', 'ps', 'ps')
layer = 4
green_machine = add_layer(green_machine, 'ps', 'x', 'x', 'x', 'ps')
layer = 5
green_machine = add_layer(green_machine, 'bs', 'bs', 'bs', 'bs')
layer = 6
green_machine = add_layer(green_machine, 'ps', 'x', 'ps', 'ps', 'x', 'ps')
layer = 7
green_machine = add_layer(green_machine, 'bs', 'bs', 'bs', 'bs')
layer = 8
green_machine = add_layer(green_machine, 'ps', 'ps', 'ps', 'ps', 'ps', 'ps', 'ps', 'ps', rename=False)



print(green_machine.port_info())
print(green_machine.s_params(wl = [1.55]))

green_machine.plot_networkx()
plt.show()