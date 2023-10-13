import datetime
from statistics import mean

from django import forms
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import SafeString, mark_safe

from todos.admin_utils import (
    a_monthly, compl_daily, compl_monthly, format_a, format_compl,
)
from todos.models import Year, Month, Day, Food



@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
    }
    list_display = ['yeardate', 'comments']
    list_editable = ['comments']



@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    date_hierarchy = 'daydate'
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
    }
    list_display = ['daydate', 'month', 'dreams', 'events', 'ideas']
    list_editable = ['dreams', 'events', 'ideas']


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    date_hierarchy = 'days__daydate'
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
    }
    list_display = ['monthdate', 'show_todos', 'completion', 'noA', 'comments']
    list_editable = ['comments']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('days__todolist')
        qs = qs.select_related('year')
        return qs

    @admin.display
    def completion(self, obj):
        try:
            return format_compl(compl_monthly(obj))
        except ZeroDivisionError:
            pass

    @admin.display
    def noA(self, obj):
        try:
            return format_a(a_monthly(obj))
        except ZeroDivisionError:
            pass

    @admin.display(description="TODO List")
    def show_todos(self, obj):
        year, month = obj.monthdate.split('-')
        year, month = int(year), int(month)

        if year == 2016:
            affix = "2016end"
        elif year == 2017 and month in [1, 2, 3, 4, 5, 6, 7]:
            affix = "2017janjul"
        elif year == 2017 and month in [8, 9, 10, 11, 12]:
            affix = "2017augdec"
        else:
            affix = year

        url = (
            reverse(f"admin:todos_todolist{affix}_changelist")
            + "?"
            + urlencode({f"date__daydate__month": month})
            + "&"
            + urlencode({f"date__daydate__year": year})
        )
        html = '<a href="{}" style="border: 1px solid; padding: 2px 3px;" target="_blank">Month TODOs</a>'
        return format_html(html, url)


# ----------------------------------------------------


class TODOListAdmin(admin.ModelAdmin):
    """An abstract ModelAdmin that serves as template via subclassing."""
    date_hierarchy = 'date__daydate'
    formfield_overrides = {
        models.PositiveSmallIntegerField: {'widget': forms.NumberInput(attrs={'style': 'width:35px'})},
        models.DecimalField: {'widget': forms.NumberInput(attrs={'style': 'width:55px'})},
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 25})},
    }

    class Media:
        css = {
            'all': (f'{settings.STATIC_URL}css/todos.css',)
        }

    def __init__(self, model, admin_site) -> None:
        self.fields = [
            'date',
            *model.TODO_FIELDS,
            *model.INFO_FIELDS,
        ]
        self.list_display = [
            'date',
            'go_to_day',
            *model.TODO_FIELDS,
            *model.INFO_FIELDS,
            'res',
            'compl',
        ]
        super().__init__(model, admin_site)

    def res(self, obj) -> str:
        try:
            sum_plus = mean([obj.awareness, obj.happiness, obj.openness, obj.focus])
            sum_minus = mean([obj.anger, obj.fear, obj.emptiness, obj.chaos])
            res = sum_plus - sum_minus

            if res < 1.1:
                color = "red"
            elif res < 2.1:
                color = "gold"
            elif res < 3.1:
                color = "deepskyblue"
            elif res < 4.1:
                color = "blueviolet"
            else:
                color = "white"

            return mark_safe(f'<span style="color: {color}"><b>{res}</b></span>')

        except TypeError:
            return "-"

    def compl(self, obj) -> SafeString:
        return format_compl(compl_daily(obj))

    @admin.display(description="Go To Day")
    def go_to_day(self, obj):
        url = (
            reverse("admin:todos_day_changelist")
            + "?"
            + urlencode({"todolist__date": f"{obj.date}"})
        )
        html = '<a href="{}" style="border: 1px solid; padding: 2px 3px;" target="_blank">GO</a>'
        return format_html(html, url)


"""
Automatically register all TODOList[year] proxy models.
Add 'list_editable' attribute only in the current year's TODOList.

This ensures that by simply creating another a proxy models for the 'new' year
will be enough to start using it.
"""
app_models = apps.get_app_config('todos').get_models()
for TODOModel in filter(lambda a: 'TODO' in str(a) and a._meta.proxy, app_models):
    try:
        class_dict = {}
        if str(datetime.date.today().year) in str(TODOModel):
            class_dict = {
                'list_editable': [
                    *TODOModel.TODO_FIELDS,
                    *TODOModel.INFO_FIELDS,
                ]
            }
        admin_cls = type(f'{TODOModel.__name__}Admin', (TODOListAdmin,), class_dict)
        admin.site.register(TODOModel, admin_cls)
    except AlreadyRegistered:
        pass



# @admin.register(TODOList2016End)
# class TODOList2016EndAdmin(TODOListAdmin):
#     pass


# @admin.register(TODOList2017JanJul)
# class TODOList2017JanJulAdmin(TODOListAdmin):
#     pass


# @admin.register(TODOList2017AugDec)
# class TODOList2017AugDecAdmin(TODOListAdmin):
#     pass


# @admin.register(TODOList2018)
# class TODOList2018Admin(TODOListAdmin):
#     pass


# @admin.register(TODOList2019)
# class TODOList2019Admin(TODOListAdmin):
#     pass


# @admin.register(TODOList2020)
# class TODOList2020Admin(TODOListAdmin):
#     pass


# @admin.register(TODOList2022)
# class TODOList2022Admin(TODOListAdmin):
#     pass

# print(TODOList2022Admin, TODOList2022Admin.__bases__)
# @admin.register(TODOList2023)
# class TODOList2023Admin(TODOListAdmin):
#     list_editable = [
#         *TODOList2023.TODO_FIELDS,
#         *TODOList2023.INFO_FIELDS,
#     ]


# ----------------------------------------------------


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'fat', 'protein', 'carbs', 'fiber']
    list_editable = ['name', 'fat', 'protein', 'carbs', 'fiber']
    list_per_page = 1000
