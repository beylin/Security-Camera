import cv2
import numpy as np

# 1. Load the two images of apple and orange.
apple = cv2.imread("apple.jpg")
apple = cv2.resize(apple, (512, 512))
orange = cv2.imread("orange.jpg")

# 2. Find the Gaussian Pyramids for apple and orange (in this particular example, number of levels is 6).
gp_apple = [apple]
gp_orange = [orange]
for i in range(6):
    layer1 = cv2.pyrDown(gp_apple[i])
    gp_apple.append(layer1)
    layer2 = cv2.pyrDown(gp_orange[i])
    gp_orange.append(layer2)

'''
for i in range(0, 7):
    cv2.imshow("gp_apple " + str(i), gp_apple[i])
    cv2.imshow("gp_orange " + str(i), gp_orange[i])
'''

# 3. From Gaussian Pyramids, find their Laplacian Pyramids.
laplacian_apple = []
laplacian_orange = []

for i in range(6):
    '''
    cv2.imshow(str(i + 1), cv2.subtract(gp_apple[i], cv2.pyrUp(cv2.pyrDown(gp_apple[i]))))
    cv2.imshow(str(i + 1), cv2.subtract(gp_orange[i], cv2.pyrUp(cv2.pyrDown(gp_orange[i]))))
    '''
    laplacian_apple.append(cv2.subtract(gp_apple[i], cv2.pyrUp(cv2.pyrDown(gp_apple[i]))))
    # cv2.imshow(str(i + 1), laplacian_apple[i])
    laplacian_orange.append(cv2.subtract(gp_orange[i], cv2.pyrUp(cv2.pyrDown(gp_orange[i]))))
    # cv2.imshow(str(i + 1), laplacian_orange[i])
laplacian_apple.append(gp_apple[6])
laplacian_orange.append(gp_orange[6])

# 4. Now add left and right halves of images in each level
height = 512
width = 256
apple_orange_pyramid = []
for i in range(7):
    # print(height, width)
    apple_orange = np.hstack((laplacian_apple[i][:height, :width], laplacian_orange[i][:height, width:]))
    apple_orange_pyramid.append(apple_orange)
    # cv2.imshow(str(i + 1), apple_orange_pyramid[i])
    height = int(height / 2)
    width = int(width / 2)

# 5. Now reconstruct
apple_orange_reconstruct = apple_orange_pyramid[6]
for i in range(5, -1, -1):
    apple_orange_reconstruct = cv2.pyrUp(apple_orange_reconstruct)
    apple_orange_reconstruct = cv2.add(apple_orange_reconstruct, apple_orange_pyramid[i])
cv2.imshow("apple_orange_reconstruct", apple_orange_reconstruct)

cv2.waitKey(0)
cv2.destroyAllWindows()
