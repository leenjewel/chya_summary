# -*-coding:utf-8 -*-

from summary.sheets.basesheet import BaseSheet
from summary.models import Profit

class ProfitSheet(BaseSheet) :

    name = u'收入-利润(本部)'

    head = (u'运量',u'收入',u'成本',u'毛利',u'毛利率',u'利润总额',)
    attr = ('traffic', 'income', 'cost', 'gross_profit', 'gross_margin', 'profit_total')

    def parse_head(self) :
        for row_num in range(0, self.sheet.nrows) :
            row_values = self.sheet.row_values(row_num)
            if self.head_row_num is None :
                head_col_num = 0
                self.head_col_from = None
                for col_value in row_values :
                    if col_value == self.head[0] :
                        if self.head_col_from is None :
                            self.head_col_from = head_col_num
                        if self.head_row_num is None :
                            self.head_row_num = row_num
                            return;
                    head_col_num += 1


    def parse_sheet(self, task) :
        if self.head_row_num is None :
            return
        profits = []
        last_group_name = None
        for row_num in range(self.head_row_num + 1, self.sheet.nrows) :
            row_values = self.sheet.row_values(row_num)
            if len(row_values) < self.head_col_from :
                continue
            group_name = self.allstrip(row_values[self.head_col_from - 2])
            if len(group_name) > 0 :
                last_group_name = group_name
            compnay_name = self.allstrip(row_values[self.head_col_from - 1])
            if len(compnay_name) == 0 :
                continue
            profits += self.parse_profit(task, compnay_name, last_group_name, row_num, row_values[self.head_col_from:])
        return profits


    def parse_profit(self, task, compnay_name, group_name, row_num, values) :
        profits = []
        profit = None
        val_num = 0
        month = 1
        head_num = len(self.head)
        compnay_id = self.pinyin(compnay_name)
        year = task.year
        for val in values :
            if 0 == val_num or 0 == val_num % head_num :
                if profit and profit.isQualified() :
                    profits.append(profit)
                try :
                    profit = Profit.objects.get(year = year, month = month, compnay_id = compnay_id)
                except Profit.DoesNotExist, e :
                    profit = Profit()
                profit.year = year
                profit.month = month
                profit.compnay_name = compnay_name
                profit.compnay_id = compnay_id
                profit.hashid = task.hashid
                profit.group_name = group_name
                profit.group_id = self.pinyin(group_name)
                month += 1
            try :
                val = float(val)
                if 0 == val_num :
                    setattr(profit, self.attr[0], val)
                else :
                    setattr(profit, self.attr[val_num % head_num], val)
            except ValueError, e:
                pass
            finally :
                val_num += 1
        return profits


    def parse(self, task) :
        self.parse_head()
        return self.parse_sheet(task)


    @classmethod
    def format(self, hashid) :
        ret = []
        try :
            profits = Profit.objects.filter(hashid = hashid)
            groups = []
            dct = {}
            for profit in profits :
                group_id = profit.group_id
                compnay_id = profit.compnay_id
                if not dct.has_key(group_id) :
                    dct[group_id] = {
                        '__name__' : profit.group_name,
                        '__compnays__' : []
                    }
                    groups.append(group_id)
                group_dct = dct[group_id]
                if not group_dct.has_key(compnay_id) :
                    group_dct[compnay_id] = {}
                    group_dct['__compnays__'].append(compnay_id)
                group_dct[compnay_id]['__name__'] = profit.compnay_name
                group_dct[compnay_id][profit.month] = (
                    profit.traffic,
                    profit.income,
                    profit.cost,
                    profit.gross_profit,
                    profit.gross_margin,
                    profit.profit_total,
                )
            for group_id in groups :
                group_dct = dct[group_id]
                group_name = (group_dct['__name__'])
                compnays = dct[group_id]['__compnays__']
                for compnay_id in compnays :
                    compnay_dct = dct[group_id][compnay_id]
                    compnay_name = compnay_dct['__name__']
                    row = [group_id, group_name, compnay_name]
                    for month in range(1, 14) :
                        if dct[group_id][compnay_id].has_key(month) :
                            row += dct[group_id][compnay_id][month]
                        else:
                            row += [0*x for x in range(0, 6)]
                    ret.append(row)
        except Profit.DoesNotExist, e:
            pass
        else :
            if len(ret) == 0 :
                return u''
            else:
                out = u''
                for l in ret :
                    line = u'<tr><td>' + l[1]
                    line += u'</td><td>'.join([unicode(x) for x in l[1:]])
                    out += line + '</td><tr>'
                return out


