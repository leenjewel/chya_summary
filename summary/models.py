# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Profit(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    compnay_id   = models.CharField(max_length = 64)
    compnay_name = models.CharField(max_length = 64)
    group_id     = models.CharField(max_length = 64)
    group_name   = models.CharField(max_length = 64)
    man_id       = models.CharField(max_length = 32)
    sub_id       = models.CharField(max_length = 32)
    trd_id       = models.CharField(max_length = 32)
    hashid       = models.CharField(max_length = 32)
    traffic      = models.FloatField(default = 0)  # 运量
    income       = models.FloatField(default = 0)  # 收入
    cost         = models.FloatField(default = 0)  # 成本
    gross_profit = models.FloatField(default = 0)  # 毛利
    gross_margin = models.FloatField(default = 0)  # 毛利率
    profit_total = models.FloatField(default = 0)  # 利润总额

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'compnay_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )

    def isQualified(self) :
        return (self.traffic <> 0 or self.income <> 0 or self.cost <> 0 or self.gross_profit <> 0 or self.gross_margin <> 0 or self.profit_total <> 0)


class Cost(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    item_control = models.BooleanField()
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class Sales(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    item_control = models.BooleanField()
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class ManagementCost(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    item_control = models.BooleanField()
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class FinancialExpenses(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    group_name   = models.CharField(max_length = 32)
    group_id     = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class TaxesPayable(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    group_name   = models.CharField(max_length = 32)
    group_id     = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class TaxesPaid(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    group_name   = models.CharField(max_length = 32)
    group_id     = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class LaborCost(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    group_name   = models.CharField(max_length = 32)
    group_id     = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class Depreciation(models.Model) :

    line         = models.IntegerField()
    year         = models.IntegerField()  # 年份
    month        = models.IntegerField()  # 月份
    hashid       = models.CharField(max_length = 32)
    group_name   = models.CharField(max_length = 32)
    group_id     = models.CharField(max_length = 32)
    item_name    = models.CharField(max_length = 32)
    item_id      = models.CharField(max_length = 32)
    value        = models.FloatField(default = 0.0)

    class Meta :
        unique_together = (('hashid', 'year', 'month', 'item_id',),)
        index_together = (
            ('hashid', 'line', 'month',),
        )


class ParseTask(models.Model) :

    hashid = models.CharField(max_length = 32, primary_key = True)
    author = models.CharField(max_length = 32, db_index = True, default = '__nobody__')
    year = models.IntegerField()
    hasparsed = models.BooleanField(default = False)
    isparseing = models.BooleanField(default = False)
    filename = models.CharField(max_length = 128)
    parsefile = models.FileField(upload_to = "workbook/%Y/%m/%d/")

