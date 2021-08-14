import cv2
import numpy as np
import time
import threading

class Tracker:

  def __init__(self, gui=False, cam_index=2):
    # Open camera
    self.cam = cv2.VideoCapture(cam_index)
    # configure window if gui is required
    self.gui = gui
    self.cam_index = cam_index

    if self.gui:
      cv2.namedWindow("tracker", cv2.WINDOW_NORMAL)

      cv2.createTrackbar('dilation','tracker', 12, 20, self.emptyCallback)
      cv2.createTrackbar('erosion','tracker', 2, 20, self.emptyCallback)
      cv2.setMouseCallback("tracker", self.clickAndCrop)

    # Setup other data
    self.cropping_points = []
    self.is_cropping = False

    # Dict to store the blobs filters
    self.blob_filter = {}

    # mutex
    self.mutex = threading.Lock()

    # initial parameters
    self.dilation_size = 1
    self.erosion_size = 1

    # Launch main thread
    self.thread = threading.Thread(target=self.processCamera)

  def __del__(self):
    # Destroy camera
    self.cam.release()
    if self.gui:
      cv2.destroyAllWindows()
  
  def start(self):
    self.thread.start()

  def setCroppingPoints(self, tl_x, tl_y, br_x, br_y):
    """
    x1: top left x
    y1: top left y
    x2: bottom right x
    y2: bottom right y
    """
    self.cropping_points = []
    self.cropping_points.append((tl_x, tl_y))
    self.cropping_points.append((br_x, br_y))
  
  def setMorphologicalOperationParameters(self, dilation_size, erosion_size):
    self.dilation_size = dilation_size
    self.erosion_size = erosion_size
  
  def addColorBlob(self, name, r, g, b, r_min, r_max, g_min, g_max, b_min, b_max):
    if self.gui:
      cv2.createTrackbar(name + '_r_min','tracker', r_min, 255,   self.emptyCallback)
      cv2.createTrackbar(name + '_r_max','tracker', r_max, 255, self.emptyCallback)
      cv2.createTrackbar(name + '_g_min','tracker', g_min, 255,   self.emptyCallback)
      cv2.createTrackbar(name + '_g_max','tracker', g_max, 255, self.emptyCallback)
      cv2.createTrackbar(name + '_b_min','tracker', b_min, 255,   self.emptyCallback)
      cv2.createTrackbar(name + '_b_max','tracker', b_max, 255, self.emptyCallback)
    
    self.blob_filter[name] = {'r': r,
                              'g': g,
                              'b': b,
                              'r_min': r_min,
                              'r_max': r_max,
                              'g_min': g_min,
                              'g_max': g_max,
                              'b_min': b_min,
                              'b_max': b_max}
  
  def getDistance(self, name):
    try:
      d = self.blob_filter[name]['distance']
    except Exception:
      d = 0
    return d
  
  def getAngles(self, name1, name2):
    angles = []
    try:
      for p1 in self.blob_filter[name1]['points']:
        for p2 in self.blob_filter[name2]['points']:
          ang = self.computeAngle(origin=p1, end=p2)
          angles.append({'p1': p1, 'p2': p2, 'angle': ang})
    except Exception as e:
      print("Problem while computing angles: %s" %e)
    return angles

  def getPoints(self,name):
    return self.blob_filter[name]['points']
  
  def updateBlobFilterParameters(self, name):
    if self.gui:
      self.blob_filter[name]['r_min'] = cv2.getTrackbarPos(name + '_r_min','tracker')
      self.blob_filter[name]['r_max'] = cv2.getTrackbarPos(name + '_r_max','tracker')
      self.blob_filter[name]['g_min'] = cv2.getTrackbarPos(name + '_g_min','tracker')
      self.blob_filter[name]['g_max'] = cv2.getTrackbarPos(name + '_g_max','tracker')
      self.blob_filter[name]['b_min'] = cv2.getTrackbarPos(name + '_b_min','tracker')
      self.blob_filter[name]['b_max'] = cv2.getTrackbarPos(name + '_b_max','tracker')
    

  def emptyCallback(self, x):
    pass

  def clickAndCrop(self, event, x, y, flags, param):
    # grab references to the global variables
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
      self.cropping_points = [(x, y)]
      self.is_cropping = True
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
      # record the ending (x, y) coordinates and indicate that
      # the cropping operation is finished
      self.cropping_points.append((x, y))
      self.is_cropping = False

  # Applies a color filter
  def applyBlobFilter(self, image_bgr, filter, dilation_size, erosion_size):
    # compute limits
    bgr_lower_limit = (self.blob_filter[filter]['b_min'], self.blob_filter[filter]['g_min'], self.blob_filter[filter]['r_min'])
    bgr_upper_limit = (self.blob_filter[filter]['b_max'], self.blob_filter[filter]['g_max'], self.blob_filter[filter]['r_max'])

    # Capture mouse mask (to select a rectangle)
    bgr_frame_cropped = image_bgr
    if len(self.cropping_points) == 2:
      cv2.rectangle(self.frame, self.cropping_points[0], self.cropping_points[1], (0, 255, 0), 2)
      bgr_frame_cropped = np.zeros(image_bgr.shape, np.uint8)
      bgr_frame_cropped[self.cropping_points[0][1]:self.cropping_points[1][1], self.cropping_points[0][0]:self.cropping_points[1][0]] = image_bgr[self.cropping_points[0][1]:self.cropping_points[1][1], self.cropping_points[0][0]:self.cropping_points[1][0]]

    # Apply threshold to get mask
    mask = cv2.inRange(bgr_frame_cropped, bgr_lower_limit, bgr_upper_limit)

    # Apply erosion
    erosion_type = cv2.MORPH_ELLIPSE
    element = cv2.getStructuringElement(erosion_type, (2*self.erosion_size + 1, 2*self.erosion_size+1), (self.erosion_size, self.erosion_size))
    mask = cv2.erode(mask, element)
      
    # Apply dilation
    dilatation_type = cv2.MORPH_ELLIPSE
    element = cv2.getStructuringElement(dilatation_type, (2*self.dilation_size + 1, 2*self.dilation_size+1), (self.dilation_size, self.dilation_size))
    mask = cv2.dilate(mask, element)
      
    # Find the centers for filter 1
    points = []
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
      M = cv2.moments(c) # calculate moments for each contour
      try:
        cX = int(M["m10"] / M["m00"]) #  calculate x,y coordinate of center
        cY = int(M["m01"] / M["m00"])
        #cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        #label = "(%.2f, %.2f)" % (cX, cY)
        points.append(np.array([cX, cY]))
      except Exception:
        continue
        
    return mask, points

  def computeDistance(self, mask_bgr, points):
    # Recover the distance between the blobs
    points_pair = {}
    for i in range(len(points)):
      for j in range(i+1, len(points)):
        p1 = points[i]
        p2 = points[j]
        # COmpute mid point
        p_mid = 0.5*(p1+p2)
        # Compute distance
        dist = np.linalg.norm(p1-p2)
        points_pair[i] = {"p1": p1, "p2": p2, "distance": dist }
        dist_str = "d=%.2f" % dist
        cv2.line(mask_bgr, (p1[0], p1[1]), (p2[0], p2[1]), (100, 100, 100), 1)
        cv2.putText(mask_bgr, dist_str, (int(p_mid[0]), int(p_mid[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
      
    distance = 0.0
    #print(points_pair)
    if(len(points_pair) == 1):
      distance = points_pair[0]["distance"]
    #print(distance)
      
    return mask_bgr, distance

  def computeAngle(self, origin, end):
    #print("origin", origin)
    #print("end", end)
    po = origin
    pe = end
    #print("po", po)
    #("pe", pe)
    
    dx = pe[0] - po[0]
    dy = pe[1] - po[1]
    #print(dx)
    #print(dy)
    angle = np.arctan2(-dy, dx) *180.0 / np.pi # so y points upwards, and x to the right
    #print("angle", angle)
    
    # draw line
    angle_str = "angle=%.2f" % angle
    p_mid = 0.5*(po + pe)
    #print(p_mid)
    if self.gui:
      cv2.line(self.frame, (po[0], po[1]), (pe[0], pe[1]), (0, 255, 0), 1)
      cv2.putText(self.frame, angle_str, (int(p_mid[0]), int(p_mid[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    return angle

  def processCamera(self,name):
    start = time.time()
    self.ret, self.frame = self.cam.read()
    if not self.ret:
      print("failed to grab frame")

    self.frame = cv2.medianBlur(self.frame, 5)

    # recover value for dilation and erosion if using gui
    if self.gui:
      self.dilation_size = cv2.getTrackbarPos('dilation','tracker')
      self.erosion_size = cv2.getTrackbarPos('erosion','tracker')
    
    # get current positions of four trackbars
    for bf in list(self.blob_filter):
      self.updateBlobFilterParameters(bf)
      
      mask, points = self.applyBlobFilter(self.frame, bf, self.dilation_size, self.erosion_size)
      self.blob_filter[bf]['points'] = points
      
      #print([name]+ points)

      # compute distances between blobs of the same color
      mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
      mask_bgr, distance = self.computeDistance(mask_bgr, points)
      mask_bgr[mask == 255] = [self.blob_filter[bf]['b'], self.blob_filter[bf]['g'], self.blob_filter[bf]['r']]
      self.blob_filter[bf]['mask_bgr'] = mask_bgr
      #print("distance1= %.2f" % distance)

      self.blob_filter[bf]['distance'] = distance
    
    # Compute angle
    #angle = computeAngle(frame, origin=points_2, end=points_1)
    
    # handle case esc is pressed
    k = cv2.waitKey(1)
    end = time.time()
    dt = (end - start)
    #print("time: %.5f, freq: %.5f" % (dt, 1/dt))
  
  def updateVisualizations(self):
    if self.gui:
      for bf in list(self.blob_filter):
        # Show points in color image
        for p in self.blob_filter[bf]['points']:
          cv2.circle(self.frame, (p[0], p[1]), 5, (self.blob_filter[bf]['b'], self.blob_filter[bf]['g'], self.blob_filter[bf]['r']), -1)
          #print(p[0],p[1])
        

      # Update figures
      self.out_image = self.frame
      for bf in list(self.blob_filter):
        self.out_image = np.concatenate((self.out_image, self.blob_filter[bf]['mask_bgr']), axis=1)

      cv2.imshow("tracker", self.out_image)



def main():
  # with gui enabled
  tracker1 = Tracker(gui=True,cam_index=2)
  tracker1.addColorBlob("red", r=255, g=0, b=0, r_min=90, r_max=255, g_min=0, g_max=80, b_min=0, b_max=80)
  # tracker.setCroppingPoints(tl_x=20, tl_y=20, br_x=100, br_y=100) 
  tracker1.setMorphologicalOperationParameters(dilation_size=12, erosion_size=2)

  tracker2 = Tracker(gui=True,cam_index=4)
  tracker2.addColorBlob("yellow", r=255, g=255, b=0, r_min=125, r_max=255, g_min=125, g_max=255, b_min=0, b_max=100)
  # tracker.setCroppingPoints(tl_x=20, tl_y=20, br_x=100, br_y=100) 
  tracker2.setMorphologicalOperationParameters(dilation_size=12, erosion_size=2)

  # with gui disabled
  # tracker = Tracker(gui=False,cam_index=2)
  # tracker.addColorBlob("red", r=255, g=0, b=0, r_min=0, r_max=255, g_min=0, g_max=255, b_min=0, b_max=255)
  # tracker.addColorBlob("yellow", r=255, g=255, b=0, r_min=0, r_max=255, g_min=0, g_max=255, b_min=0, b_max=255)
  # tracker.setCroppingPoints(tl_x=20, tl_y=20, br_x=100, br_y=100) 
  # tracker.setMorphologicalOperationParameters(dilation_size=10, erosion_size=10)

  while True:
    #tracker1.processCamera("red")
    #tracker1.updateVisualizations()
    #point1 = tracker1.getPoints("green1")
    #print(point1)
    
    tracker2.processCamera("yellow")
    tracker2.updateVisualizations()
    #point2 = tracker2.getPoints("green2")
    #print(point2)
  
#main()