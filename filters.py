from main_classes import Filter


class Int_eq(Filter):
    """filter on int only that are lower than the value"""

    def filtering(self) -> list:

        return [
            v_element
            for v_element in [
                element for element in self.queryset.qs if self.validator(element)
            ]
            if v_element == self.value
        ]

    def validator(self, v):
        if not isinstance(v, int):
            raise ValueError
        else:
            return True


class Int_lo(Filter):
    """filter on int only that are lower than the value"""

    def filtering(self) -> list:

        return [
            v_element
            for v_element in [
                element for element in self.queryset.qs if self.validator(element)
            ]
            if v_element < self.value
        ]

    def validator(self, v):
        if not isinstance(v, int):
            raise ValueError
        else:
            return True


class Int_up(Filter):
    """filter on int only that are lower than the value"""

    def filtering(self) -> list:

        return [
            v_element
            for v_element in [
                element for element in self.queryset.qs if self.validator(element)
            ]
            if v_element > self.value
        ]

    def validator(self, v):
        if not isinstance(v, int):
            raise ValueError
        else:
            return True


class Int_lo_eq(Filter):
    """filter on int only that are lower than the value"""

    def filtering(self) -> list:

        return [
            v_element
            for v_element in [
                element for element in self.queryset.qs if self.validator(element)
            ]
            if v_element <= self.value
        ]

    def validator(self, v):
        if not isinstance(v, int):
            raise ValueError
        else:
            return True


class Int_up_eq(Filter):
    """filter on int only that are lower than the value"""

    def filtering(self) -> list:

        return [
            v_element
            for v_element in [
                element for element in self.queryset.qs if self.validator(element)
            ]
            if v_element < self.value
        ]

    def validator(self, v):
        if not isinstance(v, int):
            raise ValueError
        else:
            return True


class String_len_up(Filter):
    """filter on the length of the string representation of the value (upper)"""

    def filtering(self) -> list:

        return [
            element
            for element in self.queryset.qs
            if len(self.converter(element)) > self.value
        ]

    def converter(self, v):
        try:
            return str(v)
        except ValueError as e:
            raise e


class String_len_lo(Filter):
    """filter on the length of the string representation of the value (upper)"""

    def filtering(self) -> list:

        return [
            element
            for element in self.queryset.qs
            if len(self.converter(element)) < self.value
        ]

    def converter(self, v):
        try:
            return str(v)
        except ValueError as e:
            raise e


class String_len_lo_eq(Filter):
    """filter on the length of the string representation of the value (upper)"""

    def filtering(self) -> list:

        return [
            element
            for element in self.queryset.qs
            if len(self.converter(element)) <= self.value
        ]

    def converter(self, v):
        try:
            return str(v)
        except ValueError as e:
            raise e


class String_len_up_eq(Filter):
    """filter on the length of the string representation of the value (upper)"""

    def filtering(self) -> list:

        return [
            element
            for element in self.queryset.qs
            if len(self.converter(element)) >= self.value
        ]

    def converter(self, v):
        try:
            return str(v)
        except ValueError as e:
            raise e


class String_contain(Filter):
    """pass if string representation of value contains the value"""

    def filtering(self) -> list:

        return [
            element
            for element in self.queryset.qs
            if self.converter(element).find(self.value) != -1
        ]

    def converter(self, v):
        try:
            return str(v)
        except ValueError as e:
            raise e


class Int_contain_numbers(Filter):
    """pass if string representation of value contains the value"""

    def filtering(self) -> list:

        if not isinstance(self.value, int):
            raise ValueError
        else:
            return [
                element
                for element in self.queryset.qs
                if self.converter(element).find(str(self.value)) != -1
            ]

    def converter(self, v):
        try:
            return str(v)
        except ValueError as e:
            raise e


class Type_exac(Filter):
    """pass if string representation of value contains the value"""

    def filtering(self) -> list:

        return [
            element for element in self.queryset.qs if isinstance(element, self.value)
        ]
