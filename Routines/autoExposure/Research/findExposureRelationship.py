"""
NAME: findExposureRelationship.py
AUTHOR: John Archibald Page
DATE CREATED: 12/06/2023
DATE LAST UPDATED: 12/06/2023

PURPOSE:
    To find the linear relationship of the andor camera between counts and exposure.

TO RUN:
    >python findExposureRelationship.py tifffolder

UPDATE HISTORY:
    When making an update to the code, remember to put a comment in the code what was changed and why
    .i.e. #01/12/2022: updated the message used in the pop up
"""
#call in modules
import logging as log ##troubleshooting
log.info(__file__)  ##troubleshooting
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import sys
import os

#call in which folder is being used---------------------------------------------------------
dir = os.getcwd()
foldername = sys.argv[1]
darkfile = sys.argv[2]
imagefiles = [os.path.join(dir+"\\"+foldername, file) for file in os.listdir(dir+"\\"+foldername) if file.endswith(".TIFF")]

#-------------------------------------------------------------------------------------------
#definition
def checkSaturation(file, saturationLevel = (2**16)-1, saturationPercentage = 0.05):
    """Checks saturation flag of an image. 16 bit image so 2**16 bit depth"""
    print(file)
    img = Image.open(file)
    img = np.array(img)
    print("saturation check is running")
    print("(min,max): ",np.amin(img), np.amax(img))
    #number of pixels
    pixels_sat_arr = (img >= saturationLevel) #array of truth values where saturation is true
    pixels_sat = pixels_sat_arr.sum() #the sum of truth values in above array
    pixels_tot = img.shape[0] * img.shape[1]  #total number of pixels
    #If number of saturated pixels greater than freshold to be in image, saturationflag = True
    print(f"Total number of pixels {pixels_tot}")
    print(f"Saturated pixel number {pixels_sat}")
    print(f"Percentage of pixels saturated {pixels_sat/pixels_tot}")
    if pixels_tot*saturationPercentage > pixels_sat:
        saturationFlag = False
    else:
        saturationFlag = True
    print(saturationFlag)
    return(saturationFlag, (pixels_sat/pixels_tot)*100)

def checkCounts(file, x, y, xlen, ylen):
    """Checks the average counts for a given array."""
    img = Image.open(file)
    array = np.array(img)
    ROIarray = array[x:x+xlen,y:y+ylen]
    avgVal = np.average(ROIarray)
    return(avgVal)

def checkLinear(counts_list):
    """Checks whether a data set gradient is continuing to be linear"""
    #variables
    counter = 0
    linearFlag = True
    #run while loop until the data values are not linear
    while linearFlag == True and counter < len(counts_list)-1:
        print("while loop is running!")
        grad1 = (counts_list[counter+1] - counts_list[counter])/(exposurelists[counter+1] - exposurelists[counter])
        grad2 = (counts_list[counter+2] - counts_list[counter+1])/(exposurelists[counter+2] - exposurelists[counter+1])
        print(grad1,grad2)
        if grad2 <= grad1 + grad1*2 and grad2 >= grad1 - grad1*2:
            counter += 1
        else:
            linearFlag = False
    print(counter)
    return(counter)
    
def orderFilenames(imagefiles):
    """Orders list of file names by their exposure number"""
    exposures = [float(i.split("\\")[-1].replace("ms.TIFF","")) for i in imagefiles]
    exposure_order_index = np.argsort(exposures)
    imagefiles_order = [imagefiles[i] for i in exposure_order_index]
    return(imagefiles_order)

#get saturation flag values------------------------------------------------------------------
exposurelists, satperc_list, counts_list = [], [], []
if_ordered = orderFilenames(imagefiles)
for i in if_ordered:
    exposurelists.append(float(i.split("\\")[-1].replace("ms.TIFF","")))
    #saturation check
    satpass,satperc = checkSaturation(i)
    satperc_list.append(satperc)
    #counts check
    counts = checkCounts(i, 790,1024,184,164) - checkCounts(darkfile, 790,1024,184,164) #counts - dark
    counts_list.append(counts)
 
#plots--------------------------------------------------------------------------------------
###plot the saturation percentage###
plt.title("exposure (ms) vs Saturation (%)")
plt.xlabel("exposure (ms)")
plt.ylabel("Saturation (%)")
plt.plot(exposurelists,satperc_list)
plt.xlim(0,1.5)
plt.savefig(dir+"\\"+foldername+"\\saturationcheck.png")
plt.close()

###plot the counts###
#define the linear section
counter = checkLinear(counts_list)
expslice = exposurelists[:counter]
countsslice = counts_list[:counter]
res = stats.linregress(expslice,countsslice)

#plot the exposure vs counts
plt.title("exposure (ms) vs ROI counts")
plt.xlabel("exposure (ms)")
plt.ylabel("counts")
plt.plot(exposurelists,counts_list)
plt.plot(expslice, res.intercept + res.slope*np.array(expslice), 'r', label='fitted line')
plt.xlim(0,8)
plt.savefig(dir+"\\"+foldername+"\\countscheck.png")
plt.close()

#optimum exposure-----------------------------------------------------------------------------------------
print(f"Maximum Exposure: {exposurelists[counter]} ms")
print(f"Maximum Exposure Saturation level: {satperc_list[counter]} %")
print("-------------------------------------------------------------")#
print(f"70% Exposure: {exposurelists[counter]*0.7} ms")
print(f"70% Exposure Saturation level: {satperc_list[counter]*0.7} %")

#save outputting linear line
df = pd.DataFrame({'gradient': [res.slope],
                   'intercept': [res.intercept],
                   'maximumSaturation': [satperc_list[counter]],
                   'maximumExposure': [exposurelists[counter]]})
df.to_csv(dir+"\\"+foldername+"\\expLinearRelationship.csv")