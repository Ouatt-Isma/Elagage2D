from PIL import Image 
import numpy as np 
import time
import matplotlib.pyplot as plt 
import cv2 
import argparse
import os

def contain(L  , l):
	for i in L:
		if l==i:
			return True
	return False 

def main1(file):
	im = Image.open(file)
	ar = np.asarray(im) ; 
	l = []
	row , col , rgb = np.shape(ar)
	name = os.path.basename(img_name)
	name = os.path.splitext(name)[0] 
	
	file = name
	
	print ("row = ",row)
	print ("col = ",col)
	print ("intensity = ",rgb)

	for i in range(row):
		print(i, " / ", row)
		for j in range(col):

				b = list(ar[i][j])
				if not contain(l,b ):
					l.append(b)

	print (len(l))
	print()
	print(l)


def main2(file):
	
	
	im = Image.open(file)
	ar = np.asarray(im) 
	ar.setflags(write=1)
	name = os.path.basename(img_name)
	name = os.path.splitext(name)[0] 
	
	file = name
	
	l = []
	row , col , rgb = np.shape(ar)

	print ("row = ",row)
	print ("col = ",col)
	print ("intensity = ",rgb)
	for i in range(row):
		#if(i%int(row/100)==0):
		#	print(int(i/(int(row/100))), " " , end='')
		
		for j in range(col):

				if iswhite(ar[i][j]):
					#time.sleep(1)
					#print(True)
					white = [0,0,0]
					ar[i][j] = white
					for a in vois(i , row):
						for b in vois(j , col):
							ar[a][b] = white

	os.chdir("out_dil/"+name)
	print("saving .... " , file+"_step1.jpg")
	time.sleep(2)
	Image.fromarray(ar).save(file+"_step1.jpg")

def main3(file):
	
	im = Image.open(file)
	ar = np.asarray(im) 
	ar.setflags(write=1)
	name = os.path.basename(img_name)
	name = os.path.splitext(name)[0] 
	
	file = name
	
	l = []
	row , col , rgb = np.shape(ar)

	print ("row = ",row)
	print ("col = ",col)
	print ("intensity = ",rgb)
	print(ar[0][0])
	for i in range(row):
		for j in range(col):
				
				black = 0
				white=255
				if iswhite(ar[i][j]):
					#time.sleep(1)
					#print(True)
					
					ar[i][j] = black
					for a in vois(i , row):
						for b in vois(j , col):
							ar[a][b] = black
				
				else : 
					if (ar[i][j][0]!=ar[i][j][1] or ar[i][j][0]!=ar[i][j][2]):
						ar[i][j] = white
					"""for a in vois(i , row):
						for b in vois(j , col):
							ar[a][b] = white"""

	#os.chdir("out_dil/"+name)
	print("saving .... " , file+"_step2.jpg")
	time.sleep(2)

	Image.fromarray(ar).save(file+"_step2.jpg")

	


def iswhite(x):
	return x[0]>200 and x[0]==x[1] and x[1]==x[2] 
	
def vois(i, row):
	seuil = 2

	if i-seuil>0 and i+seuil<row :
		ll = list(range(i-seuil , i+seuil+1))
		ll.remove(i)
		return ll
	elif i-seuil<0 :
		ll = list(range(i+seuil+1))
		ll.remove(i)
		return ll
	else:
		ll=list(range(i-seuil,i+1))
		ll.remove(i)
		return ll

def verify(i,j , ar , row , col):
	print("i ==",i)
	print("j == ",j)
	
	for a in vois(i , row):
		for b in vois(j , col):
			print(a , ",",b )
			if (ar[i][j]==255):
				return True 
	return False 
def erod_dila(file):
	# Python program to demonstrate erosion and  
	# dilation of images.

	
	# Reading the input image 

	print(file)
	img = cv2.imread(file)
	name = os.path.basename(img_name)
	name = os.path.splitext(name)[0] 
	
	file = name
	size = 40
	# Taking a matrix of size 5 as the kernel 
	kernel = np.ones((5,5), np.uint8) 
	kernel_d = np.ones((size,size), np.uint8) 
	# The first parameter is the original image, 
	# kernel is the matrix with which image is  
	# convolved and third parameter is the number  
	# of iterations, which will determine how much  
	# you want to erode/dilate a given image.  
	img_erosion = cv2.erode(img, kernel, iterations=3) 
	Image.fromarray(img_erosion).save(file+"_eros.jpg") 
	img_dilation = cv2.dilate(cv2.imread(file + "_eros.jpg"), kernel_d, iterations=2) 
	"""
	cv2.imshow('Input', img) 
	cv2.imshow('Erosion', img_erosion) 
	cv2.imshow('Dilation', img_dilation) 
	"""
	#os.chdir("out_dil/"+name)
	Image.fromarray(img).save(file+"_ori.jpg")
	Image.fromarray(img_dilation).save(file + "_dil.jpg") 

def main():
	im = Image.open("moi.png")
	ar = np.asarray(im) ; 
	row , col = np.shape(ar)
	print ("row = ",row)
	print ("col = ",col)
	#print ("intensity = ",rgb)
	l=[0 , 0]
	for i in range(row):
		print(i, " / ", row)
		for j in range(col):
				if ar[i][j]==255:
					l[1]+=1
					if not verify(i,j , ar  , row , col):
						ar[i][j]=0
						print("hahaha")

				else :
					l[0]+=1
	print(l)


if __name__ == '__main__':

	"""
	ap = argparse.ArgumentParser()
	ap.add_argument('-i', '--image', required = True, help = "input image source path (without the extension)")
	args = vars(ap.parse_args())
    # read image
	"""
	
	input = "images"
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
			default_path = default_P+"/out_dil/"+name
			print("Working with :" + name)
			cpt+=1
			print(str(cpt)+ "/" + str(tot))

				# read image
			try : 
				os.mkdir("out_dil")
			except:
				#print("except : "+"out_dil/"+name)
				pass
			try : 
				os.mkdir("out_dil/"+name)
			except:
				#print("except : "+"out_dil/"+name)
				pass
			
			main2(img_name)
			main3(name+"_step1.jpg")
			erod_dila(name+"_step2.jpg")
			os.chdir(default_P)
