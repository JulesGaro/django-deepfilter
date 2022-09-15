from pseudo import compute_filter_plan, compute_filters
from filters import *

queryset = [
    444515444,
    333515333,
    515,
    5151,
    1111111,
    2222222,
    1166611,
    515111111111111111111,
]  # base queryset

# define the filters :
f1 = Int_up(base_queryset=queryset, name="f1", value=1000)
f2 = String_len_up(base_queryset=queryset, name="f2", value=5)
f3 = String_contain(base_queryset=queryset, name="f3", value="515")
f4 = String_len_lo_eq(base_queryset=queryset, name="f4", value=12)
f5 = Int_eq(base_queryset=queryset, name="f5", value=1166611)
f6 = String_contain(base_queryset=queryset, name="f3", value="5154")

filters = [f1, f2, f3, f4, f5, f6]  # list of the filters

# complex filter structure
# elements in a list will be group with an AND logic
# elements in a tuple will be group with an OR logic
filter_plan = [
    [
        [
            [f1.queryset, f2.queryset],
            ([f3.queryset, f4.queryset], f5.queryset),
        ],
        f6.queryset,
    ]
]  # --> (f1 && f2) && ( (f3 && f4) || e1)


compute_filters(filters=filters)

# magic !
print(f"final : {compute_filter_plan(filter_plan=filter_plan, queryset=queryset)}")
