class input(object):

	memberIDList = list()
	prevEvent = str()
	numbers = {"agrave":0,"ampersand":1,"eacute":2,"quotedbl":3,"apostrophe":4,"parenleft":5,"section":6,"egrave":7,"exclam":8,"ccedilla":9}

	def __init__(self):
		#Create hookmanager
		hookman = pyxhook.HookManager()
		#Define our callback to fire when a key is pressed down
		hookman.KeyDown = keyboardEvent
		#Hook the keyboard
		hookman.HookKeyboard()
		#Start our listener
		hookman.start()

	def keyboardEvent(event):
		wasThereAnEvent = False
	
		# if event key is number
		if event.Key in numbers and (prevEvent in numbers or not prevEvent):
			memberIDList.append(numbers[event.key])
		elif event.Key == "Return":
			print("test");
		return True