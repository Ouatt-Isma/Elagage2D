"""
Created on Mon Oct 30 12:41:30 2017

@author: mohabmes
"""

import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import argparse 
import os

threshold_values = {}
h = [1]


def Hist(img):
   row, col = img.shape 
   y = np.zeros(256)
   for i in range(0,row):
      for j in range(0,col):
         y[img[i,j]] += 1
   x = np.arange(0,256)
   #plt.bar(x, y, color='b', width=5, align='center', alpha=0.25)
   #plt.show()
   return y


def regenerate_img(img, threshold):
    row, col = img.shape 
    y = np.zeros((row, col))
    for i in range(0,row):
        for j in range(0,col):
            if img[i,j] >= threshold:
                y[i,j] = 255
            else:
                y[i,j] = 0
    return y


   
def countPixel(h):
    cnt = 0
    for i in range(0, len(h)):
        if h[i]>0:
           cnt += h[i]
    return cnt


def wieght(s, e):
    w = 0
    for i in range(s, e):
        w += h[i]
    return w


def mean(s, e):
    m = 0
    w = wieght(s, e)
    for i in range(s, e):
        m += h[i] * i
    
    return m/float(w)


def variance(s, e):
    v = 0
    m = mean(s, e)
    w = wieght(s, e)
    for i in range(s, e):
        v += ((i - m) **2) * h[i]
    v /= w
    return v
            

def threshold(h):
    cnt = countPixel(h)
    for i in range(1, len(h)):
        vb = variance(0, i)
        wb = wieght(0, i) / float(cnt)
        mb = mean(0, i)
        
        vf = variance(i, len(h))
        wf = wieght(i, len(h)) / float(cnt)
        mf = mean(i, len(h))
        
        V2w = wb * (vb) + wf * (vf)
        V2b = wb * wf * (mb - mf)**2
        
        fw = open("trace.txt", "a")
        fw.write('T='+ str(i) + "\n")

        fw.write('Wb='+ str(wb) + "\n")
        fw.write('Mb='+ str(mb) + "\n")
        fw.write('Vb='+ str(vb) + "\n")
        
        fw.write('Wf='+ str(wf) + "\n")
        fw.write('Mf='+ str(mf) + "\n")
        fw.write('Vf='+ str(vf) + "\n")

        fw.write('within class variance='+ str(V2w) + "\n")
        fw.write('between class variance=' + str(V2b) + "\n")
        fw.write("\n")
        
        if not math.isnan(V2w):
            threshold_values[i] = V2w


def get_optimal_threshold():
    min_V2w = min(threshold_values.values())
    optimal_threshold = [k for k, v in threshold_values.items() if v == min_V2w]
   
    return optimal_threshold[0]

"""
a = Image.open('DJI_0198.jpg')
image = a.convert("L")
img = np.asarray(image)
"""
"""
b = a.copy()

temp = np.asarray(b)
temp.setflags(write=1)
print np.shape(temp[0][0])

for i in temp : 
    for j in i: 
        j[1] = 0
    """    
       

#Image.fromarray(temp).show()
#img = Image.fromarray(temp).convert('L')
#img.show()
#img = np.asarray(img)
"""
h = Hist(img)
threshold(h)
"""
#op_thres = get_optimal_threshold()
"""
op_thres=200 #230
res = regenerate_img(img, op_thres)
Image.fromarray(res).convert('L').save("moi.png")
plt.imshow(res)
plt.savefig("otsu.jpg")
"""

if __name__ =='__main__':
    
    default_path = os.getcwd()
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--type', required = True, help = "input type of clean")
    args = vars(ap.parse_args())
    type = args["type"] 
    if (type=='1'):
        op_thres=200
    else : 
        op_thres=250
    input = "../images"
    result = []
    if os.path.isdir(input):
        img_path = input
        img_name_list = []
        for dirpath, dirnames, files in os.walk(img_path):
            for f in files:
                if f.endswith(('.png', '.bmp', '.jpg')):
                    img_name_list.append(os.path.join(dirpath, f))

        tot = len(img_name_list)
        cpt = 0
        for img_name in img_name_list:
            cpt+=1
            name = os.path.basename(img_name)
            name = os.path.splitext(name)[0]
            print("Working with :" + name)
            print(str(cpt)+ "/" + str(tot))
           
            Im = Image.open(img_name)
            image = Im.convert("L")
            img = np.asarray(image)
            h = Hist(img)
            threshold(h)
            op_thres = get_optimal_threshold() + 110

            
            if (op_thres>250):
                if(type == '2'):
                     op_thres = 250
                else : 
                    op_thres = 220

            elif (op_thres<230):
                if (type == '2'):
                    op_thres=230
                else : 
                    op_thres = 200
            else :    
                if (type == '1'):
                    op_thres-=30
            op_thres = 250
            print(op_thres)
            
            res = regenerate_img(img, op_thres)
            try :  
                os.mkdir("out")
            except : 
                #print("except : out")
                pass
            os.chdir("out")
            

            Image.fromarray(res).convert('L').save(name+"_otsu"+type+".jpg")
            print ("sauvegarde dans out du fichier "+ name + "_otsu" + type + ".jpg réussi !!!")

            if (type == '2'):
                try : 
                    os.mkdir("../../hough/images") 
                except :
                    #print("except : ../../hough/images")
                    pass
            
                os.chdir("../../hough/images") 
                Image.fromarray(res).convert('L').save(name + "_otsu" +type+".jpg")
                print("sauvegarde dans ../../hough/images du fichier " +name + "_otsu" +type+ ".jpg réussi !!!")
                os.chdir(default_path)
   
 