# -*-coding:utf-8 -*-

from summary.sheets.itemsheet import ItemSheet
from summary.models import FinancialExpenses

class FinancialExpensesSheet(ItemSheet) :

    name = u'财务费用'

    model = FinancialExpenses

