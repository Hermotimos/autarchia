from functools import cache
from typing import List

from django.apps import apps
from django.utils.html import format_html
from django.utils.safestring import SafeString

from todos.models import TODOList, Month, Day


def get_model_by_date(obj: TODOList):
    year = str(obj.date).split('-')[0]
    for model in apps.get_app_config('todos').get_models():
        if year in model.__name__:
            return model


def compl_daily(obj: TODOList) -> int:
    model = get_model_by_date(obj)

    def value(field_name: str) -> List[str]:
        return getattr(obj, field_name)

    def istrue_cnt() -> int:
        return sum(
            value(f) is True for f in model.CONDITIONS['TRUE']
        )

    def iszero_cnt() -> int:
        return sum(
            value(f) == 0 for f in model.CONDITIONS['ZERO']
        )

    def ismin_cnt() -> int:
        return sum(
            value(k) >= v for k, v in
            model.CONDITIONS['MINIMUM'].items()
        )

    def isnonempty_cnt() -> int:
        return sum(
            value(f) != "" for f in
            model.CONDITIONS['NONEMPTYSTR']
        )

    def isoneof_cnt() -> int:
        return 1 if sum(1 for f in model.CONDITIONS['ONEOF'] if value(f) != "") > 0 else 0

    # # print(obj.daydate)

    try:
        sum_completed = istrue_cnt() + iszero_cnt() + ismin_cnt() + isnonempty_cnt() + isoneof_cnt()
        sum_todo = sum(len(v) for k, v in model.CONDITIONS.items() if k != 'ONEOF')
        if obj.date.daydate.year in [2021, 2022]:
            # Add 1 for 'ONEOF' conditions in years 2021 and 2022
            sum_todo += 1
        # print(obj, sum_completed, sum_todo)
        return int(round(sum_completed / sum_todo * 100, 0))
    except AttributeError:
        return 0
    # except TypeError:
    #     return 0


# -----------------------------------------------------------------------------


def _month_todolists(obj: Month) -> list[TODOList]:
    return [day.todolist for day in obj.days.all()]


def compl_monthly(obj: Month) -> int:
    sum_total = sum(compl_daily(todolist) for todolist in _month_todolists(obj))
    num_days = obj.days.count()
    return int(round(sum_total / num_days))


def a_monthly(obj: Month) -> int:
    try:
        return sum(todolist.noA for todolist in _month_todolists(obj))
    except TypeError:
        return "-"


# -----------------------------------------------------------------------------


def color_ranges(colors: list) -> dict:
    step = int(100 / len(colors))
    res = {}
    lower, upper = 0, step
    for color in colors:
        if upper + step > 100:
            res[range(lower+1, 101)] = color
            break
        res[range(0 if lower == 0 else lower+1, upper+1)] = color
        lower, upper = lower + step, upper + step
    return res


DOS_COLORS = ["#ff0000", "#ffa700", "#2cba00", "#7fff00"]
DOS_COLOR_RANGES = color_ranges(DOS_COLORS)
DONTA_COLORS = ["#2596be", "#2cba00", "#ECF126", "#ffa700", "#ff0000", "#21130d"]
DONTA_COLOR_RANGES = color_ranges(DONTA_COLORS)


def get_color(val: int, colors: dict) -> str:
    for val_range, code in colors.items():
        if val in val_range:
            return code


@cache
def format_compl(value: int) -> SafeString:
    return format_html(
        f'<b style="color: {get_color(value, DOS_COLOR_RANGES)}">{value} %</b>')


@cache
def format_a(value: int) -> SafeString:
    return format_html(
        f'<b style="color: {get_color(value, DONTA_COLOR_RANGES)}">{value}</b>')


# -----------------------------------------------------------------------------



