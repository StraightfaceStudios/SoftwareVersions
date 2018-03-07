###############################################################
## Imports
###############################################################
from System import *
from System.Diagnostics import *
from System.IO import *
from System.Text.RegularExpressions import *

from Deadline.Events import *
from Deadline.Scripting import *

import subprocess
import re
import xml.etree.ElementTree as ET

###############################################################
## Give Deadline an instance of this class so it can use it.
###############################################################
def GetDeadlineEventListener():
    return SoftwareVersionsListener()

def CleanupDeadlineEventListener( eventListener ):
    eventListener.Cleanup()
    
###############################################################
## The SoftwareVersions event listener class.
###############################################################
class SoftwareVersionsListener (DeadlineEventListener):
    def __init__( self ):

        self.OnSlaveStartingJobCallback += self.SlaveStartedJob
        self.OnSlaveStartedCallback += self.SlaveStarted
    
    def Cleanup( self ):
        del self.OnSlaveStartedCallback
        del self.OnSlaveStartingJobCallback
            
    def SlaveStartedJob(self, slaveName, job):

        eventType = self.GetConfigEntryWithDefault( "GetVersions", "On Slave Job Started" )
        self.GetVersions(slaveName)
            
    def SlaveStarted(self, slaveName):
        
        eventType = self.GetConfigEntryWithDefault( "GetVersions", "On Slave Started" )
        self.GetVersions(slaveName)
        
    def GetVersions(self, slaveName):
        ClientUtils.LogText( "Starting SoftwareVersion")
        try:
            ForestPack = subprocess.check_output('REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\Itoo Software\Forest Pack Pro" /v Installed',shell=True)
        except:
            ForestPack = ''
        try:
            RailClone = subprocess.check_output('REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\Itoo Software\RailClone Pro" /v Installed',shell=True)
        except:
            RailClone = ''
        try:
            Vray = subprocess.check_output('"C:\\Program Files\\Chaos Group\\V-Ray\\RT for 3ds Max 2018 for x64\\bin\\vray.exe" -version',shell=True)
        except:
            Vray= ''  
        try:
            log = 'C:\\Program Files\\Chaos Group\\Phoenix FD\\3ds Max 2018 for x64\\uninstall\\install.xml'
            e = ET.parse(log).getroot()
            MajorVersion = e.find('.//MajorVersion').text
            MinorVersion = e.find('.//MinorVersion').text
            MinestVersion = e.find('.//MinestVersion').text
            Phoenix = ( MajorVersion + "." + MinorVersion + "." + MinestVersion ) 

        except:
            Phoenix = ''  
        ForestPack = re.search("(\d*\.\d*\.\d*)", ForestPack )
        RailClone = re.search("(\d*\.\d*\.\d*)", RailClone )
        Vray = re.search("(\d*\.\d*\.\d*)", Vray )
        if ForestPack:
            ClientUtils.LogText( "ForestPack" )
            slaveSettings = RepositoryUtils.GetSlaveSettings( slaveName, True )
            slaveSettings.SlaveExtraInfo9 = ForestPack.group()
            RepositoryUtils.SaveSlaveSettings( slaveSettings )
        if RailClone:
            ClientUtils.LogText( "RailClone" )
            slaveSettings = RepositoryUtils.GetSlaveSettings( slaveName, True )
            slaveSettings.SlaveExtraInfo7 = RailClone.group()
            RepositoryUtils.SaveSlaveSettings( slaveSettings )
        if Vray:
            ClientUtils.LogText( "Vray" )
            slaveSettings = RepositoryUtils.GetSlaveSettings( slaveName, True )
            slaveSettings.SlaveExtraInfo8 = Vray.group()
            RepositoryUtils.SaveSlaveSettings( slaveSettings )
        if Phoenix:
            ClientUtils.LogText( "Phoenix" )
            slaveSettings = RepositoryUtils.GetSlaveSettings( slaveName, True )
            slaveSettings.SlaveExtraInfo6 = Phoenix
            RepositoryUtils.SaveSlaveSettings( slaveSettings )
        