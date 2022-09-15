from main_classes import Queryset_class
from filters import *


def compute_filters(filters: list = []):
    """Take the filters list and apply the filters to the queryset"""
    for element in filters:
        element.compute()


def compute_filter_plan(
    filter_plan=[], queryset: list = [], logic=None
) -> Queryset_class:
    """recursively compute a filter plan and finaly return a single queryset that gone
    through all the AND/OR combination of the filter plan"""

    # Reorder the filterplan to make sure isolated queryset are at the end.

    filter_plan = reorder_filter_plan(filter_plan)
    for i, stage in enumerate(filter_plan):
        if isinstance(stage, tuple):  # compute an OR group
            filter_plan[i] = compute_filter_plan(stage, queryset, logic="OR")
        elif isinstance(stage, list):  # compute an AND group
            filter_plan[i] = compute_filter_plan(stage, queryset, logic="AND")
        else:
            return apply_logic(filter_plan, logic=logic)

    return apply_logic(filter_plan, logic=logic)


def apply_logic(
    filter_plan,
    logic=None,
):
    if logic == "OR":
        return compute_OR(filter_plan)  # compute a group of depth 1 with OR logic

    elif logic == "AND":
        return compute_AND(filter_plan)  # compute a group of depth 1 with AND logic

    else:
        return filter_plan[0]


def reorder_filter_plan(filter_plan: list) -> list:
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


def compute_OR(or_join_list):
    """compute a depth 1 tuple with an OR logic and return a Queryset"""
    qs = []
    for queryset in or_join_list:
        for element in queryset.qs:
            if element not in qs:
                qs.append(element)

    return Queryset_class(qs=qs)


def compute_AND(and_join_list):
    """compute a depth 1 list with an OR logic and return a Queryset"""

    qs = []
    for queryset in and_join_list:
        for element in queryset.qs:
            in_all = True
            for queryset_verif in and_join_list:
                if element in queryset_verif.qs:
                    pass
                else:
                    in_all = False
                    break

            if in_all and element not in qs:
                qs.append(element)

    return Queryset_class(qs=qs)
