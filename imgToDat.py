import numpy as np
from PIL import Image
import math


def compressedImg(filePath, augment=1):
    img = Image.open(filePath)
    width, height = img.size

    # calculate gcd value of image to resize original image
    gcd_val = math.gcd(width, height)

    imgCompressed = img.resize(((width // gcd_val * augment), (height // gcd_val * augment)))
    # imgCompressed.save('compressed.png', 'png')

    if augment == 1:
        return np.array(list(img.getdata())).reshape(-1)
    else:
        return np.array(list(imgCompressed.getdata())).reshape(-1)


def restoreImg(decrypted, file_name, dimSize=(146,96)):
    temp = [np.uint8(i) for i in decrypted]

    width = int(dimSize[0])
    height = int(dimSize[1])
    temp = np.array(temp).reshape(height, width, 3)

    imgRecovered = Image.fromarray(temp)
    imgRecovered.save(file_name, format='png')


# if __name__ == '__main__':
#     compressedImg('space.jpg', 2)
#     restoreImg('data.txt', 'height_and_width.txt')
