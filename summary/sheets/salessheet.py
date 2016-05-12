# -*-coding:utf-8 -*-

from summary.sheets.costsheet import CostSheet
from summary.models import Sales

class SalesSheet(CostSheet) :

    name = u'销售费用 '

    model = Sales


