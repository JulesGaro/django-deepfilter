import random
from sqlite3 import IntegrityError

from django.db import models
from django.db.models import query
from .process import parser

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


class Variant(models.Model):

    chr = models.TextField(max_length=3000, default="")
    start = models.BigIntegerField()
    ref = models.TextField(max_length=3000, default="")
    alt = models.TextField(max_length=3000, default="")
    func_refgene = models.TextField(max_length=50, default="")
    filters = models.TextField(max_length=3000, default="")
    omim = models.TextField(max_length=3000, default="")
    inheritance = models.TextField(max_length=3000, default="")
    gnomad_genome_all = models.TextField(max_length=3000, default="")

    def __str__(self):
        return self.chr + ":" + str(self.start) + " " + self.ref + ">" + self.alt


class VariantFactory(models.Model):
    name = models.CharField(default="Nope", max_length=50)
    filename = models.CharField(default="", max_length=300)

    def load(self):
        reader = parser(self.filename)
        for variant in reader:
            Variant.objects.get_or_create(
                chr=variant.CHR,
                start=int(variant.START),
                ref=variant.REF,
                alt=variant.ALT,
                func_refgene=variant.FUNC_REFGENE,
                filters=variant.FILTERS,
                omim=variant.OMIM,
                inheritance=variant.INHERITANCE,
                gnomad_genome_all=[
                    existing_value
                    for existing_value in [variant.GNOMAD_GENOME_ALL]
                    if existing_value is not None
                ],
            )


class DeepFilter:
    def __init__(
        self,
        model,
        raw_filter_plan: dict,
    ):
        self.model = model
        self.filters = raw_filter_plan["filters"]

        ordered_filter_plan = self.reorder_filter_plan(raw_filter_plan["dfilter_plan"])

        self.filter_plan = [self.build_filter_plan(filter_plan=ordered_filter_plan)]

    def build_filter_plan(self, filter_plan, is_tuple=False):
        builded_fp = []
        for element in filter_plan:
            if isinstance(element, list):
                builded_fp.append(self.build_filter_plan(filter_plan=element))
            elif isinstance(element, tuple):
                builded_fp.append(
                    self.build_filter_plan(filter_plan=element, is_tuple=True)
                )
            else:
                builded_fp.append(self.compute_simple_filter(name=element))

        if is_tuple:

            return tuple(builded_fp)
        else:
            return builded_fp

    def compute_simple_filter(self, filter_name: str):
        filter = [filter for filter in self.filters if filter["name"] == filter_name][0]
        lookup = "__".join([filter["field"], filter["django_filter"]])

        return self.model.objects.filter(**{lookup: filter["value"]})

    def reorder_filter_plan(self, filter_plan):
        """Reorder the filter plan to make sure isolated querysets are at the end of the
        list/tuple and list/tuple at the begining"""

        reordered_filter_plan = []
        tuples, lists, filter = [], [], []

        for element in filter_plan:
            if isinstance(element, tuple):
                tuples.append(element)
            elif isinstance(element, list):
                lists.append(element)
            else:
                filter.append(element)

        for object_type in [tuples, lists, filter]:

            reordered_filter_plan.extend(object_type)

        return reordered_filter_plan

    def process(self):
        processor = DeepFilterProcessor(model=self.model, filter_plan=self.filter_plan)

        filtered_qs = processor.filter()

        return filtered_qs


class DeepFilterProcessor:
    def __init__(
        self,
        model,
        filter_plan,
    ):
        self.model = model
        self.filter_plan = filter_plan

    def filter(self):
        return self.compute_filter_plan(filter_plan=self.filter_plan)

    def compute_filter_plan(self, filter_plan=[], logic=None):

        for i, stage in enumerate(filter_plan):
            if isinstance(stage, tuple):  # compute an OR group
                filter_plan[i] = self.compute_filter_plan(stage, logic="OR")
            elif isinstance(stage, list):  # compute an AND group
                filter_plan[i] = self.compute_filter_plan(stage, logic="AND")
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


{
    "filters": [
        {
            "name": "on_chr1",
            "model_name": "Variant",
            "field": "chr",
            "django_filter": "iexact",
            "value": "Chr1",
        },
        {
            "name": "ref_is_G",
            "model_name": "Variant",
            "field": "ref",
            "django_filter": "iexact",
            "value": "G",
        },
        {
            "name": "alt_is_T",
            "model_name": "Variant",
            "field": "alt",
            "django_filter": "iexact",
            "value": "T",
        },
        {
            "name": "on_chr2",
            "model_name": "Variant",
            "field": "chr",
            "django_filter": "iexact",
            "value": "Chr2",
        },
        {
            "name": "alt_is_A",
            "model_name": "Variant",
            "field": "alt",
            "django_filter": "iexact",
            "value": "A",
        },
    ],
    "str_plan": "(on_chr1 && (ref_is_G || alt_is_T)) || (on_chr2 && alt_is_A)",
    "dfilter_plan": (["on_chr1", ("ref_is_G", "alt_is_T")], ["on_chr2", "alt_is_A"]),
}
# qs = NodeVariantAnnotation.objects.filter(**variant_filters)
