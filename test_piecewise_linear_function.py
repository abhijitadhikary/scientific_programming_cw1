import unittest
from piecewise_linear_function import (PiecewiseLinearFunction,
                                       INTERPOLATIONTYPE,
                                       EXTRAPOLATIONTYPE)


class PiecewiseLinearFunctionInitTest(unittest.TestCase):
    def test_type(self):
        F = PiecewiseLinearFunction()
        self.assertIsInstance(F, PiecewiseLinearFunction)

    @staticmethod
    def test_input_values():
        PiecewiseLinearFunction(values=((1, 2), (2, 3), (3, 4)))

    @staticmethod
    def test_input_rand_num():
        PiecewiseLinearFunction(rand_num_values=2)

    # def test_input_wrong_key(self):
    #     with self.assertRaises(KeyError):
    #         PiecewiseLinearFunction(values=((1, 2), (1, 2)),
    #                                 rand_num_values=3)

    def test_input_wrong_size1(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(values=((1, 2), (2,)))

    def test_input_wrong_size2(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(values=((1, 2, 3), (2, 3, 4)))

    def test_input_duplicated_key(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(values=((1, 1), (1, 2)))

    @staticmethod
    def test_input_interp():
        for t in INTERPOLATIONTYPE:
            PiecewiseLinearFunction(interpolation=t)

    @staticmethod
    def test_input_extrap():
        for t in EXTRAPOLATIONTYPE:
            PiecewiseLinearFunction(extrapolation=t)

    def test_input_wong_interp(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(interpolation='bla')

    def test_input_wong_extrap(self):
        with self.assertRaises(ValueError):
            PiecewiseLinearFunction(extrapolation='bla')

    @staticmethod
    def test_input_type():
        PiecewiseLinearFunction(values=((1, 2), (3, 4)))
        PiecewiseLinearFunction(values=((1., 2), (3, 4)))
        PiecewiseLinearFunction(values=((float(1), 2), (3, 4)))

    def test_input_wrong_type1(self):
        with self.assertRaises(TypeError):
            PiecewiseLinearFunction(values=((1, 'a'), (2, 3)))

    def test_input_wrong_type2(self):
        with self.assertRaises(TypeError):
            PiecewiseLinearFunction(rand_num_values='three')


if __name__ == '__main__':
    unittest.main()
