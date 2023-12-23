import imageio.v3 as iio

im = iio.imread('Documents/rrt_project/N_map.png')
print(im.shape)  # (300, 451, 3)
print(im[20,50])