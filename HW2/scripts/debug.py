import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def callback(data):
    print('I am debugger, x: %s, y: %s' % (data.pose.position.x, data.pose.position.y))

def listener():
    rospy.init_node('debug', anonymous=True)

    rospy.Subscriber('multi', PoseStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
