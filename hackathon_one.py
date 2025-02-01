# # Model
# # RI(t) = synaptic inputs
# # In the absence of spikes or voltage increase, the neuron decays to a resting potential
# import numpy as np
# import matplotlib.pyplot as plt

# # @title Figure settings
# import logging
# logging.getLogger('matplotlib.font_manager').disabled = True
# import ipywidgets as widgets  # interactive display
# %config InlineBackend.figure_format = 'retina'
# plt.style.use("https://raw.githubusercontent.com/NeuromatchAcademy/course-content/master/nma.mplstyle")


# # t_max = 150e-3   # second
# # dt = 1e-3        # second
# # tau = 20e-3      # second
# # el = -60e-3      # milivolt
# # vr = -70e-3      # milivolt
# # vth = -50e-3     # milivolt
# # r = 100e6        # ohm
# # i_mean = 25e-11  # ampere

# # print(t_max, dt, tau, el, vr, vth, r, i_mean)