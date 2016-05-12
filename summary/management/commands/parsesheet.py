from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.conf import settings
import md5
import os
import datetime
from django.db import transaction
from django.db import IntegrityError
from django.db import DatabaseError
from summary.models import ParseTask
import xlrd

from summary.sheets.profitsheet import ProfitSheet
from summary.sheets.costsheet import CostSheet
from summary.sheets.salessheet import SalesSheet
from summary.sheets.managementcostsheet import ManagementCostSheet
from summary.sheets.financialexpensessheet import FinancialExpensesSheet
from summary.sheets.taxespayablesheet import TaxesPayableSheet
from summary.sheets.taxespaidsheet import TaxesPaidSheet
from summary.sheets.laborcostsheet import LaborCostSheet
from summary.sheets.depreciationsheet import DepreciationSheet

class Command(BaseCommand) :

    help = 'Parse Excel'

    def add_arguments(self, parser) :
        parser.add_argument('--year', default = datetime.date.today().year)

    def handle(self, *args, **kwargs) :
        workbook_path = os.path.join(settings.MEDIA_ROOT, 'workbook')
        if os.path.exists(workbook_path) :
            for root, dirs, files in os.walk(workbook_path) :
                for workbook_file in files :
                    if not workbook_file[workbook_file.rindex('.')+1:].startswith('xls') :
                        continue
                    workbook_path = os.path.join(root, workbook_file)
                    with open(workbook_path) as workbook_fp :
                        hashobj = md5.new()
                        hashobj.update(workbook_fp.read())
                        hashid = hashobj.hexdigest()
                        task = None
                        try :
                            task = ParseTask.objects.get(hashid = hashid)
                        except ParseTask.DoesNotExist, e :
                            task = ParseTask()
                            task.year = kwargs['year']
                            task.hashid = hashid
                            task.hasparsed = False
                            task.isparseing = False
                            task.filename = workbook_file
                            task.save()
                        workbook_fp.close()
                        self.doTask(task, workbook_path)


    def doTask(self, task, workbook_path) :
        with transaction.atomic() :
            try :
                ParseTask.objects.select_for_update().get(hashid = task.hashid, isparseing = True)
            except ParseTask.DoesNotExist, e :
                task.isparseing = True
                task.hasparsed = False
                task.save()
                workbook = xlrd.open_workbook(workbook_path)

                profit_sheet = ProfitSheet(workbook).parse(task)
                cost_sheet = CostSheet(workbook).parse(task)
                SalesSheet(workbook).parse(task)
                ManagementCostSheet(workbook).parse(task)
                FinancialExpensesSheet(workbook).parse(task)
                TaxesPayableSheet(workbook).parse(task)
                TaxesPaidSheet(workbook).parse(task)
                LaborCostSheet(workbook).parse(task)
                DepreciationSheet(workbook).parse(task)

            except DatabaseError, e:
                print "DatabaseError",e
            finally :
                task.isparseing = False
                task.hasparsed = True
                task.save()

