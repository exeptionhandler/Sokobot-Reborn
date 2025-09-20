import random

class Randomizer:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = random.Random()
        return cls._instance

    @classmethod
    def next_boolean(cls) -> bool:
        return cls.get_instance().choice([True, False])

    @classmethod
    def next_int(cls, max_value: int = None) -> int:
        if max_value is None:
            return cls.get_instance().randint(-2147483648, 2147483647)
        return cls.get_instance().randint(0, max_value - 1)

    @classmethod
    def next_double(cls) -> float:
        return cls.get_instance().random()

    @classmethod
    def next_int_range(cls, min_value: int, max_value: int) -> int:
        return cls.get_instance().randint(min_value, max_value)

    @classmethod
    def next_double_range(cls, min_value: float, max_value: float) -> float:
        return min_value + (max_value - min_value) * cls.next_double()

    @classmethod
    def next_color(cls) -> str:
        color_int = cls.next_int_range(0, 16777216)
        return f"#{color_int:06x}"
