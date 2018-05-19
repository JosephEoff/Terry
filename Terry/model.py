from sqlalchemy import Unicode,  Integer,  Date,  DateTime,  Float
from sqlalchemy.schema import Column
from camelot.view import forms

from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
    
from camelot.admin.entity_admin import EntityAdmin
from camelot.admin.validator.entity_validator import EntityValidator
from camelot.core.orm import Entity,   ManyToOne,  OneToMany,  OneToOne,  ManyToMany,  belongs_to,  has_many,  has_one,    has_and_belongs_to_many
from Terry.DataImport import PAPDataImporter

class Profile( Entity ):
    __tablename__ = 'profile'
    LastName = Column( Unicode(60), nullable = False )
    FirstName = Column( Unicode(60), nullable = False )
    DateOfBirth = Column(Date)
    Devices=OneToMany('OwnedDevice')
    
    def __unicode__(self):
        return self.Name
    
    class Admin( EntityAdmin ):
        verbose_name = 'Profile'
        list_display = ['LastName', 'FirstName',   'DateOfBirth']
        form_display = forms.TabForm([('Profile', forms.Form(['LastName', 'FirstName','DateOfBirth','Devices',]))])

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
    Pressure=Column(Float)
    Strength=Column(Float)
    
    class Admin(EntityAdmin):
        verbose_name = 'Physio Event'
        list_display = ['Device','Event', 'Start', 'End', 'Pressure', 'Strength']
        validator=PhysioEventValidator

class ImportedDataSets(Entity):
    __tablename__= 'importeddatasets'
    belongs_to('Device', of_kind='OwnedDevice')
    DataSetID=Column(Unicode(400))
    
    def __unicode__(self):
        return  self.DataSetID
    
    class Admin(EntityAdmin):
        verbose_name = 'Imported Dataset'
        list_display = ['Device', 'DataSetID']
    
class OwnedDevice(Entity):
    __tablename__='owneddevice'
    SerialNumber = Column(Unicode(60),  nullable = False,  unique = True)
    Owner=ManyToOne('Profile')
    model_id = Column( Integer, ForeignKey('devicetypes.id') )
    Modelname = relationship( 'DeviceModel',  backref = 'owneddevice' )
    ImportPath =Column(Unicode(400))
    has_many('ImportedDataSetIDs', of_kind='ImportedDataSets')
    
    def __unicode__(self):
        return  self.SerialNumber
    
    class Admin( EntityAdmin ):
        verbose_name = 'Devices'
        list_display = ['SerialNumber',  'Modelname', 'ImportPath',   'ImportedDataSetIDs'] 
        form_actions = [PAPDataImporter()]

class DeviceModel(Entity):
    __tablename__ = 'devicetypes'
    ModelName = Column( Unicode(60), nullable = False )
    belongs_to('Type', of_kind='ModelType')
    
    def __unicode__(self):
        return self.ModelName or 'None'
    
    class Admin( EntityAdmin ):
        verbose_name = 'PAP Model'
        list_display = ['ModelName']

class ModelType(Entity):
    __tablename__ = 'modeltypes'
    Type = Column( Unicode(60), nullable = False )
    has_many('DeviceModels', of_kind='DeviceModel')
    has_many('Events',  of_kind='EventTypes')
    
    def __unicode__(self):
        return self.ModelName or 'None'
    
    class Admin( EntityAdmin ):
        verbose_name = 'Model Type'
        list_display = ['Type', 'DeviceModels',  'Events']
        
class EventTypes(Entity):
    __tablename__ = 'eventtypes'
    TypeID = Column( Unicode(60), nullable = False )
    Name = Column(Unicode(60), nullable=False)
    Description = Column(Unicode(300), nullable=True)    
    belongs_to('ModelType', of_kind='ModelType')
    
    def __unicode__(self):
        return self.ModelName or 'None'
    
    class Admin( EntityAdmin ):
        verbose_name = 'Event Type'
        list_display = ['TypeID', 'Name',  'Description']
    
