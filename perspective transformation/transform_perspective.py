import numpy as np
import cv2

'''
takes in 4 points in any order and returns 
the same points in a known order to be used (the order)
each time we process 4 points wrt each other
'''
def order_points(pts):
    
    '''
    initialize a list of points that we'll order pts in it
    in the following order: 
    1-topleft 2-topright 3-bottomright 4-bottomleft
    '''
    rect= np.zeros((4, 2), dtype= "float32")
    
    
    #initialize the topleft & bottomright points
    rect[0]= pts[np.argmin(pts.sum(axis=1))]
    rect[2]= pts[np.argmax(pts.sum(axis=1))]
    
    
    #initialize the topright & bottomleft points
    rect[1]= pts[np.argmin(np.diff(pts, axis=1))]
    rect[3]= pts[np.argmax(np.diff(pts, axis=1))]
    
    return rect
    
def get_max_dimensions(rect):
    
    width1= np.sqrt((rect[0][0]- rect[1][0])**2 + (rect[0][1]- rect[1][1])**2)
    width2= np.sqrt((rect[2][0]- rect[3][0])**2 + (rect[2][1]- rect[3][1])**2)
    
    height1= np.sqrt((rect[0][0]- rect[3][0])**2 + (rect[0][1]- rect[3][1])**2)
    height2= np.sqrt((rect[1][0]- rect[2][0])**2 + (rect[1][1]- rect[2][1])**2)
    
    width= max(int(width1), int(width2))
    height= max(int(height1), int(height2))
    
    return width, height

def transform(image, pts):
    
    print(pts)
    #arrange the src perpective pts
    rect= order_points(pts)
    
    width, height= get_max_dimensions(rect)
    
    #these are the destination perpective, we'll build it 
    # with the same order we arranged pts
    dst= np.array([[0,0], [width-1,0], [width-1,height-1],[0,height-1]],
                  dtype= "float32")
    
    #computer the perspective transormation matrix and apply it
    M= cv2.getPerspectiveTransform(rect, dst)
    out= cv2.warpPerspective(image, M, (width, height))

    return out

    


    