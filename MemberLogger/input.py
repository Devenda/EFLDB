import evdev
from evdev import InputDevice, categorize, ecodes
import database

class input(object):

    memberIDList = list()
    prevEvent = str()
    numbers = {"11":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7,"9":8,"10":9}

    db = database.database()

    def __init__(self,device):
        self.device = evdev.InputDevice(device)
        print("Listening on device: " + str(device))
    
    def listDevices(self):
        self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in self.devices:
            print(self.device.fn, self.device.name, self.device.phys)

    def getActiveKeys(self):
        print(self.device.active_keys(verbose=True))
        
    def keyboardEvent(self,event):
        # if event key is number
        if  event.value == 1 and str(event.code) in self.numbers and (self.prevEvent in self.numbers or not self.prevEvent):
            self.memberIDList.append(self.numbers[str(event.code)])
            #print("Known key: ",str(event.code))
        elif event.value == 1 and str(event.code) == "28" and len(self.memberIDList) == 10:
            memberId = ''.join(str(idInt) for idInt in self.memberIDList)
            
            # write scan to db
            self.db.writePresence(''.join(str(idInt) for idInt in self.memberIDList))
            print("Processed memberId")
            
            self.memberIDList.clear()
            self.prevEvent = str()
        elif event.value == 1 and str(event.code) == "28":
            self.memberIDList.clear()
        elif event.value == 0:
            pass
        else:            
            print("Unknow key: "+ str(event.code))

    def listenForInput(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                self.keyboardEvent(event)
                #print("code: ", event.code, " name: ", ecodes.KEY[event.code], event.value)
                #print(categorize(event))

    def keys(self):
        for k in range(0, 12):
            print("k: " + str(k) + "name " + str(ecodes.KEY[k]) )  
