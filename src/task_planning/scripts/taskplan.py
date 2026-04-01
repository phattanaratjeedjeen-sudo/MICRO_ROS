#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np

class StripsAction:
    def __init__(self, action, preconditions, add_list, delete_list):
        self.action = action
        self.preconditions = set(preconditions)
        self.add_list = set(add_list)
        self.delete_list = set(delete_list)
        self.complete = False
        
    def can_execute(self, current_state):
        self.complete = False
        return self.preconditions.issubset(current_state)
    
    def execute(self, current_state):
        print(f"Executing action: {self.action}")
        if not self.can_execute(current_state):
            print(f"Cannot execute '{self.action}' due to unmet preconditions.")
            return current_state, False

        new_state = (current_state - self.delete_list) | self.add_list
        print(f"Action '{self.action}' executed successfully")
        self.complete = True
        return new_state, self.complete


def reach(current_pos, target_pos):
    error = np.linalg.norm(np.array(current_pos) - np.array(target_pos))
    accept_error = 0.02
    if error < accept_error:
        return f"reached_{target_pos}"
    else:
        return f"moving_to_{target_pos}"

def hand(grip):
    if grip:
        return "holding"
    else:
        return "empty"

def see(object):
    if object:
        return "see"
    else:
        return "not_see"
    
def user_cmd(cmd):
    if cmd == 1:
        return "run"
    else:
        return "idle"

init_pos = np.array([0.0, 0.0, 0.0])
pick_pos = np.array([0.0, 0.0, 0.0])
putdown_pos = np.array([0.0, 0.0, 0.0])
home_pos = np.array([0.0, 0.0, 0.0])
search_pos = np.array([0.0, 0.0, 0.0])
range_pos = np.array([0.0, 0.0, 0.0])
retrieve_pos = np.array([0.0, 0.0, 0.0])

# actions
search = StripsAction(
    action="search",
    preconditions=[f"{reach(init_pos, target_pos=search_pos)}", 
         f"{hand(grip=False)}", 
         f"{see(object=True)}", 
         f"{user_cmd(cmd=1)}"],
    add_list=[f"{reach(init_pos, target_pos=pick_pos)}"],
    delete_list=[f"{reach(init_pos, target_pos=search_pos)}",]
)

pickup = StripsAction(
    action="pickup",
    preconditions=[f"{hand(grip=False)}",
         f"{see(object=True)}",
         f"{reach(init_pos, target_pos=pick_pos)}",
         f"{user_cmd(cmd=1)}"],
    add_list=[f"{hand(grip=True)}",],
    delete_list=[f"{hand(grip=False)}"]
)

putdown = StripsAction( 
    action="putdown",
    preconditions=[f"{hand(grip=True)}",
         f"{see(object=True)}", 
         f"{reach(init_pos, target_pos=putdown_pos)}",
         f"{user_cmd(cmd=1)}"],
    add_list=[f"{hand(grip=False)}",
         "cup_at_target"],
    delete_list=[f"{see(object=True)}",
            f"{hand(grip=True)}"]
)

move2search = StripsAction(
    action="move2search",
    preconditions=[f"{reach(init_pos, target_pos=home_pos)}", 
         f"{hand(grip=False)}", 
         f"{user_cmd(cmd = 1)}"],
    add_list=[f"{reach(init_pos, target_pos=search_pos)}",
         f"{see(object=True)}"],
    delete_list=[f"{reach(init_pos, target_pos=home_pos)}"]
)

move2putdown = StripsAction(
    action="move2putdown",
    preconditions=[f"{reach(init_pos, target_pos=pick_pos)}", 
         f"{hand(grip=True)}", 
         f"{user_cmd(cmd = 1)}",
         f"{see(object=True)}"],
    add_list=[f"{reach(init_pos, target_pos=putdown_pos)}"],
    delete_list=[f"{reach(init_pos, target_pos=pick_pos)}"]
)

move2retrieve = StripsAction(
    action="move2retrieve",
    preconditions=[f"{reach(init_pos, target_pos=putdown_pos)}", 
         f"{hand(grip=False)}", 
         f"{user_cmd(cmd = 1)}"],
    add_list=[f"{reach(init_pos, target_pos=retrieve_pos)}"],
    delete_list=[f"{reach(init_pos, target_pos=putdown_pos)}"]
)

move2home = StripsAction(
    action="move2home",
    preconditions=[f"{reach(init_pos, target_pos=retrieve_pos)}", 
         f"{hand(grip=False)}", 
         f"{user_cmd(cmd = 1)}"],
    add_list=[f"{reach(init_pos, target_pos=home_pos)}",
         f"{user_cmd(cmd = 0)}"],
    delete_list=[f"{reach(init_pos, target_pos=retrieve_pos)}",
            f"{user_cmd(cmd = 1)}"]
)

action_list = [move2search, search, pickup, move2putdown, putdown, move2retrieve, move2home]


class DummyNode(Node):
    def __init__(self):
        super().__init__('strips_commander')
        self.hz = 10.0

        self.init_pos = np.array([0.0, 0.0, 0.0])
        self.pick_pos = np.array([0.0, 0.0, 0.0])
        self.putdown_pos = np.array([0.0, 0.0, 0.0])
        self.home_pos = np.array([0.0, 0.0, 0.0])
        self.search_pos = np.array([0.0, 0.0, 0.0])
        self.range_pos = np.array([0.0, 0.0, 0.0])
        self.retrieve_pos = np.array([0.0, 0.0, 0.0])

        self.action_index = 0   
        
        # initial states
        self.states = {
            f"{reach(self.init_pos, self.home_pos)}",
            f"{hand(grip=False)}",
            f"{user_cmd(cmd=1)}"
        }
        
        self.create_timer(1.0 / self.hz, self.action_execution_callback)
        self.create_timer(1.0 / self.hz, self.action_publish_callback)
        self.create_subscription(String, 'user_command', self.user_command_callback, 10)
        self.state_publisher = self.create_publisher(String, 'current_state', 10)

    def action_execution_callback(self):
        self.states,complete = action_list[self.action_index].execute(self.states)
        if complete:
            self.action_index = (self.action_index + 1) % len(action_list)
            if self.action_index == len(action_list) - 1:
                print("\n[INFO] All actions executed. Looping back to the first action.")
    
    def action_publish_callback(self):
        msg = String()
        msg.data = action_list[self.action_index].action
        self.state_publisher.publish(msg)
        self.get_logger().info(f"{msg.data}")

    def user_command_callback(self, msg):
        pass
    


def main(args=None):
    rclpy.init(args=args)
    node = DummyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
