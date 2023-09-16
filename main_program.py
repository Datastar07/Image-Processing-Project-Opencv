#Importing the numpy and opencv library.
import cv2
import numpy as np

#Define the color range of the boundary(for orange and blue color).
orange_lower = np.array([5, 100, 150], dtype=np.uint8)
orange_upper = np.array([15, 255, 255], dtype=np.uint8)

blue_lower = np.array([100, 30, 30], dtype=np.uint8)
blue_upper = np.array([130, 200, 200], dtype=np.uint8)

#Preproces the frame.
def process_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  #convert the RGB frame into the HSV(Hue,Saturation and Value) format.

    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)   #Find the orange color intensity using the inrange function.
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Find the external contours on the orange color object.

    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)  #Find the blue color intensity using the inrange function.
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Find the external contours on the blue color object.

    return (orange_contours,blue_contours)  #Return the blue and orange color frame.

#Make the rectangle outside the objects.
def Make_Rectangle(contour,frame):
    cont=max(contour,key=cv2.contourArea)   #Find contour which contain the maximum area on that frame. 
    area=cv2.contourArea(cont)
    if area>300:
        x,y,w,h=cv2.boundingRect(cont)
        w+=x
        h+=y
        cv2.rectangle(frame,(x,y),(w,h),(0,255,0),2) #Create green rectangle outside the orange and blue object.
        #Find the coordinate of the center of the rectangle.
        center_x=int((x+w)/2)   
        center_y=int((y+h)/2)
        #create the circle to the center.
        cv2.circle(frame,center=(center_x,center_y),radius=3,color=(0,0,0),thickness=-1)
        return (center_x,center_y)
    else: return (-1,-1)

#Make the line between the blue and orange object.
def Make_Line(frame,orange_contour,blue_contour):
    if len(orange_contour)>0 and len(blue_contour)>0:
        p1,q1=Make_Rectangle(orange_contour,frame=frame)
        p2,q2=Make_Rectangle(blue_contour,frame=frame)
        if p1>0 and q1>0 and p2>0 and q2>0:
            #Create the green color line between two objects.
            cv2.line(frame,(p1,q1),(p2,q2),color=(0,255,0),thickness=2)
            ax=int((p1+p2)/2)
            ay=int((q1+q2)/2)
            #Create the black circle on the center of the line.
            cv2.circle(frame,(ax,ay),radius=2,color=(0,0,0),thickness=-1)
    return frame

#Main function
def main():
    cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()

        if not ret:
            break
        
        #Find the orange and blue color object from the frame.
        orange,blue=process_frame(frame)
        #Create the line and rectangle outside the objects.
        preprocess_frame=Make_Line(frame=frame,orange_contour=orange,blue_contour=blue)
        #Starting the capturing the frame from the camera.
        cv2.imshow("video capture",preprocess_frame)

        #Press 'ESC' key for stoping the video frame.
        if cv2.waitKey(1)&0xff==27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()