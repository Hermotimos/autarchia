import datetime

from django.db import models


# =============================================================================


def monthdate():
    y, m, _ = str(datetime.date.today()).split('-')
    return f"{y}-{m}"


class MonthManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('days') # less queries, but slower (GCP cheaper)
        return qs


class Month(models.Model):
    objects = MonthManager()

    monthdate = models.TextField(default=monthdate, primary_key=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-monthdate']

    def __str__(self):
        return self.monthdate


# =============================================================================


def thismonth():
    obj, _ = Month.objects.get_or_create(monthdate=monthdate())
    return obj.monthdate


class DayManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('month')
        return qs


class Day(models.Model):
    objects = DayManager()

    date = models.DateField(default=datetime.date.today, primary_key=True)
    month = models.ForeignKey(
        Month, related_name="days", default=thismonth, on_delete=models.PROTECT)
    dreams = models.TextField(blank=True, null=True)
    events = models.TextField(blank=True, null=True)
    ideas = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.date)



# =============================================================================


def thisday():
    obj, _ = Day.objects.get_or_create(date=str(datetime.date.today()))
    return obj.date


class TODOList(models.Model):
    INFO_FIELDS = [
        'comments',
        'awareness', 'happiness', 'openness', 'focus',
        'anger', 'fear', 'emptiness', 'chaos',
    ]
    TODO_FIELDS = []
    CONDITIONS = {}

    MARKS = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    date = models.OneToOneField(
        Day, related_name="todolist", default=thisday, on_delete=models.PROTECT,
        primary_key=True)

    # PSYCHE
    MILAM = models.BooleanField(default=False)
    DREAM = models.BooleanField(default=False)
    SUNWALK = models.BooleanField(default=False)
    MED = models.BooleanField(default=False)
    MED2 = models.BooleanField(default=False)
    MED3 = models.BooleanField(default=False)
    TETRIS = models.BooleanField(default=False)
    SATYR = models.BooleanField(default=False)
    RELAX = models.BooleanField(default=False)

    # KHR
    Mirroring = models.BooleanField(default=False)
    Appreciation = models.BooleanField(default=False)
    Helpfulness = models.BooleanField(default=False)
    SmallTalk = models.BooleanField(default=False)

    # SOMA
    sleep = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    IForKETO = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    drinkfood = models.BooleanField(default=False)
    eat1Hbeforego = models.BooleanField(default=False)
    eatnoshit = models.BooleanField(default=False)
    Mealx4 = models.BooleanField(default=False)
    facecare = models.BooleanField(default=False)
    # --
    flaxseed = models.BooleanField(default=False)
    spirulina = models.BooleanField(default=False)
    greenveggies = models.BooleanField(default=False)
    lionsmane = models.BooleanField(default=False)
    pickles = models.BooleanField(default=False)
    fishoilord3 = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    # --
    coffeex2 = models.BooleanField(default=False)
    noA = models.PositiveSmallIntegerField(default=0)
    # --
    warmup = models.BooleanField(default=False)
    stretching = models.BooleanField(default=False)
    workout = models.TextField(blank=True, null=True)
    MicroW = models.TextField(blank=True, null=True)
    Mass = models.TextField(blank=True, null=True)
    ISO = models.TextField(blank=True, null=True)
    Cardio = models.TextField(blank=True, null=True)

    # NOOS
    RPG = models.BooleanField(default=False)
    CODE = models.BooleanField(default=False)
    ENG = models.BooleanField(default=False)
    DE = models.BooleanField(default=False)
    FR = models.BooleanField(default=False)
    UKR = models.BooleanField(default=False)

    # marks
    awareness = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)
    happiness = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)
    openness = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)
    focus = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)
    anger = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)
    fear = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)
    emptiness = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)
    chaos = models.PositiveSmallIntegerField(choices=MARKS, null=True, blank=True)

    # comments
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date__date']


# ----------------------------------------------------


class TODOList2016EndManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2016")
        return qs


class TODOList2016End(TODOList):
    objects = TODOList2016EndManager()

    TODO_FIELDS = [
        "MED2", "MED3", "SATYR",
        "sleep", "Mealx4", "workout",
    ]
    CONDITIONS = {
        'TRUE': [
            "MED2", "MED3", "SATYR",
            "Mealx4",
        ],
        'ZERO': [],
        'MINIMUM': {
            'sleep': 7,
        },
        'NONEMPTYSTR': [
            'workout',
        ],
        'ONEOF': [],
    }

    class Meta:
        proxy = True
        verbose_name = "TODO 2016[end]"
        verbose_name_plural = "TODOs 2016[end]"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('MED2').verbose_name = 'DoNothing'
        self._meta.get_field('MED3').verbose_name = 'Awareness'


# ----------------------------------------------------


class TODOList2017JanJulManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2017", date__date__month__lte="07")
        return qs


class TODOList2017JanJul(TODOList):
    objects = TODOList2017JanJulManager()

    TODO_FIELDS = [
        "MILAM", "DREAM", "MED", "MED2", "MED3", "SATYR", "RELAX",
        "sleep", "facecare",
        "water", "spirulina", "flaxseed",
        "eat1Hbeforego", "Mealx4", "coffeex2", "noA",
        "warmup",  "workout",
        "ENG", "DE", "FR",
        "Helpfulness", "SmallTalk",
    ]
    CONDITIONS = {
        'TRUE': [
            "MILAM", "DREAM", "MED", "MED2", "MED3", "SATYR", "RELAX",
            "flaxseed", "spirulina", "water",
            "eat1Hbeforego", "Mealx4", "facecare",
            "coffeex2", "warmup",
            "ENG", "DE", "FR",
            "Helpfulness", "SmallTalk",
        ],
        'ZERO': [
            'noA',
        ],
        'MINIMUM': {
            'sleep': 7,
        },
        'NONEMPTYSTR': [
            'workout',
        ],
        'ONEOF': [],
    }

    class Meta:
        proxy = True
        verbose_name = "TODO 2017[1] Jan-Jul"
        verbose_name_plural = "TODOs 2017[1] Jan-Jul"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('MED').verbose_name = 'Mindfulness'
        self._meta.get_field('MED2').verbose_name = 'Contemplation'
        self._meta.get_field('MED3').verbose_name = 'Awareness'


# ----------------------------------------------------


class TODOList2017AugDecManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2017", date__date__month__gte="08")
        return qs


class TODOList2017AugDec(TODOList):
    objects = TODOList2017AugDecManager()

    TODO_FIELDS = [
        "MILAM", "DREAM", "MED", "MED3", "TETRIS", "SATYR", "RELAX",
        "sleep", "facecare",
        "water", "spirulina", "flaxseed", "fishoilord3",
        "eat1Hbeforego", "Mealx4", "coffeex2", "noA",
        "warmup",  "workout",
        "CODE", "ENG", "DE", "FR",
        "Helpfulness", "SmallTalk",
    ]
    CONDITIONS = {
        'TRUE': [
            "MILAM", "DREAM", "MED", "MED3", "TETRIS", "SATYR", "RELAX",
            "flaxseed", "spirulina", "fishoilord3", "water",
            "eat1Hbeforego", "Mealx4", "facecare",
            "coffeex2", "warmup",
            "CODE", "ENG", "DE", "FR",
            "Helpfulness", "SmallTalk",
        ],
        'ZERO': [
            'noA',
        ],
        'MINIMUM': {
            'sleep': 7,
        },
        'NONEMPTYSTR': [
            'workout',
        ],
        'ONEOF': [],
    }

    class Meta:
        proxy = True
        verbose_name = "TODO 2017[2] Aug-Dec"
        verbose_name_plural = "TODOs 2017[2] Aug-Dec"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('MED').verbose_name = 'Mindfulness'
        self._meta.get_field('MED3').verbose_name = 'Awareness'


# ----------------------------------------------------


class TODOList2018Manager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2018")
        return qs


class TODOList2018(TODOList):
    objects = TODOList2018Manager()

    TODO_FIELDS = [
        "MILAM", "DREAM", "MED", "MED2", "MED3", "TETRIS", "SATYR", "RELAX",
        "sleep", "facecare",
        "water", "spirulina", "fishoilord3",
        "eat1Hbeforego", "Mealx4", "coffeex2", "noA",
        "warmup",  "workout",
        "CODE", "ENG", "DE", "FR", "UKR",
        "Mirroring", "Appreciation", "Helpfulness",
    ]
    CONDITIONS = {
        'TRUE': [
            "MILAM", "DREAM", "MED", "MED2", "MED3", "TETRIS", "SATYR", "RELAX",
            "water", "spirulina", "fishoilord3",
            "eat1Hbeforego", "Mealx4", "facecare",
            "coffeex2", "warmup",
            "CODE", "ENG", "DE", "FR", "UKR",
            "Mirroring", "Appreciation", "Helpfulness",
        ],
        'ZERO': [
            'noA',
        ],
        'MINIMUM': {
            'sleep': 7,
        },
        'NONEMPTYSTR': [
            'workout',
        ],
        'ONEOF': [],
    }

    class Meta:
        proxy = True
        verbose_name = "TODO 2018"
        verbose_name_plural = "TODOs 2018"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('MED').verbose_name = 'Mindfulness'
        self._meta.get_field('MED2').verbose_name = 'FOCUS'
        self._meta.get_field('MED3').verbose_name = 'Awareness'


# ----------------------------------------------------


class TODOList2019Manager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2019")
        return qs


class TODOList2019(TODOList):
    objects = TODOList2019Manager()

    TODO_FIELDS = [
        "DREAM", "MED", "MED2", "MED3", "TETRIS", "RELAX",
        "sleep", "facecare",
        "water", "spirulina", "fishoilord3",
        "eat1Hbeforego", "coffeex2", "noA", "eatnoshit", "IForKETO", "drinkfood",
        "warmup", "workout",
        "RPG", "CODE", "ENG", "DE", "FR", "UKR",
    ]
    CONDITIONS = {
        'TRUE': [
            "DREAM", "MED", "MED2", "MED3", "TETRIS", "RELAX",
            "spirulina", "fishoilord3", "water", "drinkfood",
            "eat1Hbeforego", "eatnoshit", "facecare",
            "coffeex2", "warmup", "stretching",
            "RPG", "CODE", "ENG", "DE", "FR", "UKR",
        ],
        'ZERO': [
            'noA',
        ],
        'MINIMUM': {
            'sleep': 7, 'IForKETO': 12,
        },
        'NONEMPTYSTR': [
            'workout',
        ],
        'ONEOF': [],
    }

    class Meta:
        proxy = True
        verbose_name = "TODO 2019"
        verbose_name_plural = "TODOs 2019"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('MED').verbose_name = 'Mindfulness'
        self._meta.get_field('MED2').verbose_name = 'FOCUS'
        self._meta.get_field('MED3').verbose_name = 'DoNothing'


# ----------------------------------------------------


class TODOList2020Manager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2020")
        return qs


class TODOList2020(TODOList):
    objects = TODOList2020Manager()

    TODO_FIELDS = [
        "DREAM", "MED", "MED2", "MED3", "TETRIS", "RELAX",
        "sleep",
        "water", "spirulina", "fishoilord3", "flaxseed",
        "coffeex2", "noA", "IForKETO", "drinkfood",
        "warmup", "workout",
        "RPG", "CODE", "ENG", "DE", "FR", "UKR",
    ]
    CONDITIONS = {
        'TRUE': [
            "DREAM", "MED", "MED2", "MED3", "TETRIS", "RELAX",
            "flaxseed", "spirulina", "fishoilord3", "water", "drinkfood",
            "coffeex2", "warmup",
            "RPG", "CODE", "ENG", "DE", "FR", "UKR",
        ],
        'ZERO': [
            'noA',
        ],
        'MINIMUM': {
            'sleep': 7, 'IForKETO': 12,
        },
        'NONEMPTYSTR': [
            'workout',
        ],
        'ONEOF': [],
    }

    class Meta:
        proxy = True
        verbose_name = "TODO 2020"
        verbose_name_plural = "TODOs 2020"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('MED').verbose_name = 'Mindfulness'
        self._meta.get_field('MED2').verbose_name = 'FOCUS'
        self._meta.get_field('MED3').verbose_name = 'Contemplation'


# ----------------------------------------------------


class TODOList2021Manager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2021")
        return qs


class TODOList2021(TODOList):
    objects = TODOList2021Manager()

    TODO_FIELDS = [
        "MED", "MED2", "MED3", "TETRIS", "RELAX",
        "sleep",
        "water", "spirulina", "fishoilord3", "flaxseed",
        "coffeex2", "noA", "IForKETO", "drinkfood",
        "warmup", "MicroW", "Mass", "ISO", "Cardio", "stretching",
        "RPG", "CODE", "ENG", "DE", "FR", "UKR",
    ]
    CONDITIONS = {
        'TRUE': [
            "MED", "MED2", "MED3", "TETRIS", "RELAX",
            "flaxseed", "spirulina", "fishoilord3", "water", "drinkfood",
            "coffeex2", "warmup", "stretching",
            "RPG", "CODE", "ENG", "DE", "FR", "UKR",
        ],
        'ZERO': [
            'noA',
        ],
        'MINIMUM': {
            'sleep': 7, 'IForKETO': 14,
        },
        'NONEMPTYSTR': [],
        'ONEOF': [
            "MicroW", "Mass", "ISO", "Cardio",
        ],
    }

    class Meta:
        proxy = True
        verbose_name = "TODO 2021"
        verbose_name_plural = "TODOs 2021"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('MED').verbose_name = 'FOCUS'
        self._meta.get_field('MED2').verbose_name = 'Mindfulness'
        self._meta.get_field('MED3').verbose_name = 'FOCUS'


# ----------------------------------------------------


class TODOList2022Manager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2022")
        return qs


class TODOList2022(TODOList2021):
    objects = TODOList2022Manager()

    class Meta:
        proxy = True
        verbose_name = "TODO 2022"
        verbose_name_plural = "TODOs 2022"


# ----------------------------------------------------


class TODOList2023Manager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(date__date__year="2023")
        return qs


class TODOList2023(TODOList):
    objects = TODOList2023Manager()

    TODO_FIELDS = [
        'SUNWALK', 'MED', 'TETRIS', 'RELAX',
        'sleep',
        'water', 'greenveggies', 'fishoilord3', 'flaxseed', 'lionsmane', 'pickles',
        'coffeex2', 'noA', 'IForKETO', 'drinkfood',
        'warmup', 'workout', 'stretching',
        'CODE', 'ENG', 'DE', 'FR', 'UKR',
    ]
    CONDITIONS = {
        'TRUE': [
            'SUNWALK', 'MED', 'TETRIS', 'RELAX',
            'drinkfood', 'flaxseed', 'greenveggies', 'lionsmane', 'pickles',
            'fishoilord3', 'water', 'coffeex2', 'warmup', 'stretching',
            'CODE', 'ENG', 'DE', 'FR', 'UKR',
        ],
        'ZERO': [
            'noA',
        ],
        'MINIMUM': {
            'sleep': 7, 'IForKETO': 14,
        },
        'NONEMPTYSTR': [
            'workout',
        ],
        'ONEOF': [],
    }

    class Meta:
        ordering = ['-date__date']
        proxy = True
        verbose_name = "TODO 2023"
        verbose_name_plural = "TODOs 2023"


# =============================================================================


class Food(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fiber = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ['name']


# class Serving(models.Model):
#     food = models.ForeignKey(to=Food, on_delete=models.PROTECT)
#     size = models.DecimalField(max_digits=5, decimal_places=2, default=0)

#     class Meta:
#         ordering = ['id']


# class DailyServings(models.Model):
#     date = models.DateField(default=datetime.date.today, unique=True)
#     servings = models.ManyToManyField(to=Serving)

#     class Meta:
#         ordering = ['-date']

# from django.contrib.contenttypes.models import ContentType
# content_type = ContentType.objects.filter(model=c_type)
# print(content_type)


