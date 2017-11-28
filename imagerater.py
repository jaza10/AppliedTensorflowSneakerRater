#!/usr/bin/env python

import time
from PIL import Image
import glob
from matplotlib import pyplot as plt
import numpy as np
import sys, getopt

plt.ion()
try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:x:f:q:",["minimum=","maximum=","filelocation=","question="])
except getopt.GetoptError:
	print('imagerater.py -f <filelocation> -i <minimum> -x <maximum> -q <question>')
	sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('imagerater.py -f <filelocation> -i <minimum> -x <maximum> -q <question>')
        sys.exit()
    elif opt in ("-i", "--minimum"):
        min = int(arg)
    elif opt in ("-x", "--maximum"):
        max = int(arg)
    elif opt in ("-f", "--filelocation"):
        filelocation = arg
    elif opt in ("-q", "--question"):
        question = arg

print('Minimum is {}'.format(min))
print('Maximum is {}'.format(max))
print('Filelocation is {}'.format(filelocation))
print('Question is "{}"'.format(question))

def get_rating(question, min, max):
    while True:
        try:
            value = int(input(question))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if (value < min or value > max):
            print("Sorry, your input must be between {} and {}.".format(min, max))
            continue

        else:
            break
    return value

def showAndRateImages(filelocation,min,max,question):
	# Check if file location is correct
    numerOfImagesInFolder = len(glob.glob(filelocation))
    if(numerOfImagesInFolder != 0):
        #Get dimension of first image
        firstFile = glob.glob(filelocation)[0]
        firstImage = Image.open(firstFile)
        firstImageSize = np.array(list(firstImage.getdata())).flatten()
        #print(firstImageSize.shape)
        imageAndRating = np.zeros((1, firstImageSize.shape[0] + 1), dtype=np.int8)
        # Create counter variable to save matrices
        i = 0
        for filename in glob.glob(filelocation):
			#Open image
            im=Image.open(filename)
			#Flatten image
            imageFlat=np.array(list(im.getdata())).flatten()
            imageFlat_reshaped = imageFlat.reshape(imageFlat.shape[0], -1).T
			#Normalize image
            imageFlat_reshaped_normalized = imageFlat_reshaped/255.
            plt.close()
            plt.figure()
            # Show image
            plt.imshow(im)
            plt.draw()
            rating = get_rating(question.format(str(i)), min, max)
            rating = np.array(rating).reshape(1,1)
            ratedData = np.append(imageFlat_reshaped_normalized, rating, axis=1)
            if(ratedData.shape[1] == imageAndRating.shape[1]):
                imageAndRating = np.append(imageAndRating, ratedData, axis=0)
            else:
                 print("Image at i={} with filename: {} skipped".format(i, filename))
            i += 1
			#Delete first row of zeros
            if(i==1):
                imageAndRating = np.delete(imageAndRating, (0), axis=0)
            if (i % 100 == 0):
			    # Save last 100 images
                np.save('imageAndRatingMatrix' + str(i), imageAndRating[i-99:i,:])
                continue
            if (i == numerOfImagesInFolder):
				# Save entire final matrix
                np.save('imageAndRatingMatrix' + str(i), imageAndRating)
                print("All images are flattened, normalized, rated and saved in the final matrix.")
    else:
        print("No images found in file location. Make sure that you have selected the right path")

showAndRateImages(filelocation,min,max,question)
