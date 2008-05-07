
"""The DeviceManager class is responsible for holding a list of
  devices which can translate events such as a MouseHandler and
  KeyboardHandler for translation of mouse and keyboard events,
  respectively.

  Custom device handlers can be registered with this class for more
  functionality
"""

from PyQt4.QtCore import QEvent
from PyQt4.QtGui import QMouseEvent
from pivy.coin import SoLocation2Event
from pivy.coin import SbVec2f

#from pivy.quarter import DeviceHandler
#from pivy.quarter.QuarterWidget import QuarterWidget


#class DeviceManagerP {
#public:
#  QList<DeviceHandler *> devices;
#  QuarterWidget * quarterwidget;
#  SbVec2s lastmousepos;
#  QPoint globalpos;
#};

class DeviceManager:
    def __init__(self, quarterwidget):
        assert(quarterwidget)

        # NOTE jkg: equalient to DeviceManagerP
        self.devices = []
        self.quarterwidget = quarterwidget
        self.lastmousepos = SbVec2f(0, 0)

    def translateEvent(self, qevent):
        """Runs trough the list of registered devices to translate event"""
        print "hmm2"
        if qevent.type() == QEvent.MouseMove:
            self.globalpos = qevent.globalPos()
            print self.globalpos

        print "devices:", self.devices
        for device in self.devices:
            soevent = device.translateEvent(qevent)
            if soevent:
              # cache mouse position so other devices can access it
              if (soevent.getTypeId() == SoLocation2Event.getClassTypeId()):
                self.lastmousepos = soevent.getPosition()
              return soevent

        #raise Exception("hey")
        return None

    def getWidget(self):
        """Returns the QuarterWidget this devicemanager belongs to"""
        return self.quarterwidget

    def getLastGlobalPosition(self):
        """Returns the last mouse position in global coordinates"""
        return self.globalpos

    def getLastMousePosition(self):
        """Returns the last mouse position"""
        return self.lastmousepos;

    def registerDevice(self, device):
        """ Register a device for event translation"""
        if not device in self.devices:
            device.setManager(self)
            self.devices.append(device)

    def unregisterDevice(self, device):
        """unregister a device"""
        print "FIXME jkg: unregisterdevice not completely tested/ported"
        if device in self.devices:
            self.devices.removeAt(self.devices.indexOf(device))
        else:
            # FIXME jkg: give warning (not in original quarter)
            pass