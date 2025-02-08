# tools/tool_manager.py
from enum import Enum
from typing import List, Dict, Type

# Import all tools
from tools.bilateral_filter import BilateralFilterTool
from tools.brightness_adjustment import BrightnessAdjustmentTool
from tools.canny_edge_detection import CannyEdgeDetectionTool
from tools.closing import ClosingTool
from tools.color_balancing import ColorBalancingTool
from tools.contrast_adjustment import ContrastAdjustmentTool
from tools.darken_image import DarkenImageTool
from tools.dilation import DilationTool
from tools.erosion import ErosionTool
from tools.exposure_adjustment import ExposureAdjustmentTool
from tools.flipping_mirroring import FlippingMirroringTool
from tools.gamma_correction import GammaCorrectionTool
from tools.gaussian_blur import GaussianBlurTool
from tools.gaussian_noise_reduction import GaussianNoiseReductionTool
from tools.grayscale_conversion import GrayscaleConversionTool
from tools.high_pass_filter import HighPassFilterTool
from tools.hue_adjustment import HueAdjustmentTool
from tools.invert_colors import InvertColorsTool
from tools.laplacian_edge_detection import LaplacianEdgeDetectionTool
from tools.laplacian_sharpening import LaplacianSharpeningTool
from tools.median_blur import MedianBlurTool
from tools.non_local_means_denoising import NonLocalMeansDenoisingTool
from tools.opening import OpeningTool
from tools.orb_feature_detection import ORBFeatureDetectionTool
from tools.otsu_threshold import OtsuThresholdTool
from tools.posterization import PosterizationTool
from tools.prewitt_operator import PrewittOperatorTool
from tools.saturation_adjustment import SaturationAdjustmentTool
from tools.selective_color_replacement import SelectiveColorReplacementTool
from tools.sepia_effect import SepiaEffectTool
from tools.threshold_tool import SimpleThresholdTool
from tools.adaptive_threshold import AdaptiveThresholdTool
from tools.sobel_filter import SobelFilterTool
from tools.top_hat_transform import TopHatTransformTool
from tools.black_hat_transform import BlackHatTransformTool
from tools.hough_transform import HoughTransformTool
from tools.unsharp_masking import UnsharpMaskingTool
from tools.vibrance_adjustment import VibranceAdjustmentTool
from tools.wavelet_transform import WaveletTransformTool
from tools.surf_feature_detection import SURFFeatureDetectionTool
from tools.sift_feature_detection import SIFTFeatureDetectionTool
from tools.pixelation import PixelationTool
from tools.pencil_sketch import PencilSketchTool
from tools.oil_paint import OilPaintingTool
from tools.lbp import LBPTool
from tools.glitch_effect import GlitchEffectTool
from tools.gabor_filter import GaborFilterTool
from tools.fast_corner_detection import FASTCornerDetectionTool
from tools.emboss import EmbossingTool
from tools.dehaze import DehazingTool
from tools.cartoonize import CartoonizationTool

class ToolCategory(str, Enum):
    ADJUSTMENT = "Adjustment"
    FILTER = "Filter"
    EDGE_DETECTION = "Edge Detection"
    NOISE_REDUCTION = "Noise Reduction"
    MORPHOLOGICAL = "Morphological"
    COLOR = "Color"
    EFFECT = "Effect"
    FEATURE_DETECTION = "Feature Detection"
    THRESHOLD = "Threshold"
    TRANSFORM = "Transform"
    ARTISTIC = "Artistic"
    TEXTURE = "Texture"

class ToolManager:
    def __init__(self):
        # Define tool categories mapping
        self.tool_categories: Dict[str, ToolCategory] = {
            # Adjustment Tools
            "BrightnessAdjustment": ToolCategory.ADJUSTMENT,
            "ContrastAdjustment": ToolCategory.ADJUSTMENT,
            "ExposureAdjustment": ToolCategory.ADJUSTMENT,
            "GammaCorrection": ToolCategory.ADJUSTMENT,
            "VibranceAdjustment": ToolCategory.ADJUSTMENT,

            # Feature Detection
            "SURFFeatureDetection": ToolCategory.FEATURE_DETECTION,
            "SIFTFeatureDetection": ToolCategory.FEATURE_DETECTION,
            "FASTCornerDetection": ToolCategory.FEATURE_DETECTION,
            
            # Filter Tools
            "BilateralFilter": ToolCategory.FILTER,
            "GaussianBlur": ToolCategory.FILTER,
            "MedianBlur": ToolCategory.FILTER,
            "SobelFilter": ToolCategory.FILTER,
            "UnsharpMasking": ToolCategory.FILTER,
            "HighPassFilter": ToolCategory.FILTER,
            "GaborFilter": ToolCategory.FILTER,
            
            # Edge Detection Tools
            "CannyEdgeDetection": ToolCategory.EDGE_DETECTION,
            "LaplacianEdgeDetection": ToolCategory.EDGE_DETECTION,
            "PrewittOperator": ToolCategory.EDGE_DETECTION,
            
            # Noise Reduction Tools
            "GaussianNoiseReduction": ToolCategory.NOISE_REDUCTION,
            "NonLocalMeansDenoising": ToolCategory.NOISE_REDUCTION,
            
            # Morphological Tools
            "Closing": ToolCategory.MORPHOLOGICAL,
            "Dilation": ToolCategory.MORPHOLOGICAL,
            "Erosion": ToolCategory.MORPHOLOGICAL,
            "Opening": ToolCategory.MORPHOLOGICAL,
            "TopHatTransform": ToolCategory.MORPHOLOGICAL,
            "BlackHatTransform": ToolCategory.MORPHOLOGICAL,
            
            # Color Tools
            "ColorBalancing": ToolCategory.COLOR,
            "GrayscaleConversion": ToolCategory.COLOR,
            "HueAdjustment": ToolCategory.COLOR,
            "InvertColors": ToolCategory.COLOR,
            "SaturationAdjustment": ToolCategory.COLOR,
            "SelectiveColorReplacement": ToolCategory.COLOR,
            
            # Effect Tools
            "DarkenImage": ToolCategory.EFFECT,
            "FlippingMirroring": ToolCategory.EFFECT,
            "LaplacianSharpening": ToolCategory.EFFECT,
            "Posterization": ToolCategory.EFFECT,
            "SepiaEffect": ToolCategory.EFFECT,
            "GlitchEffect": ToolCategory.EFFECT,
            "Dehazing": ToolCategory.EFFECT,

            # Feature Detection Tools
            "ORBFeatureDetection": ToolCategory.FEATURE_DETECTION,
            "HoughTransform": ToolCategory.FEATURE_DETECTION,

            # Threshold Tools
            "SimpleThreshold": ToolCategory.THRESHOLD,
            "AdaptiveThreshold": ToolCategory.THRESHOLD,
            "OtsuThreshold": ToolCategory.THRESHOLD,

            # Artistic Effects
            "Pixelation": ToolCategory.ARTISTIC,
            "PencilSketch": ToolCategory.ARTISTIC,
            "OilPainting": ToolCategory.ARTISTIC,
            "Cartoonization": ToolCategory.ARTISTIC,
            "Embossing": ToolCategory.ARTISTIC,

            # Transform Tools
            "WaveletTransform": ToolCategory.TRANSFORM,

            # Texture Tools 
            "LBP": ToolCategory.TEXTURE,
        }

        # Define tool class mapping
        self.tools: Dict[str, Type] = {
            # Filtering & Noise Reduction
            "BilateralFilter": BilateralFilterTool,
            "GaussianBlur": GaussianBlurTool,
            "MedianBlur": MedianBlurTool,
            "GaussianNoiseReduction": GaussianNoiseReductionTool,
            "NonLocalMeansDenoising": NonLocalMeansDenoisingTool,
            "WaveletTransform": WaveletTransformTool,
            "GaborFilter": GaborFilterTool,

            # Image Enhancement & Adjustment
            "BrightnessAdjustment": BrightnessAdjustmentTool,
            "ContrastAdjustment": ContrastAdjustmentTool,
            "ExposureAdjustment": ExposureAdjustmentTool,
            "GammaCorrection": GammaCorrectionTool,
            "HueAdjustment": HueAdjustmentTool,
            "SaturationAdjustment": SaturationAdjustmentTool,
            "VibranceAdjustment": VibranceAdjustmentTool,
            "ColorBalancing": ColorBalancingTool,
            "DarkenImage": DarkenImageTool,

            # Edge Detection & Feature Detection
            "CannyEdgeDetection": CannyEdgeDetectionTool,
            "LaplacianEdgeDetection": LaplacianEdgeDetectionTool,
            "PrewittOperator": PrewittOperatorTool,
            "SobelFilter": SobelFilterTool,
            "FASTCornerDetection": FASTCornerDetectionTool,
            "ORBFeatureDetection": ORBFeatureDetectionTool,
            "SURFFeatureDetection": SURFFeatureDetectionTool,
            "SIFTFeatureDetection": SIFTFeatureDetectionTool,

            # Morphological Operations
            "Erosion": ErosionTool,
            "Dilation": DilationTool,
            "Opening": OpeningTool,
            "Closing": ClosingTool,
            "TopHatTransform": TopHatTransformTool,
            "BlackHatTransform": BlackHatTransformTool,

            # Thresholding & Binarization
            "OtsuThreshold": OtsuThresholdTool,
            "SimpleThreshold": SimpleThresholdTool,
            "AdaptiveThreshold": AdaptiveThresholdTool,

            # Artistic & Stylization Effects
            "SepiaEffect": SepiaEffectTool,
            "PencilSketch": PencilSketchTool,
            "OilPainting": OilPaintingTool,
            "Cartoonization": CartoonizationTool,
            "GlitchEffect": GlitchEffectTool,
            "Pixelation": PixelationTool,
            "Embossing": EmbossingTool,

            # Color & Transformation Effects
            "InvertColors": InvertColorsTool,
            "SelectiveColorReplacement": SelectiveColorReplacementTool,
            "Posterization": PosterizationTool,

            # Image Sharpening & High-Frequency Filtering
            "LaplacianSharpening": LaplacianSharpeningTool,
            "UnsharpMasking": UnsharpMaskingTool,
            "HighPassFilter": HighPassFilterTool,

            # Image Transformation
            "FlippingMirroring": FlippingMirroringTool,
            "HoughTransform": HoughTransformTool,
            "Dehazing": DehazingTool,

            # Texture & Feature Analysis
            "LBP": LBPTool,
        }

    def get_available_tools(self) -> List[str]:
        """Returns a list of all available tool names."""
        return list(self.tools.keys())

    def get_tool(self, name: str):
        """Creates and returns an instance of the specified tool."""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        try:
            return self.tools[name]()
        except Exception as e:
            raise RuntimeError(f"Error creating tool {name}: {str(e)}")

    def get_tools_by_category(self, category: ToolCategory) -> List[str]:
        """Returns a list of tool names belonging to the specified category."""
        return [
            tool_name
            for tool_name, tool_category in self.tool_categories.items()
            if tool_category == category
        ]

    def get_tool_category(self, tool_name: str) -> ToolCategory:
        """Returns the category of the specified tool."""
        if tool_name not in self.tool_categories:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self.tool_categories[tool_name]

    def get_all_categories(self) -> List[ToolCategory]:
        """Returns a list of all available tool categories."""
        return list(set(self.tool_categories.values()))