import os
from camelot.admin.action import Action
from camelot.core.utils import ugettext_lazy as _
from Terry.Converters.Prisma import Converter
from camelot.core.orm import Session
from camelot.view.action_steps import ( FlushSession )
from camelot.view.action_steps.select_file import SelectFile
from PyQt4.QtCore import QSettings,  QString

class PAPDataImporter( Action ):
    verbose_name = _('Import PAP device data')

    def model_run( self, model_context ):
        device=model_context.get_object()
        settings=QSettings ();
        #need to get file filter from device type (model context-> device definition)
        filter='Prisma Statistics File (*.psstat)'
        #squinky hack.  cannot set the directory directly for the file selector, but it does read the settings 
        #so, overwrite the settings with the appropiate directory 
        if not (device.ImportPath is None):
            settings.setValue('datasource', device.ImportPath)   
            settings.sync()       

        select_import_folder = SelectFile()
        print filter
        select_import_folder.file_name_filter= filter
        select_import_folder.single = True
        files= yield select_import_folder
        if len(files)>0:
            path=os.path.dirname(files[0])
        device.ImportPath=path
        session = Session()
        converter=Converter.Converter()
        converter.Convert(model_context)
        yield FlushSession(session)
