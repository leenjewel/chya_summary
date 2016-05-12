# -*-coding:utf-8 -*-

from summary.sheets.itemsheet import ItemSheet
from summary.models import Depreciation

class DepreciationSheet(ItemSheet) :

    use_group = True

    name = u'折旧（汇总）'

    model = Depreciation


