from statistics import mean

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.safestring import SafeString, mark_safe

from todos.admin_utils import (
    a_monthly, compl_daily, compl_monthly, format_a, format_compl,

)
from todos.models import (
    Food, Month,
    TODOList2016End, TODOList2017JanJul, TODOList2017AugDec, TODOList2018,
    TODOList2019, TODOList2020, TODOList2021, TODOList2022, TODOList2023,
)


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    date_hierarchy = 'days__daydate'
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
    }
    list_display = ['monthdate', 'completion', 'noA', 'comments']
    list_editable = ['comments']

    def completion(self, obj):
        try:
            return format_compl(compl_monthly(obj))
        except ZeroDivisionError:
            pass

    def noA(self, obj):
        try:
            return format_a(a_monthly(obj))
        except ZeroDivisionError:
            pass

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('days')
        return qs


# ----------------------------------------------------


class TODOListAdmin(admin.ModelAdmin):
    """An abstract ModelAdmin that serves as template via subclassing."""
    ADMIN_FIELDS_1 = ['daydate']
    ADMIN_FIELDS_2 = ['res', 'compl']
    date_hierarchy = 'daydate'
    formfield_overrides = {
        models.PositiveSmallIntegerField: {'widget': forms.NumberInput(attrs={'style': 'width:35px'})},
        models.DecimalField: {'widget': forms.NumberInput(attrs={'style': 'width:55px'})},
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 25})},
    }

    class Media:
        css = {
            'all': (f'{settings.STATIC_URL}css/todos.css',)
        }

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


@admin.register(TODOList2016End)
class TODOList2016EndAdmin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2016End.TODO_FIELDS,
        *TODOList2016End.INFO_FIELDS,
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 15})},
    }
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2016End.TODO_FIELDS,
        *TODOList2016End.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]


@admin.register(TODOList2017JanJul)
class TODOList2017JanJulAdmin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2017JanJul.TODO_FIELDS,
        *TODOList2017JanJul.INFO_FIELDS,
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 15})},
    }
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2017JanJul.TODO_FIELDS,
        *TODOList2017JanJul.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]


@admin.register(TODOList2017AugDec)
class TODOList2017AugDecAdmin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2017AugDec.TODO_FIELDS,
        *TODOList2017AugDec.INFO_FIELDS,
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 15})},
    }
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2017AugDec.TODO_FIELDS,
        *TODOList2017AugDec.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]



@admin.register(TODOList2018)
class TODOList2018Admin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2018.TODO_FIELDS,
        *TODOList2018.INFO_FIELDS,
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 15})},
    }
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2018.TODO_FIELDS,
        *TODOList2018.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]


@admin.register(TODOList2019)
class TODOList2019Admin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2019.TODO_FIELDS,
        *TODOList2019.INFO_FIELDS,
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 15})},
    }
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2019.TODO_FIELDS,
        *TODOList2019.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]


@admin.register(TODOList2020)
class TODOList2020Admin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2020.TODO_FIELDS,
        *TODOList2020.INFO_FIELDS,
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 15})},
    }
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2020.TODO_FIELDS,
        *TODOList2020.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]


@admin.register(TODOList2021)
class TODOList2021Admin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2021.TODO_FIELDS,
        *TODOList2021.INFO_FIELDS,
    ]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 15})},
    }
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2021.TODO_FIELDS,
        *TODOList2021.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]


@admin.register(TODOList2022)
class TODOList2022Admin(TODOList2021Admin):
    pass


@admin.register(TODOList2023)
class TODOList2023Admin(TODOListAdmin):
    fields = ['month', 'daydate'] + [
        *TODOList2023.TODO_FIELDS,
        *TODOList2023.INFO_FIELDS,
    ]
    list_display = [
        *TODOListAdmin.ADMIN_FIELDS_1,
        *TODOList2023.TODO_FIELDS,
        *TODOList2023.INFO_FIELDS,
        *TODOListAdmin.ADMIN_FIELDS_2,
    ]
    list_editable = [
        *TODOList2023.TODO_FIELDS,
        *TODOList2023.INFO_FIELDS,
    ]


# ----------------------------------------------------


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'fat', 'protein', 'carbs', 'fiber']
    list_editable = ['name', 'fat', 'protein', 'carbs', 'fiber']
    list_per_page = 1000
