import matplotlib.pyplot as plt
import random
from piecewise_linear_function import PiecewiseLinearFunction

# fct1 = PiecewiseLinearFunction(zip(
#     (random.sample(range(-1000, 1000), 10)),
#     (random.uniform(-100, 100) for i in range(10))
# ))
# fct2 = PiecewiseLinearFunction(rand_num_values=10)
#
# fct3 = fct1 + fct2








#
# plt.figure()
# plt.plot(
#     *fct1.get_lists_sorted_by_coord(), 'r-',
#     *fct2.get_lists_sorted_by_coord(), 'b-',
#     *fct3.get_lists_sorted_by_coord(), 'k-')
# plt.show()
#
# fct4 = PiecewiseLinearFunction(rand_num_values=10, interpolation='linear')
#
# fct4.interp(55)


PiecewiseLinearFunction(values=zip((1, 1), (1, 2)))


# PiecewiseLinearFunction(values=((1, 2), (2, 2)),
#                                     rand_num_values=3)



# import numpy as np
# min_value, max_value = 10, 20
# x_vals = np.array([min_value, 15, max_value])
# y_vals = np.array([5, 9, 7])
#
# coord_dict = {x: y for x, y in zip(x_vals, y_vals)}
#
# mesh_x = np.linspace(max_value-10, max_value+10, 11)
#
# my_plc = PiecewiseLinearFunction(values=coord_dict, interpolation='linear', extrapolation='linear')
# mesh_y = [my_plc.interp(x) for x in mesh_x]
#
# coords_interp = {x: y for x, y in zip(mesh_x, mesh_y)}




# fct1 = PiecewiseLinearFunction(zip(
#     (random.sample(range(-1000, 1000), 10)),
#     (random.uniform(-100, 100) for i in range(10))
# ), interpolation='nearestNeighboor')