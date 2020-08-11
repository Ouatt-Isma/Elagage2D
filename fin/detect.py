from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2
import argparse
import os


"""

def vois(i, row):
    seuil = 10
    if i-seuil>0 and i+seuil<row :
        ll = list(range(i-seuil , i+seuil+1))
        # ll = list(range(i, i+seuil+1))
        ll.remove(i)
        return ll

    elif i-seuil<0 :
        ll = list(range(i+seuil+1))
        # ll = list(range(i,i+seuil+1))
        ll.remove(i)
        return ll

    else:
        ll=list(range(i-seuil,row))
        # ll = list(range(i-seuil,row))
        ll.remove(i)
        return ll
"""


def vois(i, row, seuil):

    if(i-seuil > 0 and i+seuil < row):
        ll = list(range(i-seuil, i+seuil+1))
        #ll = list(range(i, i+seuil+1))
        ll.remove(i)
        return ll

    elif (i-seuil < 0):
        ll = list(range(i+seuil+1))
        #ll = list(range(i, i+seuil+1))
        ll.remove(i)
        return ll

    else:
        ll = list(range(i-seuil, row))
        #ll = list(range(i, row))
        ll.remove(i)
        return ll

def vois2(i, row, seuil):

    if(i-seuil > 0 and i+seuil < row):
        #ll = list(range(i-seuil, i+seuil+1))
        ll = list(range(i, i+seuil+1))
        ll.remove(i)
        return ll

    elif (i-seuil < 0):
        #ll = list(range(i+seuil+1))
        ll = list(range(i, i+seuil+1))
        ll.remove(i)
        return ll

    else:
        #ll = list(range(i-seuil, row))
        ll = list(range(i, row))
        ll.remove(i)
        return ll

def iswhite(x):
    return x[0] == 255 and x[0] == x[1] and x[1] == x[2]


def main2(file):

    im = Image.open(file)
    im.thumbnail((500, 500), Image.ANTIALIAS)
    im.convert('L')
    print(im.size)
    ar = np.asarray(im)
    arc = np.asarray(im)
    ar.setflags(write=1)
    name = os.path.basename(img_name)
    name = os.path.splitext(name)[0]
    file = name

    l = []
    row, col, rgb = np.shape(ar)
    print("row = ", row)
    print("col = ", col)
    # print("intensity = ",rgb)

    ret = 0
    r = 10
    # seuil = 10
    # area = 5
    deb = 10
    for i in range(deb , row -deb):
        # if(i%int(row/100)==0):
        #   print(int(i/(int(row/100))), " " , end='')

        # print(i,"/",row)
        for j in range( deb , col - deb):
            
            if  iswhite(arc[i][j]):
                ar[i][j] = [0, 0, 255]

                
                    # time.sleep(1)
                    # print(True)
                
                if(True) :
                    cpt=0
                    
                    
                    for a in vois(i,row,r):
                        # print(a,"/",len(vois(i,row)))
                        for b in vois2(j , col,r):
                            # print("j")
                            # if(i==257):
                            #   print("a ", a," b ",b)
                            if iswhite(arc[a][b]):
                                cpt+=1
                    
                    if (cpt==0):
                        ret+=1
                        for a in vois(i,row,r):
                        # print(a,"/",len(vois(i,row)))
                            for b in vois(j , col,10):
                                ar[a][b] = [255, 0, 0]



                                

                if (False) : 

                    pass




               
    os.chdir("out_detec/"+name)
    print("saving .... " , file+"_detec.jpg")
    time.sleep(2)
    Image.fromarray(ar).save(file+"_detec.jpg")
    Image.fromarray(arc).save(file+".jpg")
    if (ret == 0):
        txt = 'no_problem'
    else : 
        txt = 'problem'
    f = open(txt+'.txt', 'w')
    f.write(str(ret))
    f.close()
    return ret


if __name__ == '__main__':

    """
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required = True, help = "input image source path (without the extension)")
    args = vars(ap.parse_args())
    # read image
    """
    
    input = "images_de"
    default_P = os.getcwd()
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
            default_path = default_P+"/out_detec/"+name
            print("Working with :" + name)
            cpt+=1
            print(str(cpt)+ "/" + str(tot))

                # read image
            try : 
                os.mkdir("out_detec")
            except:
                # print("except : "+"out_detec/"+name)
                pass
            try : 
                os.mkdir("out_detec/"+name)
            except:
                # print("except : "+"out_detec/"+name)
                pass
            
            print(main2(img_name))
            os.chdir(default_P)
