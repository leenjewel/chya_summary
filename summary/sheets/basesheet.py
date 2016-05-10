# -*-coding:utf-8 -*-

from anjuke import pinyin
import re

class BaseSheet(object) :

    pinyin_converter = pinyin.Converter()

    name = None
    sheet = None
    head_row_num = None
    head_col_from = None

    def __init__(self, workbook) :
        self.sheet = workbook.sheet_by_name(self.name)

    def pinyin(self, txt) :
        pinyin = self.pinyin_converter.convert(unicode(txt), fmt='df', sc=False)
        return self.allstrip(pinyin)


    def allstrip(self, txt) :
        return re.sub(r"\s+", "", txt.strip().replace(' ',''), flags=re.UNICODE)

