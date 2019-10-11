import cv2
import matplotlib.pyplot as plt
from math import log2
import os
import numpy

def plotter(img_list, r, w, gray, wr, hr, fig_name = None):
    plt.rcParams['figure.figsize'] = (wr, hr)
    for i in range(len(img_list)):
        plt.subplot(r, w, i + 1)
        if gray:
            plt.imshow(img_list[i][0], cmap = 'gray')
        else:
            plt.imshow(img_list[i][0])
        plt.title(img_list[i][1])
        plt.xticks([])
        plt.yticks([])
    if fig_name is not None:
        plt.savefig(fig_name + '.jpg')
    plt.show()

def each_part_strech(image, type_string):
    transform_function = [] 
    histg = cv2.calcHist([image],[0],None,[256],[0,256]) 

    freq_list = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            freq_list.append(image[i,j])
    
    if type_string == "stretch":
        c = min(freq_list)
        d = max(freq_list)
    elif type_string == "clip":
        freq_list.sort()
        clip1_list = freq_list[600:59400]
        c = min(clip1_list)
        d = max(clip1_list)

    # print(c, d)
    a = numpy.zeros(shape=(image.shape[0], image.shape[1]))
    for area in range(local_area):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                a[i,j] = round((image[i,j]-c)*(255)/(d-c))
                if a[i,j] <0:
                    a[i,j] = 0
                elif a[i,j]>255:
                    a[i,j] = 255
    
    # transform function
    for i in range(0,255):
        new_num = round((i-c)*(255)/(d-c))
        if new_num < 0:
            new_num = 0
        elif new_num > 255:
            new_num = 255
        transform_function.append((i,new_num))   

    return a, transform_function

def seperate_picture(img, local_area):
    croped_images = []
    if local_area == 1 :
        return [img]
    

    elif local_area == 4:
        for i in range(2):
            for j in range(2):
                a, b = int(0 + (j*image.shape[0]/2)), int(image.shape[0]/2 + (j* image.shape[0]/2))
                x, y = int(0 + (i*image.shape[1]/2)), int(image.shape[1]/2 + (i *image.shape[1]/2))
                croped_images.append(img[a:b, x:y])
        # croped_images.append(img[0:100, 0:150])
        # croped_images.append(img[100:200, 0:150])
        # croped_images.append(img[0:100, 150:300])
        # croped_images.append(img[100:200, 150:300])
        croped_images = numpy.array(croped_images)
        return croped_images

    elif local_area == 8:
        for i in range(2):
            for j in range(4):
                a, b = int(0 + (j*image.shape[0]/4)), int(image.shape[0]/4 + (j* image.shape[0]/4))
                x, y = int(0 + (i*image.shape[1]/2)), int(image.shape[1]/2 + (i *image.shape[1]/2))
                croped_images.append(img[a:b, x:y])

        # croped_images.append(img[0:50, 0:150])
        # croped_images.append(img[50:100, 0:150])
        # croped_images.append(img[100:150, 0:150])
        # croped_images.append(img[150:200, 0:150])
        # croped_images.append(img[0:50, 150:300])
        # croped_images.append(img[50:100, 150:300])
        # croped_images.append(img[100:150, 150:300])
        # croped_images.append(img[150:200, 150:300])
        croped_images = numpy.array(croped_images)
        return croped_images

def concat_images(pictures_list):
    if local_area == 4:
        f = numpy.row_stack((pictures_list[0], pictures_list[1]))
        g = numpy.row_stack((pictures_list[2], pictures_list[3]))
        h = numpy.column_stack((f,g))
        return h

    elif local_area == 8:
        f = numpy.row_stack((pictures_list[0], pictures_list[1],pictures_list[2],pictures_list[3] ))
        g = numpy.row_stack((pictures_list[4], pictures_list[5], pictures_list[6], pictures_list[7]))
        h = numpy.column_stack((f,g))
        return h



def stretch_hist(image, local_area ):

    transform_functions = [[(color_s, color_d) for color_s, color_d in zip(range(256), range(256))] for _ in range(local_area)]
    croped_images = seperate_picture(image, local_area)
    pictures_list = []
    print("Strech - For Local Area %s"%local_area)

    for i in range(local_area):
        new_image, tf = each_part_strech(croped_images[i], "stretch")
        
        pictures_list.append(new_image)
        transform_functions[i] = tf

    if local_area != 1:
        new_image = concat_images(pictures_list)

    return new_image, transform_functions




def clip1_hist(image, local_area = 1):
    
    transform_functions = [[(color_s, color_d) for color_s, color_d in zip(range(256), range(256))] for _ in range(local_area)]
    croped_images = seperate_picture(image, local_area)
    pictures_list = []
    print("Clip1 - For Local Area %s"%local_area)

    for i in range(local_area):
        new_image, tf = each_part_strech(croped_images[i], "clip")
        pictures_list.append(new_image)
        transform_functions[i] = tf
    
    if local_area != 1:
        new_image = concat_images(pictures_list)

    return new_image, transform_functions


def CDF_calculator(h):
	# finds cumulative sum
	return [sum(h[:i+1]) for i in range(len(h))]


def equalize(image):

    histg = cv2.calcHist([image],[0],None,[256],[0,256]) 
    cdf = numpy.array(CDF_calculator(histg))

    #transfer function
    sk = numpy.uint8(255 * cdf / (image.shape[0]* image.shape[1])) 
    new_image = numpy.zeros_like(image)

	# equalize each pixel
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            new_image[i, j] = sk[image[i, j]]

    transform_function = []
    for i in range(256):
        transform_function.append((i,sk[i]))
    return new_image, transform_function


def equalize_hist(image, local_area ):

    transform_functions = [[(color_s, color_d) for color_s, color_d in zip(range(256), range(256))] for _ in range(local_area)]
    croped_images = seperate_picture(image, local_area)
    pictures_list = []
    print("Equalization - For Local Area %s\n"%local_area)

    for i in range(local_area):
        new_image, tf = equalize(croped_images[i])
        pictures_list.append(new_image)
        transform_functions[i] = tf
    
    if local_area != 1:
        new_image = concat_images(pictures_list)

    return new_image, transform_functions

image_list = []
local_areas = [1,4, 8]
image = cv2.imread(os.path.join('images', 'Q4.jpg'), cv2.IMREAD_GRAYSCALE)
image_list.append([image, 'src'])

for local_area in local_areas:
    stretched, transforms_stretched = stretch_hist(image, local_area)
    clipped, transforms_clipped = clip1_hist(image, local_area)
    equalized, transforms_equalized = equalize_hist(image, local_area)
    if local_area == 1:
        plt.rcParams['figure.figsize'] = (20, 10)
        for tr, title in [(transforms_stretched, 'transform_stretched'), (transforms_clipped, 'transform_clipped'), (transforms_equalized, 'transform_equalized')]:
            plt.plot([x for x, _ in tr[0]], [y for _, y in tr[0]])
            plt.title(title)
            plt.savefig(title + '.jpg')
            plt.show()
    image_list.append([stretched, 'stretch(%s)'%(local_area)])
    image_list.append([clipped, 'clipping 1 percent(%s)'%(local_area)])
    image_list.append([equalized, 'equalize(%s)'%(local_area)])
    plotter(image_list, 2, 2, True, 20, 10, 'q4a-la(%s)'%(local_area))
    image_list = []