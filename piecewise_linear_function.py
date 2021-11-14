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
        self.inputs = dict()
        if values is not None:
            self.inputs = dict(values)
        self.interpolation = interpolation
        self.extrapolation = extrapolation
        if rand_num_values is not None and isinstance(rand_num_values, int):
            self.inputs = dict(zip(
                random.sample(range(-1000, 1000), rand_num_values),
                random.sample(range(-100, 100), rand_num_values)))
        self._update_params()

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
