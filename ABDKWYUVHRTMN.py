import os, sys, inspect, thread, time, math

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

"""
	Please Note:
	All magic numbers in this file are based off measurements 
	from Loc's hands. 
"""

controller = Leap.Controller()

def read_letter(frame_count=5):
	read = lambda : digest_frames(read_letter0(frame_count))
	letter = digest_frames(read_letter0(frame_count))
	while letter == None:
		letter = read()
	return letter

def digest_frames(frames):
	counts = map(lambda x: (frames.count(x), x), frames)
	countmap = {}
	for (count, x) in counts:
		if not count in countmap:
			countmap[count] = [x]
		elif not x in countmap[count]:
			countmap[count] += [x]
	mode = countmap[max(counts)[0]]
	if len(mode) != 1 or mode[0] == None or mode[0] == '':
		return None
	else:
		return mode[0]

def read_letter0(frame_count):
	frames = []
	lastID = -1
	while len(frames) < frame_count:
		frame = controller.frame()
		if frame.id != lastID:
			lastID = frame.id
			frames += map(hand2letter, frame.hands)
	return frames


def hand2letter(hand):
	handType = "Left hand" if hand.is_left else "Right hand"
	palm = hand.palm_position

	letter = map(lambda finger: 1 if palm.distance_to(finger.tip_position) > 70 else 0, hand.fingers)

	if letter == [1,0,0,0,0]:
		print 'A'
	elif letter == [1,1,1,1,1]:
		print 'B'
	elif letter == [0,1,0,0,0]:
		print findDX(hand)
	elif letter == [0,0,1,1,1]:
		print 'F'
	elif letter == [0,1,1,1,0]:
		print 'W'
	elif letter == [1,0,0,0,1]:
		print 'Y'
	elif letter == [0,1,1,0,0]:
		print findUVRHKP(hand)
	elif letter == [0,0,0,0,1]:
		print findIJ(hand)
	elif letter == [1,1,0,0,0]:
		print findGLZQ(hand)
	elif letter == [0,0,0,0,0]:
		return findMNT(hand)		

def toDeg(rad):
	return rad/math.pi*180

def findUVRHKP(hand):
	finger1 = 0
	finger2 = 0
	for finger in hand.fingers:
		if finger.type() == 1:
			finger1 = finger
		elif finger.type() == 2:
			finger2 = finger

	dir1 = finger1.tip_position - hand.palm_position
	dir2 = finger2.tip_position - hand.palm_position
	angle = toDeg(dir1.angle_to(dir2))

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

	length = finger1.bone(3).prev_joint.distance_to(finger2.bone(3).prev_joint)

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
	angle = toDeg(bone1.angle_to(bone2))
	if angle > 30:
		return 'X'
	else:
		return 'D'

def findMNT(hand):
	finger1 = 0
	finger2 = 0
	finger3 = 0
	finger4 = 0
	for finger in hand.fingers:
		if finger.type() == 1:
			finger1 = finger
		elif finger.type() == 2:
			finger2 = finger
		elif finger.type() == 3:
			finger3 = finger
		elif finger.type() == 4:
			finger4 = finger

	bone1 = finger1.bone(1).direction
	bone2 = finger2.bone(1).direction
	bone3 = finger3.bone(1).direction
	bone4 = finger4.bone(1).direction

	if toDeg(bone1.angle_to(bone2)) > 7:
		return 'T'
	elif toDeg(bone2.angle_to(bone3)) > 5:
		return 'N'
	elif toDeg(bone3.angle_to(bone4)) > 4:
		return 'M'
	else:
		return ''

def main():
	controller = Leap.Controller()

	while True:
		time.sleep(0.5)
		print read_letter()

if __name__ == "__main__":
    main()