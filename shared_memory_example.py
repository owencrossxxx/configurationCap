
import pyrobotskinlib as rsl 
import time

S = rsl.RobotSkin("small_hexagon_001.json")
u = rsl.SkinUpdaterFromShMem(S)
u.start_robot_skin_updater()

while True:
    u.make_this_thread_wait_for_new_data()
    resp = S.get_taxel_responses()
    uids = S.get_taxel_ids()
    print(  str(u.get_timestamp_in_sec()) + " | " + str(uids[0]) + " | " + str(resp[0]) )
