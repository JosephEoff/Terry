import Terry.model
from datetime import datetime
import re
import lxml.etree as ET
from camelot.view.action_steps import (UpdateProgress )
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
        endtimestamp=float(attrib['EndTime'])/10
        starttimestamp=endtimestamp-float(attrib['Duration'])/10
        startdatetime=datetime.utcfromtimestamp(self.startTime+starttimestamp)
        enddatetime=datetime.utcfromtimestamp(self.startTime+endtimestamp)
        event=Terry.model.PhysioEvent()
        #link to the device
        event.Device=self.modelcontext.get_object()
        event.Start=startdatetime
        event.End=enddatetime
        event.Value=pressure
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
        self.startTime=float(dateitems[1])+43200
        
class Converter(object):
    def Convert(self,  ModelContext):
        device=ModelContext.get_object()
        path=device.ImportPath
        path=os.path.join(path, device.SerialNumber)
        files=self.GetAllEventFiles(path)
#        parser = ET.XMLParser(target = PrismaXMLTarget(ModelContext))
#        ET.parse('/home/dev/snarch/0000481672/20180426/event_035.xml',parser)
        for file in files: 
            print file
            #Get dataset name, see if it is in the importeddatasets for this serialnumber
            #if it exists, do not import
            #else, add to imported datasets and import.
            parser = ET.XMLParser(recover=True,  target = PrismaXMLTarget(ModelContext))
            ET.parse(file,parser)
        
    def GetAllEventFiles(self, Path):
        files= glob2.glob(os.path.join(Path, '**', 'event*.xml'))
        return files
        
    def GetDataSetNameFromFilename(self,  filename):
        path=os.path.dirname(filename)
        path=os.path.normpath(path)
        datasetname=os.path.basename(path)
        return datasetname
