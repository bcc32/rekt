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
		for hand in frame.hands:
			handType = "Left hand" if hand.is_left else "Right hand"
			palm = hand.palm_position

			letter = [0] * 5
			for finger in hand.fingers:
				bone = finger.bone(3)
				distance = palm.distance_to(bone.next_joint)
				"""print "  %s finger at (%s)\n" % (self.finger_names[finger.type()], distance),"""
				if distance > 68: #MAGIC FUCKING NUMBER
					letter[finger.type()] = 1

			if letter == [1,0,0,0,0]:
				print 'A'
			if letter == [1,1,1,1,1]:
				print findBC(hand)
			if letter == [0,1,0,0,0]:
				print findDX(hand)
			if letter == [0,0,1,1,1]:
				print 'F'
			if letter == [0,1,1,1,0]:
				print 'W'
			if letter == [1,0,0,0,1]:
				print 'Y'
			if letter == [0,1,1,0,0]:
				print findUVRHKP(hand)
			if letter == [0,0,0,0,1]:
				print findIJ(hand)
			if letter == [1,1,0,0,0]:
				print findGLZQ(hand)
			if letter == [0,0,0,0,0]:
				print findTMN(hand)

def findBC(hand):
	myList = []
	for finger in hand.fingers:
		myList.append(finger)

	sum = 0
	for i in range(len(myList)-1):
		length = (myList[i].bone(3).next_joint-myList[i+1].bone(3).next_joint).magnitude
		sum += length

	if sum/5 > 30:
		return 'B'
	if sum/5 > 22:
		return 'C'

def findTMN(hand):
	index = 0
	middle = 0
	ring = 0
	pinky = 0
	for finger in hand.fingers:
		if finger.type() == 1:
			index = finger
		if finger.type() == 2:
			middle = finger
		if finger.type() == 3:
			ring = finger
		if finger.type() == 4:
			pinky = finger
	angle = math.acos(index.bone(1).next_joint.dot(middle.bone(1).next_joint)/(index.bone(1).next_joint.magnitude*middle.bone(1).next_joint.magnitude))/math.pi*180
	angle2 = math.acos(middle.bone(1).next_joint.dot(ring.bone(1).next_joint)/(middle.bone(1).next_joint.magnitude*ring.bone(1).next_joint.magnitude))/math.pi*180
	angle3 = math.acos(ring.bone(1).next_joint.dot(pinky.bone(1).next_joint)/(ring.bone(1).next_joint.magnitude*pinky.bone(1).next_joint.magnitude))/math.pi*180

	if angle > 11:
		return 'T'
	elif angle2 > 9:
		return 'N'
	elif angle3 > 8:
		return 'M'
	else:
		return ''


def findUVRHKP(hand):
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

	if angle > 40 and hand.palm_normal.y < 0:
		return 'P'
	elif angle > 40:
		return 'K'
	elif angle > 20 and hand.palm_normal.y < 0:
		return 'V'
	elif angle > 7.5 and hand.palm_normal.y < 0:
		return 'U'
	elif angle < 7.5 and hand.palm_normal.y < 0:
		return 'R'
	elif hand.palm_normal.y > 0:
		return 'H'
	else:
		return ''

def findIJ(hand):
	if hand.palm_normal.y > 0:
		return 'J'
	else:
		return 'I'

def findGLZQ(hand):
	finger1 = 0
	finger2 = 0
	for finger in hand.fingers:
		if finger.type() == 1:
			finger1 = finger
		elif finger.type() == 2:
			finger2 = finger

	length = (finger1.bone(3).prev_joint - finger2.bone(3).prev_joint).magnitude

	if length > 70:
		return 'L'
	if length > 60:
		return 'Z'
	if length > 45:
		return 'G'
	if length < 45:
		return 'Q'
	else:
		return ''

def findDX(hand):
	finger1 = 0
	for finger in hand.fingers:
		if finger.type() == 1:
			finger1 = finger
	bone1 = finger1.bone(1).direction
	bone2 = finger1.bone(2).direction
	angle = math.acos(bone1.dot(bone2)/(bone1.magnitude*bone2.magnitude))/math.pi*180
	if angle > 30:
		return 'X'
	else:
		return 'D'

def main():
	listener = myListener()
	controller = Leap.Controller()
	controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
	controller.add_listener(listener)

	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
    main()