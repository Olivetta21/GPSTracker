class UInt8:
    __slots__ = ("_value",)

    def __init__(self, value=0):
        self._value = self._wrap(value)

    @staticmethod
    def _wrap(value):
        """Força o valor a caber em 8 bits sem sinal (uint8_t)."""
        return value & 0xFF  # mantém apenas 8 bits (0–255)

    def __int__(self):
        return int(self._value)

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"B'{self._value}"

    # Comparações
    def __eq__(self, other):
        return int(self) == int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    # Operadores aritméticos
    def __add__(self, other):
        return UInt8(self._value + int(other))

    def __sub__(self, other):
        return UInt8(self._value - int(other))

    def __mul__(self, other):
        return UInt8(self._value * int(other))

    def __floordiv__(self, other):
        return UInt8(self._value // int(other))

    def __mod__(self, other):
        return UInt8(self._value % int(other))

    def __neg__(self):
        return UInt8(-self._value)

    # Operadores bitwise
    def __and__(self, other):
        return UInt8(self._value & int(other))

    def __or__(self, other):
        return UInt8(self._value | int(other))

    def __xor__(self, other):
        return UInt8(self._value ^ int(other))

    def __invert__(self):
        return UInt8(~self._value)

    def __lshift__(self, other):
        return UInt8(self._value << int(other))

    def __rshift__(self, other):
        return UInt8(self._value >> int(other))
