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

			letter = [0] * 5
			for finger in hand.fingers:
				bone = finger.bone(3)
				distance = palm.distance_to(bone.next_joint)
				print "  %s finger at (%s)\n" % (self.finger_names[finger.type()], distance),
				if distance > 70: #MAGIC FUCKING NUMBER
					letter[finger.type()] = 1

			if letter == [1,0,0,0,0]:
				print 'A'
			if letter == [1,1,1,1,1]:
				print 'B'
			if letter == [0,1,0,0,0]:
				print 'D'
			if letter == [0,0,1,1,1]:
				print 'K'
			if letter == [0,1,1,1,0]:
				print 'W'
			if letter == [1,0,0,0,1]:
				print 'Y'
			if letter == [0,1,1,0,0]:
				print findUVRH(hand)
			if letter == [0,0,0,0,0]:
				print findMNT(hand)

def findUVRH(hand):
	finger1 = 0
	finger2 = 0
	for finger in hand.fingers:
		if finger.type() == 1:
			finger1 = finger
		elif finger.type() == 2:
			finger2 = finger

	dir1 = finger1.bone(3).next_joint - hand.palm_position
	dir2 = finger2.bone(3).next_joint - hand.palm_position
	angle = math.acos(dir1.dot(dir2)/(dir1.magnitude*dir2.magnitude))
	angle = angle/math.pi*180

	if angle > 20 and hand.palm_normal.z < 0:
		return 'V'
	elif angle > 7.5 and hand.palm_normal.z < 0:
		return 'U'
	elif angle < 7.5 and hand.palm_normal.z < 0:
		return 'R'
	elif hand.palm_normal.z > 0:
		return 'H'
	else:
		return ''

def findMNT(hand):
	finger1 = 0
	finger2 = 0
	finger3 = 0
	finger4 = 0
	for finger in hand.fingers:
		if finger.type() == 1:
			finger1=finger
		elif finger.type() == 2:
			finger2=finger
		elif finger.type() == 3:
			finger3=finger
		elif finger.type() == 4:
			finger4=finger

	bone1 = finger1.bone(1).direction
	bone2 = finger2.bone(1).direction
	bone3 = finger3.bone(1).direction
	bone4 = finger4.bone(1).direction
	angle1 = math.acos(bone1.dot(bone2)/(bone1.magnitude*bone2.magnitude))/math.pi*180
	angle2 = math.acos(bone2.dot(bone3)/(bone2.magnitude*bone3.magnitude))/math.pi*180
	angle3 = math.acos(bone3.dot(bone4)/(bone3.magnitude*bone4.magnitude))/math.pi*180
	if angle1 > 6:
		return 'T'
	elif angle2 > 6:
		return 'N'
	elif angle3 > 5:
		return 'M'
	else:
		return ''


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