import pyxhook
import database

class input(object):

	memberIDList = list()
	prevEvent = str()
	numbers = {"agrave":0,"ampersand":1,"eacute":2,"quotedbl":3,"apostrophe":4,"parenleft":5,"section":6,"egrave":7,"exclam":8,"ccedilla":9}
	db = database.database()

	def keyboardEvent(self,event):
		wasThereAnEvent = False

		# if event key is number
		if event.Key in self.numbers and (self.prevEvent in self.numbers or not self.prevEvent):
			self.memberIDList.append(self.numbers[event.Key])
		elif event.Key == "Return" and len(self.memberIDList) == 10:
			print(str(self.memberIDList))
			# write scan to db
			self.db.writePresence(''.join(str(idInt) for idInt in self.memberIDList))
			self.memberIDList.clear()
		else:
			print(str(event.Key))

	def __init__(self):
		#Create hookmanager
		self.hookman = pyxhook.HookManager()
		#Define our callback to fire when a key is pressed down
		self.hookman.KeyDown = self.keyboardEvent
		#Hook the keyboard
		self.hookman.HookKeyboard()
		#Start our listener
		self.hookman.start()
