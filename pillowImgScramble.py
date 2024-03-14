from PIL import Image
import numpy as np
import math
from icecream import ic
import sys


def calc_cell_pixels_1d(num_cells, size):
    """
    returns a list with the number of pixels per cell.
    e.g. 6 cells for size 15:
    [3, 3, 3, 2, 2, 2]
    """
    cell_sizes = []
    cell_size_floor = math.floor(size / num_cells)
    cell_rest_value = size - (cell_size_floor * num_cells)
    for i in range(num_cells):
        cell_size = cell_size_floor
        if (cell_rest_value > 0):
            cell_size += 1
            cell_rest_value -= 1
        cell_sizes.append(cell_size)
    return cell_sizes


def draw_cell_lines(im, y_offsets, x_offsets):
    """
    draws lines on a copy of the image according to calculate cells
    """
    np_im_lines = np.copy(im)
    y = 0
    for y_offset in y_offsets:
        x = 0
        for x_offset in x_offsets:
            # draw vertical lines
            for v in range(h):
                np_im_lines[v, x] = [0, 0, 0, 255]
            x += x_offset
        # draw horizontal lines
        for u in range(w):
            np_im_lines[y, u] =  [0, 0, 0, 255]

        y += y_offset
    return Image.fromarray(np_im_lines)


def shuffle_cell(np_im, from_x, from_y, to_x, to_y):
    """
    shuffles the pixel in a given range within a 3d numpy array representing an image
    """
    np_im_cell = np.copy(np_im[from_y:to_y, from_x:to_x, 0:np_im.shape[2]])
    cell_h = np_im_cell.shape[0]
    cell_w = np_im_cell.shape[1]
    cell_pixel_l = np_im_cell.shape[2]

    np_im_cell = np_im_cell.reshape(cell_h * cell_w, cell_pixel_l)
    np.random.shuffle(np_im_cell)
    np_im_cell = np_im_cell.reshape(cell_h, cell_w, cell_pixel_l)

    np_im[from_y:to_y, from_x:to_x, 0:np_im.shape[2]] = np_im_cell
    np_im_cell

    return np_im


def shuffle_cells(im, cell_heights, cell_widths):
    # draws lines on a copy of the image according to calculate cells
    np_im_shuffle = np.copy(im)
    y = 0

    for cell_height in cell_heights:
        x = 0
        for cell_width in cell_widths:
            np_im_shuffle = shuffle_cell(np_im_shuffle, x, y, x + cell_width, y + cell_height)
            x += cell_width
        y += cell_height
    return Image.fromarray(np_im_shuffle)




if len(sys.argv) <=3:
    print("please provide filePath and 'num horizontal cells' and 'num vertical cells' ")
    quit()

filePath = sys.argv[1]
hor_num_slices = int(sys.argv[2])
ver_num_slices = int(sys.argv[3])
ic(filePath, hor_num_slices, ver_num_slices)
im = Image.open(filePath)
w, h = im.size

R, G, B, A = (0, 1, 2, 3)

# calculate the number of pixels per cell in horizontal and vertical directions
cell_width_pixels = calc_cell_pixels_1d(hor_num_slices, w)
cell_height_pixels = calc_cell_pixels_1d(ver_num_slices, h)

# print size and number of cells and number of pixels per cell values
ic(w)
ic(hor_num_slices)
ic(cell_width_pixels)
ic(h)
ic(ver_num_slices)
ic(cell_height_pixels)

# create an image with lines indicating the cells; debug purpose
lines_img_filename = "pillow_cellLines.png"
im_lines = draw_cell_lines(im, cell_height_pixels, cell_width_pixels)
im_lines.save(lines_img_filename)

# create an image with the pixels shuffled within the calculated cell dimensions
shuffle_img_filename = "pillow_cellShuffle.png"
im_shuffle = shuffle_cells(im, cell_height_pixels, cell_width_pixels)
im_shuffle.save(shuffle_img_filename)