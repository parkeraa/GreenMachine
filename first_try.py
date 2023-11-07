import jax.numpy as jnp
import matplotlib.pyplot as plt
import sax
from simphony.libraries import ideal


# make some waveguide



ckt, info = sax.circuit(
    netlist = {
        "instances" : {
            "wg_in" : "wg",
            "wg_out" : "wg",
            "wg_top" : "wg",
            "wg_bot" : "wg",
            "splitter" : "coupler",
            "combiner" : "coupler",
            },
        "connections" : {
            "wg_in,o1" : "splitter,o0",
            "splitter,o1" : "wg_bot,o0",
            "splitter,o3" : "wg_top,o0",
            "wg_top,o1" : "combiner,o2",
            "wg_bot,o1" : "combiner,o0",
            "wg_out,o0" : "combiner,o1",
        },
        "ports" : {
            "in" : "wg_in,o0",
            "out" : "wg_out,o1",

        }
        },
    models = {
        "wg" : ideal.waveguide,
        "coupler" : ideal.coupler,
        }
)


wl = jnp.linspace(1.5, 1.6, 1000)
s_params = ckt(wl=wl, wg_top = {"length":10}, wg_bot = {"length":20})

mag = jnp.abs(s_params["out", "in"])**2

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(wl, mag)
axs[0].set_ylabel("Transmission")
axs[1].plot(wl, 10*jnp.log10(mag))
axs[1].set_ylabel("Transmission (dB)")
axs[1].set_xlabel("Wavelength (um)")
plt.suptitle("MZI Response")
plt.show()