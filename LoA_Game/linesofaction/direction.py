import enum
import numpy as np

class Direction(enum.Enum):
    r'''Direction is just a unitvector in geographic coordinates.'''
    N = NORTH = (-1, 0)
    S = SOUTH = (1, 0)
    E = EAST = (0, 1)
    W = WEST = (0, -1)

    # Add the directions, and make sure they are tuples
    NE = NORTH_EAST = tuple(np.add(N, E).tolist())
    NW = NORTH_WEST = tuple(np.add(N, W).tolist())
    SE = SOUTH_EAST = tuple(np.add(S, E).tolist())
    SW = SOUTH_WEST = tuple(np.add(S, W).tolist())

    # === The rest are just utilities ===

    @classmethod
    def str2value(cls, string):
        value = string.upper()
        # Try to guess from the string
        if value in cls.__members__:
            return cls.__members__[value].value
        elif len(value) in (9, 10):  # NORTHEAST, NORTH_EAST, NORTH EAST
            value = value[0] + value[-4] # NE
        if len(value) == 2 and value[0] != value[1]:
            value = (
                cls.__members__[value[0]].value[0],
                cls.__members__[value[1]].value[1]
            )
        else:
            raise ValueError(f'Not sure how to convert: {string}')
        return value

    def __and__(self, other):
        return Direction(self.value[0] + other.value[0], self.value[1] + other.value[1])

    def __invert__(self):
        return Direction(-self.value[0], -self.value[1])

    def __add__(self, other):
        return self & other

    def __eq__(self, other):
        if isinstance(other, list):
            return self == tuple(other)
        return self.value == Direction(other).value
    
    def __contains__(self, other):
        return self.value[0] == other.value[0] or self.value[1] == other.value[1]

    @classmethod
    def numel(self):
        # Finds all unique directions and returns their count
        unique_directions = set([value for value in Direction])
        return len(unique_directions)

    @classmethod
    def _missing_(cls, value):
        r'''This method handles all the corner cases:
        
        * When the value is a list, convert it to a tuple
        * When the value is a string
            * Call `str2value` to attempt to convert it
        * When the value is not a unit vector, convert it to a unit vector
        * When the value is not in the list of directions, create a composite direction
            * This should never happen, as we enumerated all cases. But just in case.
        '''
        if isinstance(value, list):  # Keep it as a tuple everywhere
            return Direction(tuple(value))
        if isinstance(value, str):  # Try converting the string
            value = cls.str2value(value)

        # Convert non-unit values to unit values
        value = tuple(np.sign(value))

        # Check if the value already exists
        for member in cls:
            if value == member.value:
                return member

        # Create a composite direction        
        pseudo_member = object.__new__(cls)
        pseudo_member._value_ = value
        # Collect the directions that make up the composite direction
        directions = set()
        for member in cls:
            if value[0] == member.value[0]:
                directions.add(member)
            if value[1] == member.value[1]:
                directions.add(member)
        pseudo_member._name_ = ''.join([direction.name for direction in directions])
        return pseudo_member