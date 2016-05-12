# -*-coding:utf-8 -*-

from summary.sheets.basesheet import BaseSheet

class ItemSheet(BaseSheet) :

    model = None
    use_group = False

    head = (u'项目', u'1月', u'2月', u'3月', u'4月', u'5月', u'6月', u'7月', u'8月', u'9月', u'10月', u'11月', u'12月', u'累计',)
    attr = ('item_name', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,)

    def parse(self, task) :
        self.parse_head()
        if self.head_row_num is None :
            return
        year = task.year
        xiaoji = 1
        last_group_name = ""
        for row_num in range(self.head_row_num + 1, self.sheet.nrows) :
            row_values = self.sheet.row_values(row_num)
            try :
                item_name = row_values[self.head_col_from]
                if None is item_name or len(item_name) == 0 :
                    continue
                item_name = self.allstrip(item_name)
                # if u'合计' == item_name :
                #     continue
                if u'小计' == item_name :
                    item_id = self.pinyin(item_name + u'_' + unicode(xiaoji))
                    xiaoji += 1
                else :
                    item_id = self.pinyin(item_name)
                group_name = ""
                if self.use_group :
                    try :
                        group_name = self.allstrip(row_values[self.head_col_from-1])
                    except IndexError:
                        group_name = ""
                    if len(group_name) > 0 :
                        last_group_name = group_name
                    if len(last_group_name) > 0 :
                        item_id = self.pinyin(last_group_name) + u'-' +item_id
                col_num = self.head_col_from + 1
                for val in row_values[col_num :]:
                    month = self.attr_key_by_col(col_num)
                    if not isinstance(month, int) :
                        col_num += 1
                        continue
                    try :
                        amodel = self.model.objects.get(hashid = task.hashid, year = year, month = month, item_id = item_id)
                    except self.model.DoesNotExist :
                        amodel = self.model()
                        amodel.line = row_num
                        amodel.year = year
                        amodel.month = month
                        amodel.hashid = task.hashid
                        amodel.item_id = item_id
                        amodel.item_name = item_name
                        amodel.group_name = last_group_name
                        amodel.group_id = self.pinyin(last_group_name)
                    try :
                        amodel.value = float(val)
                    except ValueError :
                        amodel.value = 0.0
                    amodel.save()
                    col_num += 1
            except IndexError:
                continue


    @classmethod
    def format(cls, hashid) :
        ret = []
        try :
            amodel_list = []
            amodels = cls.model.objects.filter(hashid = hashid).order_by('line', 'month')
            for amodel in amodels :
                if len(amodel_list) > 0 and 1 == amodel.month :
                    amodel_list.append(u'</tr>')
                    ret.append(u''.join(amodel_list))
                    amodel_list = []
                if len(amodel_list) == 0 :
                    if u'可控费用小计' == amodel.item_name \
                        or u'不可控费用小计' == amodel.item_name \
                        or u'小计' == amodel.item_name :
                        amodel_list.append(u'<tr class="alert-info">')
                    elif u'累计' == amodel.item_name \
                        or u'合计' == amodel.item_name :
                        amodel_list.append(u'<tr class="alert-success">')
                    else :
                        amodel_list.append(u'<tr>')
                    if cls.use_group :
                        amodel_list.append(u'<td>'+amodel.group_name+u'</td>')
                    amodel_list.append(u'<td>'+amodel.item_name+u'</td>')
                if amodel.month < 13 :
                    amodel_list.append(u'<td data-toggle="tooltip" data-placement="top" title="'+amodel.item_name+u'_'+unicode(amodel.month)+u'月份">' + unicode(amodel.value) + '</td>')
                else :
                    amodel_list.append(u'<td data-toggle="tooltip" data-placement="top" title="'+amodel.item_name+u'_累计">' + unicode(amodel.value) + '</td>')
            amodel_list.append(u'</tr>')
            ret.append(u''.join(amodel_list))
        except cls.DoesNotExist :
            pass
        finally :
            return u'\n'.join(ret)

