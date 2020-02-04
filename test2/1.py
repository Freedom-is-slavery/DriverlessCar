import os

classes = ['police_go_straight', 'police_turn_left', 'police_turn_right', 'police_slow_down', 'police_stop',
           'go_straight', 'turn_left', 'turn_right', 'stop',
           'forbid_whistle', 'speed_limit40', 'turn_left_and_right',
           'forbid_straight', 'forbid_turn_right', 'forbid_turn_left',
           'speed_limit50', 'forbid_in', 'stop_check']
for dir in classes:
    path = '/home/pi/Pictures/capture/' + dir
    os.makedirs(path)