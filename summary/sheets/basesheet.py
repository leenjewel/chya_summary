# -*-coding:utf-8 -*-

from anjuke import pinyin
import re
import xlrd

class BaseSheet(object) :

    pinyin_converter = pinyin.Converter()

    name = None
    sheet = None
    head = None
    attr = None
    head_row_num = None
    head_col_from = None
    head_row_values = None

    def __init__(self, workbook) :
        try :
            self.sheet = workbook.sheet_by_name(self.name)
        except xlrd.biffh.XLRDError:
            self.sheet = workbook.sheet_by_name(self.allstrip(self.name))

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
                        if self.head_row_values is None :
                            self.head_row_values = row_values
                            return;
                    head_col_num += 1

    def attr_key_by_col(self, col_num) :
        try :
            col_head_val = self.allstrip(self.head_row_values[col_num])
            head_index = self.head.index(col_head_val)
            return self.attr[head_index]
        except ValueError :
            return None
        except IndexError :
            return None


    def pinyin(self, txt) :
        pinyin = self.pinyin_converter.convert(unicode(txt), fmt='df', sc=False)
        return self.allstrip(pinyin)


    def allstrip(self, txt) :
        if not isinstance(txt, str) and not isinstance(txt, unicode) :
            return u''
        return re.sub(r"\s+", "", txt.strip().replace(' ',''), flags=re.UNICODE)

