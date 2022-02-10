"""Julia set generator"""

import time
from PIL import Image
import array

from decorator import timefn

# area of complex space to investigate
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193


# draw images
def show_greyscale(output_raw, width, height):
    """convert list to array, show using PIL"""
    # convert output to PIL-compatible input
    # scale to [0...255]
    max_value = float(max(output_raw))
    print(max_value)
    scale_factor = float(max_value)
    scaled = [int(o / scale_factor * 255) for o in output_raw]
    output = array.array('B', scaled)
    im = Image.new("L", (width, height))
    im.frombytes(output.tobytes(), "raw", "L", 0, -1)
    im.show()


def show_false_greyscale(output_raw, width, height):
    """convert list to array, show using PIL"""
    # convert output to PIL-compatible input
    assert width * height == len(output_raw)
    max_value = float(max(output_raw))
    output_raw_limited = [int(float(o) / max_value * 255) for o in output_raw]
    output_rgb = ((o + (256 * o) + (256 ** 2) * o) * 16 for o in output_raw_limited)  # fancier
    output_rgb = array.array('I', output_rgb)
    im = Image.new("RGB", (width, height))
    im.frombytes(output_rgb.tobytes(), "raw", "RGBX", 0, -1)
    im.show()


@timefn
def calculate_z_serial_purepython(max_iter, zs, cs):
    """calculate output list using Julia update rule: f(z) = z**2 + c"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < max_iter:
            z = z * z + c
            n += 1
        output[i] = n
    return output


def calc_pure_python(width, max_iter, draw_output=False, greyscale=True):
    """create a list of complex coordinates (zs) and complex parameters (cs), build Julia set
    f(z) = z**2 + c
    """
    x_step = (x2 - x1) / width
    y_step = (y1 - y2) / width
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))
    print("Length of x: ", len(x))
    print("Total elements: ", len(zs))
    start_time = time.time()
    output = calculate_z_serial_purepython(max_iter, zs, cs)
    end_time = time.time()
    secs = end_time - start_time
    print(calculate_z_serial_purepython.__name__ + " took", secs, "seconds")

    # for width = 1000 and max_iter = 300
    # assert sum(output) == 33219980
    if draw_output:
        if greyscale:
            show_greyscale(output, width, width)
        else:
            show_false_greyscale(output, width, width)


if __name__ == "__main__":
    calc_pure_python(width=1000, max_iter=300, draw_output=True, greyscale=True)
