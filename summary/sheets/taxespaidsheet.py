# -*-coding:utf-8 -*-

from summary.sheets.itemsheet import ItemSheet
from summary.models import TaxesPaid

class TaxesPaidSheet(ItemSheet) :

    name = u'已交税金 '

    model = TaxesPaid


