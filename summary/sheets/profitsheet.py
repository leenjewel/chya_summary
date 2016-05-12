# -*-coding:utf-8 -*-

from summary.sheets.basesheet import BaseSheet
from summary.models import Profit

class ProfitSheet(BaseSheet) :

    name = u'收入-利润(本部)'

    head = (u'运量',u'收入',u'成本',u'毛利',u'毛利率',u'利润总额',)
    attr = ('traffic', 'income', 'cost', 'gross_profit', 'gross_margin', 'profit_total')

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
            if u'合计' == group_name :
                continue
            if len(group_name) > 0 :
                last_group_name = group_name
            compnay_name = self.allstrip(row_values[self.head_col_from - 1])
            if len(compnay_name) == 0 :
                continue
            if u'合计' == compnay_name :
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
                    profit.save()
                    profits.append(profit)
                try :
                    profit = Profit.objects.get(hashid = task.hashid, year = year, month = month, compnay_id = compnay_id)
                except Profit.DoesNotExist, e :
                    profit = Profit()
                profit.line = row_num
                profit.year = year
                profit.month = month
                profit.compnay_name = compnay_name
                profit.compnay_id = compnay_id
                compnay_split = compnay_id.split('-')
                profit.man_id = compnay_split[0]
                compnay_split_len = len(compnay_split)
                if compnay_split_len > 1 :
                    profit.sub_id = compnay_split[1]
                else :
                    profit.sub_id = ""
                if compnay_split_len > 2 :
                    profit.trd_id = compnay_split[2]
                else :
                    profit.trd_id = ""
                profit.hashid = task.hashid
                profit.group_name = group_name
                profit.group_id = self.pinyin(group_name)
                month += 1
            try :
                key = self.attr_key_by_col(self.head_col_from + val_num)
                if key is None :
                    raise ValueError()
                val = float(val)
                if 'gross_margin' == key and (profit.gross_profit == 0 or profit.income == 0) :
                    val = 0
                setattr(profit, key, val)
            except ValueError, e:
                pass
            finally :
                val_num += 1
        return profits


    def parse(self, task) :
        self.parse_head()
        return self.parse_sheet(task)


    @classmethod
    def format(cls, hashid) :
        ret = []
        try :
            profits = Profit.objects.filter(hashid = hashid).order_by('line')
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
                        {'val' : profit.traffic, 'tip' : u'_'.join([profit.compnay_name, unicode(profit.month)+u'月', cls.head[0]])},
                        {'val' : profit.income, 'tip' : u'_'.join([profit.compnay_name, unicode(profit.month)+u'月', cls.head[1]])  },
                        {'val' : profit.cost, 'tip' : u'_'.join([profit.compnay_name, unicode(profit.month)+u'月', cls.head[2]])  },
                        {'val' : profit.gross_profit, 'tip' : u'_'.join([profit.compnay_name, unicode(profit.month)+u'月', cls.head[3]])  },
                        {'val' : profit.gross_margin, 'tip' : u'_'.join([profit.compnay_name, unicode(profit.month)+u'月', cls.head[4]])  },
                        {'val' : profit.profit_total, 'tip' : u'_'.join([profit.compnay_name, unicode(profit.month)+u'月', cls.head[5]])  },
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
                            row += [{'val' : 0.0, 'tip' : u'_'.join([compnay_name, unicode(month)+u'月', cls.head[x]])} for x in range(0, 6)]
                    ret.append(row)
        except Profit.DoesNotExist, e:
            pass
        finally :
            if len(ret) == 0 :
                return u''
            else:
                out = u''
                for l in ret :
                    line = u'<tr><td>' + l[1] + u'</td><td>' + l[2] + u'</td>'
                    line += u''.join([u'<td data-toggle="tooltip" data-placement="top" title="'+x['tip']+u'">'+unicode(x['val'])+u'</td>' for x in l[3:]])
                    out += line + '</tr>'
                return out


