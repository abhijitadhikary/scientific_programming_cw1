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

    def test_input_wrong_key(self):
        with self.assertRaises(KeyError):
            PiecewiseLinearFunction(values=((1, 2), (1, 2)),
                                    rand_num_values=3)

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

    def test_plus_equal_for_classes(self):
        '''
        Tests += where the second object is a PiecewiseLinearFunction
        '''
        fct1 = PiecewiseLinearFunction(rand_num_values=10)
        fct2 = PiecewiseLinearFunction(rand_num_values=10)

        fct3 = fct1 + fct2
        fct1 += fct2

        assert fct3.inputs == fct1.inputs, 'Implementaiton error of += for objects'

    def test_plus_equal_for_int(self):
        '''
        Tests += where the second object is an int
        '''
        int_list = [-100, -5, 0, 5, 15000]
        fct1 = PiecewiseLinearFunction(rand_num_values=10)
        for fct2 in int_list:
            fct3 = fct1 + fct2
            fct1 += fct2
            assert fct3.inputs == fct1.inputs, f'Implementaiton error of += for int ({fct2})'


    def test_plus_equal_for_float(self):
        '''
        Tests += where the second object is an int
        '''
        # test for a list of different values
        float_list = [-100.0, -0.005, 0.0, 0.5, 15000.0]
        fct1 = PiecewiseLinearFunction(rand_num_values=10)
        for fct2 in float_list:
            fct3 = fct1 + fct2
            fct1 += fct2
            assert fct3.inputs == fct1.inputs, f'Implementaiton error of += for float ({fct2})'

    def test_plus_equal_for_other(self):
        '''
        Tests += where the second object is other than numeric or PieceWiseLinear object
        '''
        test_cases = ['c', None, {}, [], ()]
        fct1 = PiecewiseLinearFunction(rand_num_values=10)
        for fct2 in test_cases:
            with self.assertRaises(TypeError):
                fct3 = fct1 + fct2

    def test_linear_interpolation(self):
        '''
        The midpoint between the key, value pairs {2: 6, 4: 10} shold be 8
        '''
        fct1 = PiecewiseLinearFunction({2: 6, 4: 10}, interpolation='linear')

        interpolated_value = fct1.interp(3)
        assert interpolated_value == 8, 'Middle Value'

    def test_linear_interpolation_edge(self):
        '''
        The a point which coincides which the nearest points, should return the exact value
        '''
        fct1 = PiecewiseLinearFunction({2: 6, 4: 10}, interpolation='linear')

        interpolated_value = fct1.interp(2)
        assert interpolated_value == 6, 'Middle Value'

        interpolated_value = fct1.interp(4)
        assert interpolated_value == 10, 'Middle Value'

    def test_linear_extrapolation(self):
        '''
        The point equally distant from the nearest two coordinates, should have linearly
        increasing/decreasing value
        '''
        fct1 = PiecewiseLinearFunction({2: 6, 4: 10}, extrapolation='linear')

        extrapolated_value = fct1.extrap(6)
        assert extrapolated_value == 14, 'Middle Value'

        extrapolated_value = fct1.extrap(0)
        assert extrapolated_value == 2, 'Middle Value'

    def test_linear_extrapolation_edge(self):
        '''
        The a point which coincides which the nearest points, should return the exact value
        '''
        fct1 = PiecewiseLinearFunction({2: 6, 4: 10}, extrapolation='linear')

        extrapolated_value = fct1.extrap(2)
        print('\n\n\n\n\n\n{}')
        assert extrapolated_value == 6, 'Middle Value'

        extrapolated_value = fct1.extrap(4)
        assert extrapolated_value == 10, 'Middle Value'


if __name__ == '__main__':
    unittest.main()
