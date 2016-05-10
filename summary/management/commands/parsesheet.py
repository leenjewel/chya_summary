from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.conf import settings
import md5
import os
import datetime
from django.db import IntegrityError
from django.db import transaction
from summary.models import ParseTask
import xlrd
from summary.sheets.profitsheet import ProfitSheet

class Command(BaseCommand) :

    help = 'Parse Excel'

    def add_arguments(self, parser) :
        parser.add_argument('--year', default = datetime.date.today().year)

    def handle(self, *args, **kwargs) :
        workbook_path = os.path.join(settings.MEDIA_ROOT, 'workbook')
        if os.path.exists(workbook_path) :
            for root, dirs, files in os.walk(workbook_path) :
                for workbook_file in files :
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
        try :
            ParseTask.objects.get(hashid = task.hashid, isparseing = True)
        except ParseTask.DoesNotExist, e :
            sid = transaction.savepoint()
            try :
                task.isparseing = True
                task.hasparsed = False
                task.save()
                transaction.savepoint_commit(sid)
                workbook = xlrd.open_workbook(workbook_path)
                profit_sheet = ProfitSheet(workbook)
                profits = profit_sheet.parse(task)
                for profit in profits :
                    profit.save()

                task.isparseing = False
                task.hasparsed = True
                task.save()
            except IntegrityError :
                transaction.savepoint_rollback(sid)

