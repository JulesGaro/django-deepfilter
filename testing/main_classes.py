class Queryset_class:
    def __init__(self, qs=[]):
        self.__qs = qs

    @property
    def qs(self) -> list:
        return self.__qs

    @qs.setter
    def qs(self, v: list) -> None:
        self.__qs = v

    def __str__(self):
        return str(self.qs)


class Filter:
    def __init__(self, name: str, value, base_queryset: list = []):
        self.queryset = Queryset_class(base_queryset)
        self.value = value
        self.name = name

    def compute(self) -> list:
        self.queryset.qs = self.filtering()

    def filtering(self) -> list:
        return self.queryset.qs
