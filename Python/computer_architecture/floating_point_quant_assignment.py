#!/usr/bin/env python
#
#
# Author: Joe Weibel
# Program: floating_point_quant_assignment.py
# Purpose:
#   First:
    # Use latitude, longitude, altitude coordinates to perform some calculations.
    # The first is a coordinate change into Earth Centered, Earth Fixed (ECEF). Then use a
    # method for calculating the euclidean distance. Will then make observations on the precision
    # of the calculations using three different floating point definitions.
#   Second:
    # On a number line, place a sequence of at least 10 numbers (both +/-), along with the largest
    # possible value (+/-) represented in the 8-bit tiny notation.
    # You should observe the distance between the numbers, and make some comments.
#   Third:
    # perform quantization of an image using different quantization levels. Quantization can
    # take many forms. This project will focus on image quantization. Refer to the Wikipedia page on
    # Quantization. To start, we will have to convert an image from color with RGB to grayscale. We
    # will use the weights defined with by following equation
    # To ensure that we stay in the common 8-bit grayscale range we will use np.uint8 for all calculated
    # arrays.
    # Let’s take a look at our starting image for reference. Replacing the image is encouraged once the
    # example has been proven to work.
#   Fourth:
    # Choose a quantization level 𝐿 to your satisfaction and display your image
#
# Run instructions:
# 1. pip install -r requirements.txt
# 2. ./disassembler_assignment.py


def coordinate_calculations():
    print("=" * 100)
    print("Calculations in 64 bit accuracy")
    uccs_64 = np.array([38.8936117,-104.8005516, 1965.96])
    ucb_64 = np.array([40.0073943,-105.2662901, 1661.16])
    uccs_64_ecef = np.array([*geodetic2ecef(*uccs_64)])
    ucb_64_ecef = np.array([*geodetic2ecef(*ucb_64)])
    print(ucb_64_ecef)
    print(uccs_64_ecef)
    print(np.linalg.norm(uccs_64_ecef - ucb_64_ecef))
    print("=" * 100)
    print()

    print("=" * 100)
    print("Calculations in 32 bit accuracy")
    uccs_32 = uccs_64.astype(np.float32)
    ucb_32 = ucb_64.astype(np.float32)
    uccs_32_ecef = np.array([*geodetic2ecef(*uccs_32)])
    ucb_32_ecef = np.array([*geodetic2ecef(*ucb_32)])
    print(uccs_32_ecef)
    print(ucb_32_ecef)
    print(np.linalg.norm(uccs_32_ecef - ucb_32_ecef))
    print("=" * 100)
    print()

    print("=" * 100)
    print("Calculations in 16 bit accuracy")
    uccs_16 = uccs_32.astype(np.float16)
    ucb_16 = ucb_32.astype(np.float16)
    uccs_16_ecef = np.array([*geodetic2ecef(*uccs_16)])
    ucb_16_ecef = np.array([*geodetic2ecef(*ucb_16)])
    print(uccs_16_ecef)
    print(ucb_16_ecef)
    print(np.linalg.norm(uccs_16_ecef - ucb_16_ecef))
    print("=" * 100)
    print()


def main():
    coordinate_calculations()


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    from pymap3d.ecef import geodetic2ecef
    
    main()