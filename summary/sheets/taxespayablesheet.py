# -*-coding:utf-8 -*-

from summary.sheets.itemsheet import ItemSheet
from summary.models import TaxesPayable

class TaxesPayableSheet(ItemSheet) :

    name = u'应交税金'

    model = TaxesPayable

