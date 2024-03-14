from pycasso import Canvas
import sys

# credits: pycasso code from pypi.org/project/image-scramble/2.0.1/


if len(sys.argv) <=3:
    print("please provide filePath and 'num horizontal cells' and 'num vertical cells' ")
    quit()

filePath = sys.argv[1]
hor_num_slices = int(sys.argv[2])
ver_num_slices = int(sys.argv[3])

# todo - retrieve w and h from img?
img_width = 710
img_height = 820

slice_weight = round(img_width / hor_num_slices)
slice_height = round(img_height / ver_num_slices)
slice_size = (slice_weight, slice_height)

num_pycasso_scrambles = 1

for i in range(num_pycasso_scrambles):
    seed = 'seed' + str(i)
    pycasso = Canvas(filePath, slice_size, seed)
    pycasso.export(mode='scramble' , path='pycasso_scramble_' + str(i), format='png')

