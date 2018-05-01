import Terry.model
from datetime import datetime
import re
import lxml.etree as ET
from camelot.view.action_steps import (UpdateProgress ,  MessageBox)
import glob2
import os

class PrismaXMLTarget(object):
    startTime=None
    serialnumber=''
    
    def __init__(self, ModelContext):
        self.modelcontext=ModelContext
    
    def start(self, tag, attrib):
        if (not ('RespEventID' in attrib)):
            return
        
        pressure=float(attrib['Pressure'])/100
        strength=float(attrib['Strength'])
        endtimestamp=float(attrib['EndTime'])/10
        starttimestamp=endtimestamp-float(attrib['Duration'])/10
        startdatetime=datetime.utcfromtimestamp(self.startTime+starttimestamp)
        enddatetime=datetime.utcfromtimestamp(self.startTime+endtimestamp)
        event=Terry.model.PhysioEvent()
        #link to the device
        event.Device=self.modelcontext.get_object()
        event.Start=startdatetime
        event.End=enddatetime
        event.Strength=strength
        event.Pressure=pressure
        event.Event=attrib['RespEventID']
        
    def end(self, tag):
        pass
    def data(self, data):
         pass
    def close(self):
        pass
    def comment(self,text):
        if not (self.startTime is None):
            #already defined
            return
        dateitems=re.split(' +', text.strip())
        if (len(dateitems)!=2):
            #wrong format
            return
        if (dateitems[0]!='started'):
            #wrong content
            return
        #Date and time in the events file are off by 12 hours.  Add 12 hours worth of seconds.
        self.startTime=float(dateitems[1])+43200
        
class Converter(object):
    def Convert(self,  ModelContext):
        device=ModelContext.get_object()
        path=device.ImportPath
        path=os.path.join(path, device.SerialNumber)
    
        filter='Prisma Statistics File (*.psstat)'
        
        datasetstoimport=self.GetDataSetsToImport(device, path)
       
        if len(datasetstoimport)==0:
            return
   
        for datasetname in datasetstoimport: 
            try:
                datasetpath=os.path.join(path, datasetname )
                self.ImportEvents(datasetpath,  ModelContext)
                datasetobject=Terry.model.ImportedDataSets()
                datasetobject.Device=ModelContext.get_object()
                datasetobject.DataSetID=datasetname
            except:
                #Really ought to do something here.
                pass
        
    def ImportEvents(self,  DatasetPath,  ModelContext):
        files=self.GetAllEventFiles(DatasetPath)
        for file in files: 
            print file
            parser = ET.XMLParser(recover=True,  target = PrismaXMLTarget(ModelContext))
            ET.parse(file,parser)
        
    def GetAllEventFiles(self, Path):
        files= glob2.glob(os.path.join(Path, '**', 'event*.xml'))
        return files
        
    def GetDataSetsToImport(self, Device,  Path):
        existingdatasets=Device.ImportedDataSetIDs
        existingdatasetIDs=[]
        for row in existingdatasets:
            existingdatasetIDs.append(row.DataSetID)
        datasetsavailable=self.GetAllAvailableDatasets(Path)
        datasetstoimport=[x for x in datasetsavailable if x not in existingdatasetIDs]
        return datasetstoimport
        
    def GetDataSetNameFromFilename(self,  filename):
        path=os.path.dirname(filename)
        path=os.path.normpath(path)
        datasetname=os.path.basename(path)
        return datasetname
        
    def GetAllAvailableDatasets(self, Path):
        files=self.GetAllEventFiles(Path)
        availabledatasets=[]
        for file in files:
            datasetname=self.GetDataSetNameFromFilename(file)
            if not datasetname in availabledatasets:
                availabledatasets.append(datasetname)
        return availabledatasets
        
