import os
from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section
from camelot.core.utils import ugettext_lazy as _

from Terry.model import PhysioEvent,  Profile,  DeviceModel,  ImportedDataSets

class TerryAdmin(ApplicationAdmin):
  
    name = 'Terry'
    application_url = ''
    help_url = ''
    author = 'Joseph Eoff'
    domain = 'molear.de'
    
    def get_sections(self):
        from camelot.model.memento import Memento
        from camelot.model.i18n import Translation
        #handiconpath=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hands.png')
        return [ Section( _('Terry'),
                          self,
                          Icon('tango/22x22/apps/system-users.png'),
                          items = [Profile] ),
                    Section( _('Data'),
                          self,
                          Icon('tango/22x22/apps/system-users.png'),
                          items = [PhysioEvent] ),
                Section( _('Maintenance'),
                          self,
                          Icon('tango/22x22/apps/system-users.png'),
                          items = [DeviceModel,  ImportedDataSets] ),
                 Section( _('Configuration'),
                          self,
                          Icon('tango/22x22/categories/preferences-system.png'),
                          items = [Memento, Translation] )
                ]
    
