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

fct4 = PiecewiseLinearFunction(rand_num_values=10, interpolation='linear')

fct4.interp(55)

