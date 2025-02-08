# Image Processing Tools Documentation

This document provides a comprehensive overview of various image processing tools, their parameters, and detailed explanations of how each parameter affects the output. Each tool is categorized based on its functionality, and additional details such as access methods, parameter types, and constraints are provided.

---

## Table of Contents

1. [Adaptive Threshold Tool](#1-adaptive-threshold-tool)
2. [Bilateral Filter](#2-bilateral-filter)
3. [Black Hat Transform Tool](#3-black-hat-transform-tool)
4. [Brightness Adjustment](#4-brightness-adjustment)
5. [Canny Edge Detection](#5-canny-edge-detection)
6. [Cartoonize](#6-cartoonize)
7. [Closing](#7-closing)
8. [Color Balancing](#8-color-balancing)
9. [Contrast Adjustment](#9-contrast-adjustment)
10. [Darken Image](#10-darken-image)
11. [Dehaze](#11-dehaze)
12. [Dilation](#12-dilation)
13. [Emboss](#13-emboss)
14. [Erosion](#14-erosion)
15. [Exposure Adjustment](#15-exposure-adjustment)
16. [Fast Corner Detection](#16-fast-corner-detection)
17. [Flipping/Mirroring](#17-flippingmirroring)
18. [Gabor Filter](#18-gabor-filter)
19. [Gamma Correction](#19-gamma-correction)
20. [Gaussian Blur](#20-gaussian-blur)
21. [Gaussian Noise Reduction](#21-gaussian-noise-reduction)
22. [Glitch Effect](#22-glitch-effect)
23. [Gradient Tool](#23-gradient-tool)
24. [Grayscale Conversion](#24-grayscale-conversion)
25. [High Pass Filter](#25-high-pass-filter)
26. [Hough Transform Tool](#26-hough-transform-tool)
27. [Hue Adjustment](#27-hue-adjustment)
28. [Invert Colors](#28-invert-colors)
29. [Laplacian Edge Detection](#29-laplacian-edge-detection)
30. [Laplacian Sharpening](#30-laplacian-sharpening)
31. [LBP (Local Binary Patterns)](#31-lbp-local-binary-patterns)
32. [Median Blur](#32-median-blur)
33. [Non-Local Means Denoising](#33-non-local-means-denoising)
34. [Oil Paint](#34-oil-paint)
35. [Opening](#35-opening)
36. [ORB Feature Detection Tool](#36-orb-feature-detection-tool)
37. [Otsu Threshold Tool](#37-otsu-threshold-tool)
38. [Pencil Sketch](#38-pencil-sketch)
39. [Pixelation](#39-pixelation)
40. [Posterization](#40-posterization)
41. [Prewitt Operator](#41-prewitt-operator)
42. [Saturation Adjustment](#42-saturation-adjustment)
43. [Selective Color Replacement](#43-selective-color-replacement)
44. [Sepia Effect](#44-sepia-effect)
45. [SIFT Feature Detection](#45-sift-feature-detection)
46. [Sobel Filter](#46-sobel-filter)
47. [SURF Feature Detection](#47-surf-feature-detection)
48. [Threshold Tool](#48-threshold-tool)
49. [Top Hat Transform Tool](#49-top-hat-transform-tool)
50. [Unsharp Masking](#50-unsharp-masking)
51. [Vibrance Adjustment](#51-vibrance-adjustment)
52. [Wavelet Transform](#52-wavelet-transform)

---

### 1 Adaptive Threshold Tool
**Category**: Thresholding  
**Access**: `tools/adaptive_threshold_tool.py`  

#### Parameters:
- **max_value** (`int`): The maximum value to use with the thresholding operation. Typically ranges from 0 to 255.
- **block_size** (`int`): Size of the pixel neighborhood used to calculate the threshold value. Must be an odd integer.
- **c** (`float`): Constant subtracted from the mean or weighted mean. Can be positive or negative.
- **adaptive_method** (`str`): Method used to determine the threshold value. Options: `"mean"` or `"gaussian"`.
- **threshold_type** (`str`): Type of thresholding applied. Options: `"binary"`, `"binary_inv"`, etc.

---

### 2 Bilateral Filter
**Category**: Smoothing  
**Access**: `tools/bilateral_filter.py`  

#### Parameters:
- **d** (`int`): Diameter of each pixel neighborhood. Larger values increase smoothing.
- **sigma_color** (`float`): Filter sigma in the color space. Larger values smooth colors more aggressively.
- **sigma_space** (`float`): Filter sigma in the coordinate space. Controls spatial smoothing.

---

### 3 Black Hat Transform Tool
**Category**: Morphological Operations  
**Access**: `tools/black_hat_transform_tool.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the structuring element. Must be an odd integer.
- **kernel_shape** (`str`): Shape of the structuring element. Options: `"rect"`, `"ellipse"`, `"cross"`.

---

### 4 Brightness Adjustment
**Category**: Color Adjustments  
**Access**: `tools/brightness_adjustment.py`  

#### Parameters:
- **brightness** (`float`): Factor by which brightness is adjusted. Positive values increase brightness; negative values decrease it.

---

### 5 Canny Edge Detection
**Category**: Edge Detection  
**Access**: `tools/canny_edge_detection.py`  

#### Parameters:
- **threshold1** (`float`): Lower threshold for hysteresis procedure.
- **threshold2** (`float`): Upper threshold for hysteresis procedure.
- **aperture_size** (`int`): Aperture size for Sobel operator. Must be odd (e.g., 3, 5, 7).
- **l2gradient** (`bool`): Flag indicating whether to use L2-norm for gradient magnitude.

---

### 6 Cartoonize
**Category**: Artistic Effects  
**Access**: `tools/cartoonize.py`  

#### Parameters:
- **num_down** (`int`): Number of downsampling steps.
- **num_bilateral** (`int`): Number of bilateral filtering steps.
- **edge_threshold** (`float`): Threshold for edge detection.
- **color_reduce_levels** (`int`): Number of quantization levels for color reduction.

### Notes:
- **Parameter Types**: Ensure that all parameters match their expected data types (e.g., integers, floats, strings).
- **Constraints**: Some parameters have specific constraints (e.g., odd integers for kernel sizes).
- **Usage**: Each tool can be accessed via its respective Python module and initialized with the required parameters.

---

### 7 Closing
**Category**: Morphological Operations  
**Access**: `tools/closing.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the structuring element. Must be an odd integer.
- **kernel_shape** (`str`): Shape of the structuring element. Options: `"rect"`, `"ellipse"`, `"cross"`.

**Description**:  
Closing is a morphological operation that involves dilation followed by erosion. It is used to close small holes or gaps in the foreground objects, effectively smoothing the boundaries of objects while preserving their size.

---

### 8 Color Balancing
**Category**: Color Adjustments  
**Access**: `tools/color_balancing.py`  

#### Parameters:
- **red** (`float`): Red channel balance factor. Values > 1 increase red intensity; values < 1 decrease it.
- **green** (`float`): Green channel balance factor. Values > 1 increase green intensity; values < 1 decrease it.
- **blue** (`float`): Blue channel balance factor. Values > 1 increase blue intensity; values < 1 decrease it.

**Description**:  
Color balancing adjusts the intensity of the red, green, and blue channels independently. This tool is useful for correcting color casts or enhancing specific colors in an image.

---

### 9 Contrast Adjustment
**Category**: Color Adjustments  
**Access**: `tools/contrast_adjustment.py`  

#### Parameters:
- **contrast** (`float`): Factor by which contrast is adjusted. Values > 1 increase contrast; values < 1 decrease it.

**Description**:  
Contrast adjustment modifies the difference between the darkest and lightest areas of an image. Increasing contrast makes the image more vivid, while decreasing contrast softens the image.

---

### 10 Darken Image
**Category**: Color Adjustments  
**Access**: `tools/darken_image.py`  

#### Parameters:
- **amount** (`float`): Factor by which the image is darkened. Values between 0 and 1 reduce brightness.

**Description**:  
This tool reduces the overall brightness of an image by scaling the pixel values down by the specified amount. It is useful for creating moodier or darker images.

---

### 11 Dehaze
**Category**: Image Enhancement  
**Access**: `tools/dehaze.py`  

#### Parameters:
- **transmission_weight** (`float`): Weight factor for transmission estimation. Higher values emphasize haze removal.
- **attenuation_factor** (`float`): Controls the attenuation of light due to haze.
- **max_filter_size** (`int`): Maximum size of the filter used for transmission estimation.
- **omega** (`float`): Weighting factor for haze removal.
- **algorithm** (`str`): Algorithm used for dehazing. Options: `"dark_channel"`, `"guided_filter"`.

**Description**:  
Dehazing removes atmospheric effects like fog or haze from images, improving visibility and clarity. The tool uses advanced algorithms to estimate and remove haze based on the image's transmission map.

---

### 12 Dilation
**Category**: Morphological Operations  
**Access**: `tools/dilation.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the structuring element. Must be an odd integer.
- **kernel_shape** (`str`): Shape of the structuring element. Options: `"rect"`, `"ellipse"`, `"cross"`.

**Description**:  
Dilation expands the boundaries of foreground objects in an image. It is often used to fill gaps, connect broken parts, or enlarge objects.

---

### 13 Emboss
**Category**: Artistic Effects  
**Access**: `tools/emboss.py`  

#### Parameters:
- **emboss_angle** (`float`): Angle of the emboss effect in degrees.
- **emboss_depth** (`float`): Depth of the emboss effect. Higher values create a more pronounced 3D effect.
- **background_gray** (`float`): Gray level of the background. Typically ranges from 0 (black) to 255 (white).

**Description**:  
Emboss creates a 3D effect by highlighting edges and giving the impression of depth. The angle and depth parameters control the direction and intensity of the embossing.

---

### 14 Erosion
**Category**: Morphological Operations  
**Access**: `tools/erosion.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the structuring element. Must be an odd integer.
- **kernel_shape** (`str`): Shape of the structuring element. Options: `"rect"`, `"ellipse"`, `"cross"`.

**Description**:  
Erosion shrinks the boundaries of foreground objects in an image. It is commonly used to remove small noise or thin out objects.

---

### 15 Exposure Adjustment
**Category**: Color Adjustments  
**Access**: `tools/exposure_adjustment.py`  

#### Parameters:
- **exposure** (`float`): Factor by which exposure is adjusted. Values > 1 increase exposure; values < 1 decrease it.

**Description**:  
Exposure adjustment simulates the effect of changing the camera's exposure settings. Increasing exposure brightens the image, while decreasing exposure darkens it.

---

### 16 Fast Corner Detection
**Category**: Feature Detection  
**Access**: `tools/fast_corner_detection.py`  

#### Parameters:
- **threshold** (`int`): Threshold for detecting corners. Higher values result in fewer corners being detected.
- **non_max_suppression** (`bool`): Whether to apply non-maximum suppression to refine corner locations.
- **feature_type** (`str`): Type of features to detect. Options: `"corner"`, `"edge"`.

**Description**:  
FAST (Features from Accelerated Segment Test) is a corner detection algorithm that identifies keypoints in an image. It is computationally efficient and widely used in real-time applications.

---

### 17 Flipping/Mirroring
**Category**: Geometric Transformations  
**Access**: `tools/flipping_mirroring.py`  

#### Parameters:
- **flip_code** (`int`): Specifies how to flip the image.  
  - `0`: Flip vertically (around the x-axis).
  - `1`: Flip horizontally (around the y-axis).
  - `-1`: Flip both vertically and horizontally.

**Description**:  
Flipping or mirroring reverses the image along one or both axes. This is useful for data augmentation, symmetry analysis, or artistic effects.

---

### 18 Gabor Filter
**Category**: Filtering  
**Access**: `tools/gabor_filter.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the Gabor kernel. Must be an odd integer.
- **sigma** (`float`): Standard deviation of the Gaussian envelope.
- **theta** (`float`): Orientation of the normal to the parallel stripes of the Gabor function.
- **lambda** (`float`): Wavelength of the sinusoidal factor.
- **gamma** (`float`): Spatial aspect ratio.
- **psi** (`float`): Phase offset.

**Description**:  
Gabor filters are used for texture analysis and edge detection. They are particularly effective at capturing local patterns and orientations in an image.

---

### 19 Gamma Correction
**Category**: Color Adjustments  
**Access**: `tools/gamma_correction.py`  

#### Parameters:
- **gamma** (`float`): Gamma correction factor. Values < 1 brighten the image; values > 1 darken it.

**Description**:  
Gamma correction adjusts the brightness of an image by applying a non-linear transformation to the pixel values. It is commonly used to correct brightness imbalances caused by different display devices.

---

### 20 Gaussian Blur
**Category**: Smoothing  
**Access**: `tools/gaussian_blur.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the Gaussian kernel. Must be an odd integer.
- **sigma** (`float`): Standard deviation of the Gaussian kernel.

**Description**:  
Gaussian blur applies a low-pass filter to smooth an image. It reduces noise and detail while preserving edges better than uniform blurring.

---

### 21 Gaussian Noise Reduction
**Category**: Denoising  
**Access**: `tools/gaussian_noise_reduction.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the Gaussian kernel. Must be an odd integer.
- **sigma_x** (`float`): Standard deviation in the X direction.
- **sigma_y** (`float`): Standard deviation in the Y direction.

**Description**:  
This tool reduces Gaussian noise in an image by applying a Gaussian filter. It is effective for removing random noise while retaining important features.

---

### 22 Glitch Effect
**Category**: Artistic Effects  
**Access**: `tools/glitch_effect.py`  

#### Parameters:
- **glitch_intensity** (`float`): Intensity of the glitch effect. Higher values create more pronounced glitches.
- **channel_shift** (`int`): Number of pixels to shift color channels. Creates RGB misalignment.
- **seed** (`int`): Random seed for reproducibility of the glitch effect.
- **glitch_type** (`str`): Type of glitch effect. Options: `"random"`, `"blocky"`, `"wave"`.
- **block_size** (`int`): Size of blocks used in blocky glitches.

**Description**:  
The glitch effect creates a distorted, digital-art-style appearance by manipulating pixel values and shifting color channels. It is often used for artistic or retro effects.

---

### 23 Gradient Tool
**Category**: Edge Detection  
**Access**: `tools/gradient_tool.py`  

#### Parameters:
- **gradient_type** (`str`): Type of gradient to compute. Options: `"sobel"`, `"scharr"`, `"prewitt"`.
- **kernel_size** (`int`): Size of the kernel used for gradient computation. Must be an odd integer.
- **direction** (`str`): Direction of the gradient. Options: `"horizontal"`, `"vertical"`, `"both"`.

**Description**:  
The gradient tool computes the gradient magnitude of an image, highlighting edges and transitions between regions of different intensities. Different gradient types emphasize different edge properties.

---

### 24 Grayscale Conversion
**Category**: Color Adjustments  
**Access**: `tools/grayscale_conversion.py`  

#### Parameters:
- **weights** (`list`): Weights for RGB channels in grayscale conversion. Default: `[0.299, 0.587, 0.114]`.

**Description**:  
Grayscale conversion transforms a color image into a single-channel grayscale image. The weights parameter allows customization of how much each color channel contributes to the final grayscale value.

---

### 25 High Pass Filter
**Category**: Filtering  
**Access**: `tools/high_pass_filter.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the high-pass filter kernel. Must be an odd integer.
- **sigma** (`float`): Standard deviation of the Gaussian kernel used for high-pass filtering.

**Description**:  
A high-pass filter emphasizes edges and fine details by removing low-frequency components from the image. It is useful for sharpening or detecting edges.

---

### 26 Hough Transform Tool
**Category**: Feature Detection  
**Access**: `tools/hough_transform_tool.py`  

#### Parameters:
- **transform_type** (`str`): Type of Hough transform. Options: `"lines"`, `"circles"`.
- **threshold** (`int`): Accumulator threshold for detecting lines or circles.
- **rho** (`float`): Distance resolution of the accumulator in pixels (for lines).
- **theta** (`float`): Angle resolution of the accumulator in radians (for lines).
- **min_line_length** (`float`): Minimum length of detected lines.
- **max_line_gap** (`float`): Maximum gap between line segments to treat them as a single line.
- **dp** (`float`): Inverse ratio of the accumulator resolution to the image resolution (for circles).
- **min_dist** (`float`): Minimum distance between detected circle centers.
- **param1** (`float`): Upper threshold for edge detection (for circles).
- **param2** (`float`): Accumulator threshold for circle detection.
- **min_radius** (`int`): Minimum radius of detected circles.
- **max_radius** (`int`): Maximum radius of detected circles.

**Description**:  
The Hough transform detects geometric shapes like lines or circles in an image. It is widely used in applications such as lane detection, object recognition, and shape analysis.

---

### 27 Hue Adjustment
**Category**: Color Adjustments  
**Access**: `tools/hue_adjustment.py`  

#### Parameters:
- **hue_shift** (`float`): Amount to shift the hue in degrees. Ranges from -180 to 180.

**Description**:  
Hue adjustment modifies the color tone of an image by rotating the hue values in the HSV color space. This tool is useful for color correction or creating artistic effects.

---

### 28 Invert Colors
**Category**: Color Adjustments  
**Access**: `tools/invert_colors.py`  

#### Parameters:
- **strength** (`float`): Strength of the inversion effect. Values range from 0 to 1.

**Description**:  
Inverting colors reverses the intensity of each pixel, creating a negative-like effect. This tool is often used for artistic purposes or to enhance contrast.

---

### 29 Laplacian Edge Detection
**Category**: Edge Detection  
**Access**: `tools/laplacian_edge_detection.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the Laplacian kernel. Must be an odd integer.
- **scale** (`float`): Scaling factor for the Laplacian operator.
- **delta** (`float`): Offset added to the result.

**Description**:  
Laplacian edge detection highlights regions of rapid intensity change, emphasizing edges and fine details. It is sensitive to noise, so smoothing is often applied beforehand.

---

### 30 Laplacian Sharpening
**Category**: Sharpening  
**Access**: `tools/laplacian_sharpening.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the Laplacian kernel. Must be an odd integer.
- **scale** (`float`): Scaling factor for the Laplacian operator.

**Description**:  
Laplacian sharpening enhances edges and fine details by applying a Laplacian filter and adding the result back to the original image. It is commonly used for image enhancement.

---

### 31 LBP (Local Binary Patterns)
**Category**: Texture Analysis  
**Access**: `tools/lbp.py`  

#### Parameters:
- **radius** (`int`): Radius of the circular neighborhood.
- **n_points** (`int`): Number of points in the circular neighborhood.
- **method** (`str`): Method for computing LBP. Options: `"default"`, `"uniform"`, `"nri_uniform"`.

**Description**:  
LBP is a texture descriptor that captures local patterns in an image. It is widely used in applications like face recognition, texture classification, and object detection.

---

### 32 Median Blur
**Category**: Smoothing  
**Access**: `tools/median_blur.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the median filter kernel. Must be an odd integer.

**Description**:  
Median blur replaces each pixel with the median value of its neighborhood, effectively removing noise while preserving edges. It is particularly effective at reducing salt-and-pepper noise.

---

### 33 Non-Local Means Denoising
**Category**: Denoising  
**Access**: `tools/non_local_means_denoising.py`  

#### Parameters:
- **h** (`float`): Parameter controlling the strength of denoising.
- **template_window_size** (`int`): Size of the template window.
- **search_window_size** (`int`): Size of the search window.

**Description**:  
Non-local means denoising removes noise by averaging similar patches across the image. It preserves fine details and textures better than traditional denoising methods.

---

### 34 Oil Paint
**Category**: Artistic Effects  
**Access**: `tools/oil_paint.py`  

#### Parameters:
- **brush_size** (`int`): Size of the brush used for painting.
- **color_levels** (`int`): Number of quantization levels for color reduction.
- **smooth_factor** (`float`): Factor for smoothing the image before applying the effect.

**Description**:  
The oil paint effect simulates the appearance of an oil painting by reducing color levels and applying a brush-like texture. It is often used for artistic rendering.

---

### 35 Opening
**Category**: Morphological Operations  
**Access**: `tools/opening.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the structuring element. Must be an odd integer.
- **kernel_shape** (`str`): Shape of the structuring element. Options: `"rect"`, `"ellipse"`, `"cross"`.

**Description**:  
Opening is a morphological operation that involves erosion followed by dilation. It is used to remove small objects or noise while preserving the overall structure of larger objects.

---

### 36 ORB Feature Detection Tool
**Category**: Feature Detection  
**Access**: `tools/orb_feature_detection_tool.py`  

#### Parameters:
- **n_features** (`int`): Maximum number of features to detect.
- **scale_factor** (`float`): Factor between pyramid scales.
- **n_levels** (`int`): Number of pyramid levels.
- **edge_threshold** (`int`): Threshold for edge detection.
- **first_level** (`int`): Level of the first image pyramid.
- **wta_k** (`int`): Number of points considered for each feature.
- **score_type** (`str`): Type of score used for feature evaluation. Options: `"harris"`, `"fast"`.
- **patch_size** (`int`): Size of the patch used for feature description.
- **fast_threshold** (`int`): Threshold for FAST corner detection.

**Description**:  
ORB (Oriented FAST and Rotated BRIEF) is a fast and efficient feature detection and description algorithm. It is widely used in real-time applications like object tracking and augmented reality.

---

### 37 Otsu Threshold Tool
**Category**: Thresholding  
**Access**: `tools/otsu_threshold_tool.py`  

#### Parameters:
- **max_value** (`int`): Maximum value to use with the thresholding operation.

**Description**:  
Otsu's method automatically determines the optimal threshold for separating foreground and background based on the histogram of the image. It is particularly effective for bimodal images.

---

### 38 Pencil Sketch
**Category**: Artistic Effects  
**Access**: `tools/pencil_sketch.py`  

#### Parameters:
- **sketch_mode** (`str`): Mode of sketching. Options: `"grayscale"`, `"color"`.
- **sigma_s** (`float`): Spatial standard deviation for bilateral filtering.
- **sigma_r** (`float`): Range standard deviation for bilateral filtering.
- **edge_threshold** (`float`): Threshold for edge detection.
- **shade_factor** (`float`): Factor for shading intensity.

**Description**:  
The pencil sketch effect simulates the appearance of a hand-drawn sketch by enhancing edges and reducing color levels. It is often used for artistic rendering.

---

### 39 Pixelation
**Category**: Artistic Effects  
**Access**: `tools/pixelation.py`  

#### Parameters:
- **pixel_size** (`int`): Size of each pixel block.
- **scale_factor** (`float`): Factor for scaling the image before pixelation.

**Description**:  
Pixelation reduces the resolution of an image by grouping pixels into larger blocks. It is often used for anonymizing faces or creating retro-style effects.

---

### 40 Posterization
**Category**: Color Adjustments  
**Access**: `tools/posterization.py`  

#### Parameters:
- **levels** (`int`): Number of quantization levels for each color channel.

**Description**:  
Posterization reduces the number of colors in an image, creating a flat, cartoon-like appearance. It is often used for artistic effects or simplifying images.

---

### 41 Prewitt Operator
**Category**: Edge Detection  
**Access**: `tools/prewitt_operator.py`  

#### Parameters:
- **direction** (`str`): Direction of the gradient. Options: `"horizontal"`, `"vertical"`.
- **scale** (`float`): Scaling factor for the Prewitt operator.

**Description**:  
The Prewitt operator detects edges by computing the gradient magnitude using convolution kernels. It is less sensitive to noise compared to other edge detectors.

---

### 42 Saturation Adjustment
**Category**: Color Adjustments  
**Access**: `tools/saturation_adjustment.py`  

#### Parameters:
- **saturation** (`float`): Factor by which saturation is adjusted. Values > 1 increase saturation; values < 1 decrease it.

**Description**:  
Saturation adjustment modifies the intensity of colors in an image. Increasing saturation makes colors more vivid, while decreasing saturation desaturates the image.

---

### 43 Selective Color Replacement
**Category**: Color Adjustments  
**Access**: `tools/selective_color_replacement.py`  

#### Parameters:
- **target_color** (`tuple`): RGB value of the target color to replace.
- **replacement_color** (`tuple`): RGB value of the replacement color.
- **tolerance** (`int`): Tolerance for matching the target color.

**Description**:  
Selective color replacement changes specific colors in an image while leaving others unchanged. It is useful for recoloring objects or correcting color imbalances.

---

### 44 Sepia Effect
**Category**: Artistic Effects  
**Access**: `tools/sepia_effect.py`  

#### Parameters:
- **intensity** (`float`): Intensity of the sepia effect. Values range from 0 to 1.

**Description**:  
The sepia effect gives an image a warm, vintage appearance by applying a brownish tint. It is often used for historical or nostalgic effects.

---

### 45 SIFT Feature Detection
**Category**: Feature Detection  
**Access**: `tools/sift_feature_detection.py`  

#### Parameters:
- **n_features** (`int`): Maximum number of features to detect.
- **n_octave_layers** (`int`): Number of layers per octave.
- **contrast_threshold** (`float`): Threshold for contrast-based feature detection.
- **edge_threshold** (`float`): Threshold for edge-based feature detection.
- **sigma** (`float`): Sigma for Gaussian blurring.

**Description**:  
SIFT (Scale-Invariant Feature Transform) detects and describes keypoints that are invariant to scale, rotation, and illumination changes. It is widely used in computer vision tasks.

---

### 46 Sobel Filter
**Category**: Edge Detection  
**Access**: `tools/sobel_filter.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the Sobel kernel. Must be an odd integer.
- **dx** (`int`): Order of the derivative in the x-direction.
- **dy** (`int`): Order of the derivative in the y-direction.
- **scale** (`float`): Scaling factor for the Sobel operator.

**Description**:  
The Sobel filter detects edges by computing the gradient magnitude using convolution kernels. It is widely used for edge detection and image sharpening.

---

### 47 SURF Feature Detection
**Category**: Feature Detection  
**Access**: `tools/surf_feature_detection.py`  

#### Parameters:
- **hessian_threshold** (`float`): Threshold for keypoint detection.
- **n_octaves** (`int`): Number of octaves.
- **n_octave_layers** (`int`): Number of layers per octave.
- **extended** (`bool`): Whether to use the extended descriptor.
- **upright** (`bool`): Whether to compute upright descriptors.

**Description**:  
SURF (Speeded-Up Robust Features) is a fast and robust feature detection and description algorithm. It is widely used in applications like object recognition and 3D reconstruction.

---

### 48 Threshold Tool
**Category**: Thresholding  
**Access**: `tools/threshold_tool.py`  

#### Parameters:
- **threshold** (`float`): Threshold value for binarization.
- **max_value** (`int`): Maximum value to use with the thresholding operation.
- **threshold_type** (`str`): Type of thresholding applied. Options: `"binary"`, `"binary_inv"`, etc.

**Description**:  
Thresholding converts a grayscale image into a binary image by setting pixel values above or below a threshold to specified values. It is widely used for segmentation.

---

### 49 Top Hat Transform Tool
**Category**: Morphological Operations  
**Access**: `tools/top_hat_transform_tool.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the structuring element. Must be an odd integer.
- **kernel_shape** (`str`): Shape of the structuring element. Options: `"rect"`, `"ellipse"`, `"cross"`.

**Description**:  
Top hat transform highlights small objects or details that are brighter than their surroundings. It is often used for feature extraction or noise removal.

---

### 50 Unsharp Masking
**Category**: Sharpening  
**Access**: `tools/unsharp_masking.py`  

#### Parameters:
- **kernel_size** (`int`): Size of the Gaussian kernel. Must be an odd integer.
- **amount** (`float`): Strength of the sharpening effect.
- **threshold** (`float`): Threshold for sharpening.

**Description**:  
Unsharp masking enhances edges by subtracting a blurred version of the image from the original. It is widely used for image sharpening.

---

### 51 Vibrance Adjustment
**Category**: Color Adjustments  
**Access**: `tools/vibrance_adjustment.py`  

#### Parameters:
- **vibrance** (`float`): Factor by which vibrance is adjusted. Values > 1 increase vibrance; values < 1 decrease it.

**Description**:  
Vibrance adjustment selectively increases the intensity of muted colors while leaving already saturated colors unchanged. It is often used for enhancing natural-looking images.

---

### 52 Wavelet Transform
**Category**: Filtering  
**Access**: `tools/wavelet_transform.py`  

#### Parameters:
- **wavelet** (`str`): Type of wavelet to use. Options: `"haar"`, `"db1"`, `"sym2"`, etc.
- **level** (`int`): Number of decomposition levels.
- **mode** (`str`): Mode for wavelet transform. Options: `"symmetric"`, `"periodic"`, etc.

**Description**:  
Wavelet transform decomposes an image into different frequency components, enabling multi-resolution analysis. It is widely used for compression, denoising, and feature extraction.

