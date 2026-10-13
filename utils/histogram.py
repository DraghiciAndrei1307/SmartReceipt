import cv2
import matplotlib.pyplot as plt


gray = cv2.imread('../input_images/image_3_jumbo_gray.jpeg', cv2.IMREAD_GRAYSCALE)


hist = cv2.calcHist([gray], [0], None, [256], [0, 256])


plt.figure(figsize=(8, 4))
plt.title("Histogram")
plt.xlabel("Pixel value")
plt.ylabel("Nr. of pixels")
plt.plot(hist, color='black')
plt.xlim([0, 256])
plt.show()