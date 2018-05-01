#import os
from camelot.admin.action import Action
from camelot.core.utils import ugettext_lazy as _
from Terry.Converters.Prisma import Converter
from camelot.core.orm import Session
from camelot.view.action_steps import ( FlushSession )
from camelot.view.action_steps.select_file import SelectDirectory
#from PyQt4.QtCore import QSettings,  QString

class PAPDataImporter( Action ):
    verbose_name = _('Import PAP device data')

    def model_run( self, model_context ):
        device=model_context.get_object()
        select_import_folder = SelectDirectory()
        if not (device.ImportPath is None):
            select_import_folder.directory = device.ImportPath
      
        path= yield select_import_folder
        device.ImportPath=path
        session = Session()
        converter=Converter.Converter()
        converter.Convert(model_context)
        yield FlushSession(session)
