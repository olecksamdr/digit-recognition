from skimage.transform import resize, SimilarityTransform, warp
import numpy as np

def make_mnist(img):
    # Padding

    # height - number of rows
    # with - number of columns
    height, width = img.shape
    padding = 450

    # Add Pading Around Image
    tmp = np.zeros((height + 2 * padding, width + 2 * padding)).astype(int)
    tmp[padding:padding + height, padding:padding + width] = img

    # Computing the bounding box
    nonzY, nonzX = np.where(tmp)
    min_y, min_x = nonzY.min(), nonzX.min()
    max_y, max_x = nonzY.max(), nonzX.max()

    boundingBoxWith = max_x - min_x
    boundingBoxHeight = max_y - min_y
     
    if boundingBoxWith < boundingBoxHeight:
        max_x = min_x + boundingBoxHeight

    if boundingBoxWith > boundingBoxHeight:
        max_y = min_y + boundingBoxWith

    img = resize(tmp[min_y:max_y, min_x:max_x].astype(float), (20, 20))
    
    # Now inserting the 20x20 image
    tmp = np.zeros((28,28))
    tmp[0:20, 0:20] = img

    # Calculating translation
    
    Y, X = np.where(tmp)
    height, width = tmp.shape

    tsy, tsx = np.round(height / 2 - Y.mean()), np.round(width / 2 - X.mean())

    # Moving the digit
    tf = SimilarityTransform(translation=(-tsx, -tsy))
    tmp = warp(tmp, tf)
    return np.round(tmp).astype(int)
