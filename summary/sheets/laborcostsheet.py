# -*-coding:utf-8 -*-

from summary.sheets.itemsheet import ItemSheet
from summary.models import LaborCost

class LaborCostSheet(ItemSheet) :

    name = u'人工成本-人力'

    model = LaborCost


