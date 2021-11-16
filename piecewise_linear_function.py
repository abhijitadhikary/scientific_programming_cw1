import random

INTERPOLATIONTYPE = ['nearestNeighboor', 'linear']
EXTRAPOLATIONTYPE = ['nearestNeighboor', 'linear']


class PiecewiseLinearFunction:
    """
    Class that represents a piecewise linear function. The function is
    parametrised by a list of points encoded each by a coordinate (1D) and a
    value.
    """
    def __init__(self,
                 values=None,
                 rand_num_values=None,
                 interpolation=INTERPOLATIONTYPE[0],
                 extrapolation=EXTRAPOLATIONTYPE[0]):
        self.test_input_wrong_type1(values)

        self.check_duplicate_keys(values)
        self.test_input_wrong_type2(rand_num_values)

        # self.check_wrong_key(values, rand_num_values)



        self.inputs = dict()
        if values is not None:
            self.inputs = dict(values)
        self.interpolation = interpolation
        self.extrapolation = extrapolation
        self.sanitize_string_inputs()
        if rand_num_values is not None and isinstance(rand_num_values, int):
            self.inputs = dict(zip(
                random.sample(range(-1000, 1000), rand_num_values),
                random.sample(range(-100, 100), rand_num_values)))

        self._update_params()

    def is_numeric(self, value):
        '''
        Tests whether a supplied value is numeric
        '''
        return True if isinstance(value, int) or isinstance(value, float) else False


    def test_input_wrong_type1(self, values):
        '''
        Makes sure all supplied values are numerical
        '''
        if not values is None:
            for key, value in values:
                if not (self.is_numeric(key) and self.is_numeric(value)):
                    raise TypeError('All key and values should be numeric')

    def test_input_wrong_type2(self, rand_num_values):
        '''
        Makes sure rand_num_values is an integer
        '''
        if not rand_num_values is None:
            if not isinstance(rand_num_values, int):
                raise TypeError(f'rand_num_values should be an integer')





    def check_duplicate_keys(self, values):
        '''
        Checks whether there are duplicate keys in the supplied values
        raises ValueError if present
        '''

        if not values is None:
            key_list = []
            for key, _ in values:
                if key in key_list:
                    raise ValueError('Duplicate Keys Supplied (ValueError)')
                else:
                    key_list.append(key)

    # def check_wrong_key(self, values, rand_num_values):
    #     '''
    #     Checks whether the number of elements in  values is equal to
    #     rand_num_values
    #     '''
    #     if not values is None:
    #         if not (len(values) == rand_num_values):
    #             raise KeyError(f'The number of elements in values ({len(values)})'
    #                            f' and rand_num_values ({rand_num_values}) are not equal')


    # def check_wrong_key(self, values, rand_num_values):
    #     '''
    #     Raises key error if both values and rand_num_values are supplued at the
    #     same time, or if neither is supplied
    #     '''
    #     if not ((values is None) and (rand_num_values is None)):
    #         raise KeyError('Both values and rand_num_values supplied at the same time')
    #
    #     if (values is None) and (rand_num_values is None):
    #         raise KeyError('None of values and rand_num_values supplied')

    def sanitize_string_inputs(self):
        if not self.interpolation in INTERPOLATIONTYPE:
            raise ValueError(f'Incorrect interpolation type: `{self.interpolation}`')

        if not self.extrapolation in EXTRAPOLATIONTYPE:
            raise ValueError(f'Incorrect extrapolation type: `{self.extrapolation}`')



    def _update_params(self):
        self.num = len(self.inputs)
        self.min_coord, self.max_coord = self.get_min_max_coord()

    def get_min_max_coord(self):
        if len(self.inputs) == 0:
            return None, None
        min_coord = float('+inf')
        max_coord = float('-inf')
        for v in self.inputs.keys():
            if v < min_coord:
                min_coord = v
            if v > max_coord:
                max_coord = v
        return min_coord, max_coord

    def __iter__(self):
        return self.inputs.items().__iter__()

    def get_linear_interpolation(self, coord):
        '''
        Returns the interpolated value corresponding to the nearest two
        points of the supplied coordinate.
        '''

        # obtain the 2 closest coordinates of the input coord
        closest_1, closest_2 = sorted(self.inputs.keys(),
                                      key=lambda c: abs(c - coord))[:2]

        # extract and assign the corresponding values to A and B
        A = closest_1 if closest_1 <= closest_2 else closest_2
        B = closest_2 if A == closest_1 else closest_1

        # calculate the interpolated value based on the ratio
        ratio = (coord - A) / (B - A)
        C_value = (self.inputs[A] * (1 - ratio)) + (self.inputs[B] * ratio)

        return C_value

    def interp(self, coord):
        """
        Interpolate the value at any coordinate using linear interpolation
        from the two closest points
        :param coord: real scalar value that encodes the coordinate of the
        value to interpolate
        :return: the interpolated value
        """
        # Call the extrapolation function if the coordinate is outside of the
        # range
        if not self.min_coord < coord < self.max_coord:
            return self.extrap(coord)
        if self.interpolation == 'nearestNeighboor':
            # Extract the closest point and return the corresponding value
            closest = sorted(self.inputs.keys(),
                             key=lambda c: abs(c - coord))[0]
            return self.inputs[closest]
        elif self.interpolation == 'linear':
            return self.get_linear_interpolation(coord)
        else:
            raise NotImplementedError('Interpolation for non nearest '
                                      'neighbour interpolation has not been '
                                      'implemented yet')

    def extrap(self, coord):
        """
        Extrapolate the value at any coordinate
        :param coord: real scalar value that encodes the coordinate of the
        value to extrapolate
        :return: the extrapolated value
        """
        if self.extrapolation == 'nearestNeighboor':
            if coord <= self.min_coord:
                return self.inputs[self.min_coord]
            elif coord >= self.max_coord:
                return self.inputs[self.max_coord]
            else:
                raise RuntimeError('The interpolation method should be'
                                   'called instead')
        elif self.interpolation == 'linear':
            return self.get_linear_interpolation(coord)
        else:
            raise NotImplementedError('Extrapolation for non nearest '
                                      'neighbour extrapolation has not been '
                                      'implemented yet')

    def remove_point(self, coord):
        """
        Remove a data point from the dictionary encoding the parameters.
        :param coord: Coordinate of the point to remove
        """
        if not isinstance(coord, (int, float)):
            raise TypeError('A real numerical value is expected as '
                            'a coordinate')
        if coord in self.inputs.keys():
            del self.inputs[coord]
        else:
            raise ValueError('The specified coordinate does not exist')
        self._update_params()

    def add_point(self, coord_value):
        """
        Add a data point to parametrise the function
        :param coord_value: tuple encoding the coordinate and associated value
        """
        if not isinstance(coord_value, tuple):
            raise TypeError('The point to be added is expected to be encoded'
                            ' as a tuple containing (coordinate, value)')
        if not isinstance(coord_value[0], (int, float)):
            raise TypeError('A real numerical value is expected as '
                            'a coordinate')
        if not isinstance(coord_value[1], (int, float)):
            raise TypeError('A real numerical value is expected as '
                            'a value')
        if coord_value[0] in self.inputs.keys():
            raise ValueError('The specified coordinate already exists')
        self.inputs[coord_value[0]] = coord_value[1]
        self._update_params()

    def __add__(self, other):
        """
        Define the addition operator for two objects of type
         PiecewiseLinearFunction or one PiecewiseLinearFunction and a real
         number
        :param other: right-hand side argument
        :return: A PiecewiseLinearFunction object
        """
        new_values = dict()
        # Add two functions
        if isinstance(other, PiecewiseLinearFunction):
            for c, v in self.inputs.items():
                new_values[c] = v + other.interp(c)
            for c2, v2 in other:
                if c2 not in new_values.keys():
                    new_values[c2] = self.interp(c2) + v2
        # Add a constant to the left-hand side operand
        elif isinstance(other, (int, float)):
            for c, v in self.inputs.items():
                new_values[c] = v + other
        else:
            raise TypeError('Unsupported data type')
        return PiecewiseLinearFunction(new_values)

    # def __iadd__(self, other):
    #     """
    #     Define the addition operator for two objects of type
    #      PiecewiseLinearFunction or one PiecewiseLinearFunction and a real
    #      number using ++=
    #     :param other: right-hand side argument
    #     :return: A PiecewiseLinearFunction object
    #     """
    #     new_values = dict()
    #     # Add two functions
    #     if isinstance(other, PiecewiseLinearFunction):
    #         for c, v in self.inputs.items():
    #             new_values[c] = v + other.interp(c)
    #         for c2, v2 in other:
    #             if c2 not in new_values.keys():
    #                 new_values[c2] = self.interp(c2) + v2
    #     # Add a constant to the left-hand side operand
    #     elif isinstance(other, (int, float)):
    #         for c, v in self.inputs.items():
    #             new_values[c] = v + other
    #     else:
    #         raise TypeError('Unsupported data type')
    #     return PiecewiseLinearFunction(new_values)

    def get_lists_sorted_by_coord(self):
        """
        Returns two lists as a tuple containing the ordered coordinates and the
        corresponding values in the corresponding order.
        :return: a tuple of two lists
        """
        sorted_dict = sorted(self.inputs.items())
        sorted_keys = [i[0] for i in sorted_dict]
        sorted_values = [i[1] for i in sorted_dict]
        return sorted_keys, sorted_values
