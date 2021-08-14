
import pyrobotskinlib as rsl 
import time
import numpy as np
import cv2

S = rsl.RobotSkin("small_hexagon_001.json")
#u = rsl.SkinUpdaterFromFile(S,"../recorded_data/baxter_W2-recorded_data.txt")
u = rsl.SkinUpdaterFromShMem(S)

T = rsl.TactileMap(S,0)

TIB = rsl.TactileImageBuilder(T)

TIB.build_tactile_image()

u.start_robot_skin_updater()

rows = TIB.get_rows()
cols = TIB.get_cols()

while True:
    u.make_this_thread_wait_for_new_data()
    I = np.array(TIB.get_tactile_image(),np.uint8)
    I = I.reshape([rows,cols])
    cv2.imshow('Tactile Image',I)
    cv2.waitKey(1)
    #print(  str(u.get_timestamp_in_sec()) + " | " + str(S.taxels[0].get_taxel_response())+ " | " + str(S.taxels[1].get_taxel_response())+ " | " + str(S.taxels[2].get_taxel_response())+ " | " + str(S.taxels[3].get_taxel_response()) + " | " + str(S.taxels[4].get_taxel_response())+ " | " + str(S.taxels[5].get_taxel_response())+ " | " + str(S.taxels[6].get_taxel_response()))