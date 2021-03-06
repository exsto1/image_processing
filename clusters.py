import sys
from skimage import io
from sklearn.cluster import KMeans
import numpy as np
import PIL.Image



# reading filename

filename = sys.argv[1]
n_of_clusters = sys.argv[2]
n_of_clusters = int(n_of_clusters)

rgba_image = PIL.Image.open(filename)
rgb_image = rgba_image.convert('RGB')
rgb_image = rgb_image.save(f"c_{filename}")

# reading the image
image = io.imread(f"c_{filename}")

# preprocessing
rows, cols = image.shape[0], image.shape[1]
image = image.reshape(rows * cols, 3)

# modelling
print('Compressing...')
print('Note: This can take a while for a large image file.')
kMeans = KMeans(n_clusters=n_of_clusters)
kMeans.fit(image)

# getting centers and labels
centers = np.asarray(kMeans.cluster_centers_, dtype=np.uint8)
labels = np.asarray(kMeans.labels_, dtype=np.uint8)
labels = np.reshape(labels, (rows, cols))
print('Almost done.')

# reconstructing the image
newImage = np.zeros((rows, cols, 3), dtype=np.uint8)
for i in range(rows):
    for j in range(cols):
        # assinging every pixel the rgb color of their label's center
        newImage[i, j, :] = centers[labels[i, j], :]
io.imsave(filename.split('.')[0] + '-compressed.png', newImage)

print('Image has been compressed sucessfully.')