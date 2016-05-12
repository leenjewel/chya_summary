# -*-coding:utf-8 -*-

from summary.sheets.costsheet import CostSheet
from summary.models import ManagementCost

class ManagementCostSheet(CostSheet) :

    name = u'管理费用'

    model = ManagementCost



