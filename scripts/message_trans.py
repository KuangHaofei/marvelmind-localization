#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from marvelmind_nav.msg import hedge_pos


def callback(data):
    x = data.x_m
    y = data.y_m
    z = data.z_m

    pos = "x:%f;y:%f;z:%f" % (x, y, z)
    pub.publish(pos)


if __name__ == '__main__':
    rospy.init_node('message_trans', anonymous=True)

    pub = rospy.Publisher('track_pos', String, queue_size=1)
    rospy.Subscriber("/hedge_pos", hedge_pos, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
