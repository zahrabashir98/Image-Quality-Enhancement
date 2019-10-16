# Image-histogram-Stretch-Clip-and-Equalize
## This project includes the following parts:
* #### Stretching histogram:
    ##### The **Stretch** operation re-distributes values of an input image over a wider or narrower range of values in an output image. Stretching can for instance be used to enhance the **contrast** in your image when it is displayed.
    
    ###### the formula: 

   ```sh
                        g(x,y) = (f(x,y) - fmin/ (fmax- fmin)) *255
    ```
* #### Clipping 1 percent of histigram:
     ##### The **Clipping** operation acts like the prevoius one with one difference. We remove the outliers which may cause problem. For instance, if the minimum and maximum are near 0 and 255 respectively, then our strething does not effect that much on  image contast. By applying this approach we remove ,say 1 percent, from the begining and the end of the data (pixel colors) and then apply streching.


* #### Histogram Equalization:
     #####  **Histogram Equalization** is a method to process images in order to adjust the contrast of an image by modifying the intensity distribution of the histogram. The objective of this technique is to give a linear trend to the cumulative probability function associated to the image.
    
    ##### [This link](http://www.sci.utah.edu/~acoste/uou/Image/project1/Arthur_COSTE_Project_1_report.html) helps you to learn it well !
***
### How to run:
##### The main code is located in `Main.py`.
##### You can see the results and tranfromation fucntions it the separet folders.
#### `As an example:`This is the input and output of mine:
![The primary image](/images/Q3.jpg)

![After applying the approaches with local area = 1](/results/local_area(1).jpg)
