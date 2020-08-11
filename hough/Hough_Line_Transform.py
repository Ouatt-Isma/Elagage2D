
#------------------------------------#
# Author: Yueh-Lin Tsou              #
# Update: 7/23/2019                  #
# E-mail: hank630280888@gmail.com    #
#------------------------------------#

"""----------------------
- Hough Line Transform
----------------------"""

from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2
from PIL import Image
import os

def droite(x1 , y1 , x2 , y2):
    a = (y2 - y1)/(x2 - x1)
    b = y1 - a*x1
    return a,b 

def xymax(a , b , xmax , ymax):
    x = xmax
    y = int(a*x + b)
    if (y<ymax):
        return x,y
    else:
        return int((ymax - b)/a) , ymax

def xymin(a , b , xmin , ymin):
    x = xmin
    y =int(a*x + b)
    if (y>ymin):
        return x,y
    else:
        return int((ymin - b)/a) , ymin


# ---------------- Function to do Hough Line Transform ---------------- #
def Hough_Line(image, edges):
    img = image.copy()

    # Hough Line Transform
    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    xmax ,ymax , rgb= img.shape
    xmax-=1
    ymax-=1
    m = open("size.txt","w")
    m.write(str(xmax)+"\n")
    m.write(str(ymax)+"\n")
    print("nombre de ligne ",len(lines))
    # Draw all the line on the image
    ss = 5000

    f = open(name+".txt","w")
    for i in range(0, len(lines)):
        
        for rho,theta in lines[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
           
            """
            if (x1 - x2 != 0):
                a , b = droite(x1, y1 , x2, y2)
                x1 , y1 = xymin(a , b , 0 , 0)
                x2 , y2 = xymax(a , b , xmax , ymax)
              
            """
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),5)
            f.write(str(x1) + " "+str(y1) +" "+str(x2) + " "+str(y2) +"\n")
            
          
    f.close()
    m.close()

    # show result
    #plt.subplot(111), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #plt.show()

    return img

# ---------------- Function to do Probabilistic Hough Line Transform ---------------- #
def P_Hough_Line(image, edges):
    img = image.copy()
    xmax,ymax , rgb= img.shape
    xmax-=1
    ymax-=1

    # Probabilistic Hough Transform
    minLineLength = 10000
    maxLineGap = 5
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
   
    print("nombre de ligne ",len(lines))
    ss = 5000
    f = open(name+".txt","w")
    # Draw all the line on the image
    for i in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            """
            if (x1 <0 or x2<0 or y1<0 or y2<0):
                break
            
            if (x1 - x2 !=0):
                a , b = droite(x1, y1 ,x2, y2)
                x1 , y1 = xymin(a , b , 0 , 0)
                x2 , y2 = xymax(a , b , xmax , ymax)
            
            """
            f.write(str(x1) + " "+str(y1) +" "+str(x2) + " "+str(y2) +"\n")
            
        
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)
            
    f.close()

    
    
    # show result
    #plt.subplot(111), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #plt.show()


    return img

# -------------------------- main -------------------------- #
if __name__ == '__main__':
    # read one input from terminal
    # (1) command line >> python Hough_Line_Transform.py -i pool.jpg
    """
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required = True, help = "input image source path")
    args = vars(ap.parse_args())
    """
    default_path = os.getcwd()
    input = "images"
    if os.path.isdir(input):
        img_path = input
        img_name_list = []
        for dirpath, dirnames, files in os.walk(img_path):
            for f in files:
                if f.endswith(('.png', '.bmp', '.jpg')):
                    img_name_list.append(os.path.join(dirpath, f))

        cpt =0
        tot = len(img_name_list)
        for img_name in img_name_list:
            name = os.path.basename(img_name)
            name = os.path.splitext(name)[0]
            print("Working with :" + name)
            cpt+=1
            print(str(cpt)+ "/" + str(tot))
            
             # read image
            image = cv2.imread(img_name)
    # convert to grayscale
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # get edges by using "Canny edge detection"
            edges = cv2.Canny(gray,50,150,apertureSize = 3)

    # Functions
            try : 
                os.mkdir("out")
            except:
                pass
            os.chdir("out")
            
            try :  
                Image.fromarray(P_Hough_Line(image, edges)).save(name +"_hough1.jpg")
                Image.fromarray(Hough_Line(cv2.imread(name +"_hough1.jpg"), edges)).save(name +"_hough2.jpg")
                print("sauvegarde dans out du fichier "+name+"_hough1.jpg réussi !!!")
            except : 
                pass
            """
            try : 
                Image.fromarray(Hough_Line(cv2.imread(name +"_hough1.jpg"), edges)).save(name +"_hough2.jpg")
                print("sauvegarde dans ../../hough/images du fichier hough2.jpg réussi !!!")
            except :
                pass
            """
            os.chdir(default_path)
   




# Reference:
# Website: OpenCV-Python Document
# Link: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html#hough-lines
