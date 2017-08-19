#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint

import math

'''
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
'''

LOOKAHEAD_WPS = 200 # Number of waypoints we will publish. You can change this number


class WaypointUpdater(object):
    def __init__(self):
        rospy.init_node('waypoint_updater')

        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)

        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below


        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)

        # TODO: Add other member variables you need below 

        # current path
        # NOTE: supposedly comes from top level planner (from file for simulator) at rate 40
        current_waypoints = None

        # current pose     
        # NOTE: supposedly comes from fusion (briged from simulator) at unknown rate   
        current_pose = None

        rospy.spin()

    def euclidean_distance(self, position1, position2):
        a = position1
        b = position2
        return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)

    def get_closest_waypoint(self):
        min_dist = 100000
        min_ind = 0
        ind = 0
        position1 = self.current_pose.pose.position
        for wp in self.current_waypoints:
            position2 = wp.pose.pose.position 
            dist = self.euclidean_distance(position1, position2)
            if dist < min_dist:
                min_dist = dist
                min_ind = ind
            ind += 1
        return min_ind
#1131
#1183
    # publish final_waypoints 
    def publish(self):
        if (not rospy.is_shutdown() \
            and (self.current_pose is not None) \
            and (self.current_waypoints is not None)):
                closest_waypoint_ahead_index = self.get_closest_waypoint()
                lane = Lane()
                lane.header.frame_id = '/world'
                lane.header.stamp = rospy.Time(0)
                lane.waypoints = self.current_waypoints[closest_waypoint_ahead_index:closest_waypoint_ahead_index+LOOKAHEAD_WPS]
                self.final_waypoints_pub.publish(lane)
        pass

    def pose_cb(self, msg):
        # TODO: Implement
        self.current_pose = msg
        # will publish on each pose update for now 
        self.publish()
        pass

    def waypoints_cb(self, waypoints):
        # TODO: Implement
        self.current_waypoints = waypoints.waypoints;
        pass

    def traffic_cb(self, msg):
        # TODO: Callback for /traffic_waypoint message. Implement
        pass

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist


if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
