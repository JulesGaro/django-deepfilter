import random
from sqlite3 import IntegrityError

from django.db import models
from django.db.models import query

QS = [
    444515444,
    333515333,
    515,
    5151,
    1111111,
    2222222,
    1166611,
    51511111111,
]  # base queryset


class Object(models.Model):

    value = models.BigIntegerField()
    value_str = models.CharField(max_length=15, default="666")

    def __str__(self):
        return str(self.value)

    @classmethod
    def generate_random_qs(cls):
        for value in [random.randint(100, 9999999999) for _ in range(10000)]:
            try:
                cls.objects.create(value=value, value_str=str(value))
            except IntegrityError:
                pass


class SimpleFilter:
    def __init__(
        self,
        name: str = "",
        model: models.Model = None,
        field: str = "",
        value=None,
        django_filter: str = "",
    ):
        self.name = name
        self.value = value
        self.model = model
        self.lookup = "__".join([field, django_filter])
        self.__queryset = None

    @property
    def queryset(self):
        return self.__queryset

    @queryset.setter
    def queryset(self, v):
        self.__queryset = v

    def compute(self):
        self.__queryset = self.model.objects.filter(**{self.lookup: self.value})


class DeepFilter:
    def __init__(
        self,
        model: models.Model,
        filter_plan: list = [],
    ):
        self.model = model
        self.filter_plan = []
        self.init = False

    def compute_simple_filters(self, filter_plan=None):
        for filter in filter_plan:
            if isinstance(filter, list) or isinstance(filter, tuple):
                self.compute_all_filters(filter_plan=filter)
            else:
                filter.compute()

    def swap_filter_plan(self, filter_plan, is_tuple=False):
        swapped_filter_plan = []
        for element in filter_plan:
            if isinstance(element, list):
                swapped_filter_plan.append(self.swap_filter_plan(filter_plan=element))
            elif isinstance(element, tuple):
                swapped_filter_plan.append(
                    self.swap_filter_plan(filter_plan=element, is_tuple=True)
                )
            else:
                swapped_filter_plan.append(element.queryset)

        if is_tuple:

            return tuple(swapped_filter_plan)
        else:
            return swapped_filter_plan

    def compute_filter_plan(self, filter_plan=[], queryset: list = [], logic=None):

        # Reorder the filterplan to make sure isolated queryset are at the end.

        filter_plan = self.reorder_filter_plan(filter_plan)
        for i, stage in enumerate(filter_plan):
            if isinstance(stage, tuple):  # compute an OR group
                filter_plan[i] = self.compute_filter_plan(stage, queryset, logic="OR")
            elif isinstance(stage, list):  # compute an AND group
                filter_plan[i] = self.compute_filter_plan(stage, queryset, logic="AND")
            else:
                return self.apply_logic(filter_plan, logic=logic)

        return self.apply_logic(filter_plan, logic=logic)

    def apply_logic(
        self,
        filter_plan,
        logic=None,
    ):
        if logic == "OR":
            return self.compute_OR(
                filter_plan
            )  # compute a group of depth 1 with OR logic

        elif logic == "AND":
            return self.compute_AND(
                filter_plan
            )  # compute a group of depth 1 with AND logic

        else:
            return filter_plan[0]

    def reorder_filter_plan(self, filter_plan: list) -> list:
        """Reorder the filter plan to make sure isolated querysets are at the end of the
        list/tuple and list/tuple at the begining"""

        reordered_filter_plan = []
        tuples, lists, querysets = [], [], []

        for element in filter_plan:
            if isinstance(element, tuple):
                tuples.append(element)
            elif isinstance(element, list):
                lists.append(element)
            else:
                querysets.append(element)

        for object_type in [tuples, lists, querysets]:

            reordered_filter_plan.extend(object_type)

        return reordered_filter_plan

    def compute_OR(self, or_join_list):
        """compute a depth 1 tuple with an OR logic and return a Queryset"""
        qs = []
        for queryset in or_join_list:
            for element in queryset:
                if element not in qs:
                    qs.append(element.pk)

        return self.model.objects.filter(pk__in=qs)

    def compute_AND(self, and_join_list):
        """compute a depth 1 list with an OR logic and return a Queryset"""
        qs = []
        for queryset in and_join_list:
            for element in queryset:
                in_all = True
                for queryset_verif in and_join_list:
                    if element in queryset_verif:
                        pass
                    else:
                        in_all = False
                        break

                if in_all and element not in qs:
                    qs.append(element.pk)

        return self.model.objects.filter(pk__in=qs)


# qs = NodeVariantAnnotation.objects.filter(**variant_filters)
