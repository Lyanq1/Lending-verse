"""
Document preprocessing module for OCR and document verification.
"""

import cv2
import numpy as np
import os
from PIL import Image
import logging
from typing import Tuple, Optional, List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentPreprocessor:
    """
    Class for preprocessing document images for OCR.
    """
    
    def __init__(self, output_dir: str = 'processed_images'):
        """
        Initialize the document preprocessor.
        
        Args:
            output_dir (str): Directory to save processed images
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load an image from file.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            np.ndarray: Loaded image
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image from {image_path}")
            return image
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise
    
    def save_image(self, image: np.ndarray, filename: str) -> str:
        """
        Save a processed image.
        
        Args:
            image (np.ndarray): Image to save
            filename (str): Output filename
            
        Returns:
            str: Path to saved image
        """
        output_path = os.path.join(self.output_dir, filename)
        cv2.imwrite(output_path, image)
        return output_path
    
    def resize_image(self, image: np.ndarray, target_dpi: int = 300) -> np.ndarray:
        """
        Resize image to a target DPI.
        
        Args:
            image (np.ndarray): Input image
            target_dpi (int): Target DPI
            
        Returns:
            np.ndarray: Resized image
        """
        # For simplicity, we'll assume the image needs to be scaled up
        # In a real implementation, you would calculate the actual DPI
        height, width = image.shape[:2]
        scale_factor = target_dpi / 72  # Assuming source is 72 DPI
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        return resized
    
    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Convert image to grayscale.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Grayscale image
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    def denoise_image(self, image: np.ndarray) -> np.ndarray:
        """
        Remove noise from image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Denoised image
        """
        return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
    
    def adjust_contrast(self, image: np.ndarray, alpha: float = 1.5, beta: int = 0) -> np.ndarray:
        """
        Adjust image contrast.
        
        Args:
            image (np.ndarray): Input image
            alpha (float): Contrast control (1.0-3.0)
            beta (int): Brightness control (0-100)
            
        Returns:
            np.ndarray: Contrast-adjusted image
        """
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    def threshold_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply adaptive thresholding to image.
        
        Args:
            image (np.ndarray): Input grayscale image
            
        Returns:
            np.ndarray: Thresholded image
        """
        return cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    
    def deskew_image(self, image: np.ndarray) -> np.ndarray:
        """
        Deskew image to straighten text.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Deskewed image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Calculate skew angle
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        # Adjust angle
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Rotate image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    def remove_borders(self, image: np.ndarray) -> np.ndarray:
        """
        Remove borders from image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Image with borders removed
        """
        gray = self.convert_to_grayscale(image)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find largest contour (assumed to be the document)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Crop to content area with a small margin
            margin = 10
            x = max(0, x - margin)
            y = max(0, y - margin)
            w = min(gray.shape[1] - x, w + 2 * margin)
            h = min(gray.shape[0] - y, h + 2 * margin)
            
            return image[y:y+h, x:x+w]
        
        return image
    
    def detect_and_correct_perspective(self, image: np.ndarray) -> np.ndarray:
        """
        Detect and correct document perspective.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Perspective-corrected image
        """
        # Convert to grayscale
        gray = self.convert_to_grayscale(image)
        
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply edge detection
        edges = cv2.Canny(blur, 75, 200)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Find the largest 4-sided contour (assumed to be the document)
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            if len(approx) == 4:
                # Found the document contour
                points = approx.reshape(4, 2)
                
                # Order points: top-left, top-right, bottom-right, bottom-left
                rect = np.zeros((4, 2), dtype="float32")
                
                # Top-left has smallest sum, bottom-right has largest sum
                s = points.sum(axis=1)
                rect[0] = points[np.argmin(s)]
                rect[2] = points[np.argmax(s)]
                
                # Top-right has smallest difference, bottom-left has largest difference
                diff = np.diff(points, axis=1)
                rect[1] = points[np.argmin(diff)]
                rect[3] = points[np.argmax(diff)]
                
                # Calculate width and height of the new image
                (tl, tr, br, bl) = rect
                widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                maxWidth = max(int(widthA), int(widthB))
                
                heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                maxHeight = max(int(heightA), int(heightB))
                
                # Create destination points
                dst = np.array([
                    [0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]
                ], dtype="float32")
                
                # Calculate perspective transform matrix
                M = cv2.getPerspectiveTransform(rect, dst)
                
                # Apply perspective transformation
                warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
                
                return warped
        
        # If no suitable contour found, return original image
        return image
    
    def process_image(self, image_path: str, output_filename: Optional[str] = None) -> Tuple[np.ndarray, str]:
        """
        Apply full preprocessing pipeline to an image.
        
        Args:
            image_path (str): Path to the input image
            output_filename (str, optional): Output filename
            
        Returns:
            Tuple[np.ndarray, str]: Processed image and path to saved image
        """
        logger.info(f"Processing image: {image_path}")
        
        try:
            # Load image
            image = self.load_image(image_path)
            
            # Generate output filename if not provided
            if output_filename is None:
                base_name = os.path.basename(image_path)
                name, ext = os.path.splitext(base_name)
                output_filename = f"{name}_processed{ext}"
            
            # Apply preprocessing steps
            # 1. Detect and correct perspective
            image = self.detect_and_correct_perspective(image)
            
            # 2. Resize to target DPI
            image = self.resize_image(image, target_dpi=300)
            
            # 3. Convert to grayscale
            image = self.convert_to_grayscale(image)
            
            # 4. Denoise
            image = self.denoise_image(image)
            
            # 5. Adjust contrast
            image = self.adjust_contrast(image, alpha=1.5, beta=10)
            
            # 6. Apply thresholding
            image = self.threshold_image(image)
            
            # 7. Deskew
            image = self.deskew_image(image)
            
            # Save processed image
            output_path = self.save_image(image, output_filename)
            
            logger.info(f"Image processed successfully: {output_path}")
            
            return image, output_path
        
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise
    
    def process_pdf(self, pdf_path: str, output_dir: Optional[str] = None) -> List[str]:
        """
        Extract and process images from a PDF.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str, optional): Output directory for processed images
            
        Returns:
            List[str]: Paths to processed images
        """
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            from pdf2image import convert_from_path
            
            # Set output directory
            if output_dir is None:
                output_dir = self.output_dir
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Extract images from PDF
            images = convert_from_path(pdf_path, dpi=300)
            
            # Process each page
            processed_paths = []
            for i, image in enumerate(images):
                # Convert PIL Image to OpenCV format
                cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Generate output filename
                base_name = os.path.basename(pdf_path)
                name, _ = os.path.splitext(base_name)
                output_filename = f"{name}_page_{i+1}.jpg"
                
                # Process image
                _, output_path = self.process_image_from_array(cv_image, output_filename)
                processed_paths.append(output_path)
            
            logger.info(f"PDF processed successfully: {len(processed_paths)} pages")
            
            return processed_paths
        
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
    
    def process_image_from_array(self, image: np.ndarray, output_filename: str) -> Tuple[np.ndarray, str]:
        """
        Process image from numpy array.
        
        Args:
            image (np.ndarray): Input image array
            output_filename (str): Output filename
            
        Returns:
            Tuple[np.ndarray, str]: Processed image and path to saved image
        """
        try:
            # Apply preprocessing steps
            # 1. Detect and correct perspective
            image = self.detect_and_correct_perspective(image)
            
            # 2. Resize to target DPI
            image = self.resize_image(image, target_dpi=300)
            
            # 3. Convert to grayscale
            image = self.convert_to_grayscale(image)
            
            # 4. Denoise
            image = self.denoise_image(image)
            
            # 5. Adjust contrast
            image = self.adjust_contrast(image, alpha=1.5, beta=10)
            
            # 6. Apply thresholding
            image = self.threshold_image(image)
            
            # 7. Deskew
            image = self.deskew_image(image)
            
            # Save processed image
            output_path = self.save_image(image, output_filename)
            
            return image, output_path
        
        except Exception as e:
            logger.error(f"Error processing image array: {str(e)}")
            raise