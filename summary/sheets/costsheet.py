# -*-coding:utf-8 -*-

from summary.sheets.basesheet import BaseSheet
from summary.models import Cost

class CostSheet(BaseSheet) :

    name = u'成本明细'

    model = Cost

    head = (u'项目', u'1月', u'2月', u'3月', u'4月', u'5月', u'6月', u'7月', u'8月', u'9月', u'10月', u'11月', u'12月', u'累计',)
    attr = ('item_name', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,)

    def parse(self, task) :
        self.parse_head()
        if self.head_row_num is None :
            return
        year = task.year
        item_control = False
        for row_num in range(self.head_row_num + 1, self.sheet.nrows) :
            row_values = self.sheet.row_values(row_num)
            try :
                item_name = row_values[self.head_col_from]
                if None is item_name or len(item_name) == 0 :
                    continue
                item_name = self.allstrip(item_name)
                if u'合计' == item_name :
                    continue
                item_id = self.pinyin(item_name)
                col_num = self.head_col_from + 1
                for val in row_values[col_num :]:
                    month = self.attr_key_by_col(col_num)
                    if not isinstance(col_num, int) :
                        col_num += 1
                        continue
                    try :
                        cost = self.model.objects.get(year = year, month = month, item_id = item_id)
                    except self.model.DoesNotExist :
                        cost = self.model()
                        cost.line = row_num
                        cost.year = year
                        cost.month = month
                        cost.hashid = task.hashid
                        cost.item_id = item_id
                        cost.item_name = item_name
                        cost.item_control = item_control
                    try :
                        cost.value = float(val)
                    except ValueError :
                        cost.value = 0.0
                    cost.save()
                    col_num += 1
                if u'不可控费用小计' == item_name :
                    item_control = True
            except IndexError:
                continue


    @classmethod
    def format(cls, hashid) :
        ret = []
        try :
            cost_list = []
            costs = cls.model.objects.filter(hashid = hashid).order_by('line', 'month')
            for cost in costs :
                if len(cost_list) == 14 :
                    ret.append(cost_list)
                    cost_list = []
                if len(cost_list) == 0 :
                    if u'可控费用小计' == cost.item_name or u'不可控费用小计' == cost.item_name :
                        cost_list.append(u'<tr class="alert-success"><td>' + cost.item_name + u'</td>')
                    else :
                        cost_list.append(u'<tr><td>'+cost.item_name+u'</td>')
                if cost.month < 13 :
                    cost_list.append(u'<td data-toggle="tooltip" data-placement="top" title="'+cost.item_name+u'_'+unicode(cost.month)+u'月份">' + unicode(cost.value) + '</td>')
                else :
                    cost_list.append(u'<td data-toggle="tooltip" data-placement="top" title="'+cost.item_name+u'_累计">' + unicode(cost.value) + '</td>')
            ret.append(cost_list)
        except cls.DoesNotExist :
            pass
        finally :
            return u'\n'.join([u''.join(x)+u'</tr>' for x in ret])

