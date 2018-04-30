from sqlalchemy import Unicode,  Integer,  Date,  DateTime,  Float
from sqlalchemy.schema import Column
from camelot.view import forms

from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
    
from camelot.admin.entity_admin import EntityAdmin
from camelot.admin.validator.entity_validator import EntityValidator
from camelot.core.orm import Entity,   ManyToOne,  OneToMany,  OneToOne,  ManyToMany
from Terry.DataImport import PAPDataImporter

class Profile( Entity ):
    __tablename__ = 'profile'
    Name = Column( Unicode(60), nullable = False )
    Devices=OneToMany('OwnedDevice')
    DateOfBirth = Column(Date)
    
    def __unicode__(self):
        return self.Name
    
    class Admin( EntityAdmin ):
        verbose_name = 'Profile'
        list_display = ['Name',  'DateOfBirth']
        form_display = forms.TabForm([('Profile', forms.Form(['Name', 'DateOfBirth','Devices',]))])

class PhysioEventValidator(EntityValidator):
    def objectValidity(self, entity_instance):
        messages = super(PhysioEventValidator,self).objectValidity(entity_instance)
        if (entity_instance.Start >= entity_instance.End):
            messages.append("Negative time span in PhysioEvents not allowed.  End must be after start.")
        return messages

class PhysioEvent(Entity):
    __tablename__='physioevents'
    Device_id=Column(Integer, ForeignKey('owneddevice.id'))
    Device=relationship( 'OwnedDevice',  backref = 'physioevents' )
    Event=Column(Unicode(60), nullable = False)
    Start=Column(DateTime)
    End=Column(DateTime)
    Value=Column(Float)
    
    class Admin(EntityAdmin):
        verbose_name = 'Physio Event'
        list_display = ['Device','Event', 'Start', 'End', 'Value']
        validator=PhysioEventValidator

class ImportedDataSets(Entity):
    __tablename__= 'importeddatasets'
    Device_id=Column(Integer, ForeignKey('owneddevice.id'))
    Device=relationship( 'OwnedDevice',  backref = 'importeddatasets' )
    DataSetID=Column(Unicode(400))
    
class OwnedDevice(Entity):
    __tablename__='owneddevice'
    SerialNumber = Column(Unicode(60),  nullable = False,  unique = True)
    Owner=ManyToOne('Profile')
    model_id = Column( Integer, ForeignKey('devicetypes.id') )
    Modelname = relationship( 'DeviceModel',  backref = 'owneddevice' )
    ImportPath =Column(Unicode(400))
    
    def __unicode__(self):
        return  self.SerialNumber
    
    class Admin( EntityAdmin ):
        verbose_name = 'Devices'
        list_display = ['SerialNumber',  'Modelname', 'ImportPath'] 
        form_actions = [PAPDataImporter()]

class DeviceModel(Entity):
    __tablename__ = 'devicetypes'
    ModelName = Column( Unicode(60), nullable = False )
    
    def __unicode__(self):
        return self.ModelName or 'None'
    
    class Admin( EntityAdmin ):
        verbose_name = 'PAP Model'
        list_display = ['ModelName']
