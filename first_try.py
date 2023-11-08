import jax.numpy as jnp
import matplotlib.pyplot as plt
import sax
from simphony.libraries import ideal


# make some waveguide

# factory to build individual layers

def routing_wg(wl):
    return ideal.waveguide(wl=wl)

def crossover_wg(wl, device):
    return ideal.waveguide(wl=wl)

def beamsplitter(wl, device):
    return ideal.coupler(wl=wl)

def crossover(wl, device):
    return ideal.coupler(wl=wl, coupling=1)

def edge_coupler(wl, device):
    return ideal.coupler(wl=wl, coupling=0.5)

def layer_factory(wl, components, device=0) -> sax.SDict:
    """
    makes a layer of the green machine. receives as inputs the components listed 
    from row 0 to 7 and returns a circuit object with the components added and the 
    ports renamed. No connections are made within a layer

    @param components: a list of components to be added to the circuit. List as
    strings in the order of the ports. 
        "wg" - waveguide
        "ps" - phase shifter
        "bs" - beam splitter
        "x"  - crossover
        "ec" - edge coupler
    """

    # first we will make the dictionaries to be used in the netlist
    
    inst = {}
    ports = {}
    row = 0
    for comp in components:
        if comp == "wg":
            inst[f'wg_{row}'] = comp
            ports[f'in_{row}'] = f'wg_{row},o0'
            ports[f'out_{row}'] = f'wg_{row},o1'
            row += 1
        if comp == 'xwg':
            inst[f'xwg_{row}'] = comp
            ports[f'in_{row}'] = f'xwg_{row},o0'
            ports[f'out_{row}'] = f'xwg_{row},o1'
            row += 1
        if comp == "bs":
            inst[f'bs_{row}{row+1}'] = comp
            ports[f'in_{row}'] = f'bs_{row}{row+1},o0'
            ports[f'out_{row}'] = f'bs_{row}{row+1},o1'
            ports[f'in_{row+1}'] = f'bs_{row}{row+1},o2'
            ports[f'out_{row+1}'] = f'bs_{row}{row+1},o3'
            row += 2
        if comp == "x":
            inst[f'x_{row}{row+1}'] = comp
            ports[f'in_{row}'] = f'x_{row}{row+1},o0'
            ports[f'out_{row}'] = f'x_{row}{row+1},o1'
            ports[f'in_{row+1}'] = f'x_{row}{row+1},o2'
            ports[f'out_{row+1}'] = f'x_{row}{row+1},o3'
            row += 2
        if comp == "ec":
            inst[f'ec_{row}'] = comp
            ports[f'in_{row}'] = f'ec_{row},o0'
            row += 1
    print(inst)
    print(ports)

    layer, _ = sax.circuit(
            netlist = {
                "instances" : inst,
                'connections' : {},
                'ports' : ports,
            },
            models = {
                'wg': routing_wg,
                # 'xwg': crossover_wg,
                # 'bs' : beamsplitter,
                # 'x' : crossover,
                # 'ec' : edge_coupler,

            }
    )
    return layer(wl=wl)



routing_comps = ('wg', 'wg', 'wg', 'wg', 'wg', 'wg', 'wg', 'wg')

# for comp in routing_comps:
    # print(comp)
    # print(comp == 'wg')
s = layer_factory(1.55, routing_comps)
# s