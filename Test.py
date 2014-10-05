import os, sys, inspect, thread, time, math
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class myListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	
	def on_init(self, controller):
		print "Initialized"
	def on_connect(self, controller):
		print "Connected"
	def on_disconnect(self, controller):
		print "Disconnected"

	def on_frame(self, controller):
		frame = controller.frame()
		print frame, 
		for hand in frame.hands:
			handType = "Left hand" if hand.is_left else "Right hand"
			palm = hand.palm_position

			for finger in hand.fingers:
				bone = finger.bone(3)
				distance = palm.distance_to(bone.next_joint)
				print "  %s finger at (%s)\n" % (self.finger_names[finger.type()], distance),


def main():
	listener = myListener()
	controller = Leap.Controller()

	controller.add_listener(listener)
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
    main()