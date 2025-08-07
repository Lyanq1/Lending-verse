"""
OCR module for document processing.
"""

import pytesseract
import cv2
import numpy as np
import os
import json
from typing import Dict, List, Any, Optional, Tuple
import logging
from PIL import Image
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCREngine:
    """
    Class for performing OCR on document images.
    """
    
    def __init__(self, tesseract_path: Optional[str] = None, output_dir: str = 'ocr_results'):
        """
        Initialize the OCR engine.
        
        Args:
            tesseract_path (str, optional): Path to Tesseract executable
            output_dir (str): Directory to save OCR results
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def perform_ocr(self, image_path: str, lang: str = 'eng') -> Dict[str, Any]:
        """
        Perform OCR on an image.
        
        Args:
            image_path (str): Path to the image file
            lang (str): Language for OCR
            
        Returns:
            Dict[str, Any]: OCR results
        """
        logger.info(f"Performing OCR on image: {image_path}")
        
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image from {image_path}")
            
            # Get OCR data
            ocr_data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            
            # Get full text
            full_text = pytesseract.image_to_string(image, lang=lang)
            
            # Create result
            result = {
                'text': full_text,
                'words': self._extract_words(ocr_data),
                'confidence': self._calculate_confidence(ocr_data),
                'image_path': image_path
            }
            
            # Save result
            self._save_result(result, image_path)
            
            logger.info(f"OCR completed successfully for {image_path}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error performing OCR: {str(e)}")
            raise
    
    def perform_ocr_with_layout(self, image_path: str, lang: str = 'eng') -> Dict[str, Any]:
        """
        Perform OCR with layout analysis.
        
        Args:
            image_path (str): Path to the image file
            lang (str): Language for OCR
            
        Returns:
            Dict[str, Any]: OCR results with layout information
        """
        logger.info(f"Performing OCR with layout analysis on image: {image_path}")
        
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image from {image_path}")
            
            # Get OCR data
            ocr_data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            
            # Get layout analysis
            layout_data = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
            
            # Get full text
            full_text = pytesseract.image_to_string(image, lang=lang)
            
            # Extract paragraphs
            paragraphs = self._extract_paragraphs(image, ocr_data)
            
            # Create result
            result = {
                'text': full_text,
                'words': self._extract_words(ocr_data),
                'confidence': self._calculate_confidence(ocr_data),
                'layout': layout_data,
                'paragraphs': paragraphs,
                'image_path': image_path
            }
            
            # Save result
            self._save_result(result, image_path, suffix='_layout')
            
            logger.info(f"OCR with layout analysis completed successfully for {image_path}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error performing OCR with layout analysis: {str(e)}")
            raise
    
    def perform_ocr_on_region(self, image_path: str, region: Tuple[int, int, int, int], lang: str = 'eng') -> Dict[str, Any]:
        """
        Perform OCR on a specific region of an image.
        
        Args:
            image_path (str): Path to the image file
            region (Tuple[int, int, int, int]): Region to process (x, y, width, height)
            lang (str): Language for OCR
            
        Returns:
            Dict[str, Any]: OCR results for the region
        """
        logger.info(f"Performing OCR on region {region} of image: {image_path}")
        
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image from {image_path}")
            
            # Extract region
            x, y, width, height = region
            region_image = image[y:y+height, x:x+width]
            
            # Get OCR data for region
            ocr_data = pytesseract.image_to_data(region_image, lang=lang, output_type=pytesseract.Output.DICT)
            
            # Get full text for region
            region_text = pytesseract.image_to_string(region_image, lang=lang)
            
            # Create result
            result = {
                'text': region_text,
                'words': self._extract_words(ocr_data),
                'confidence': self._calculate_confidence(ocr_data),
                'region': region,
                'image_path': image_path
            }
            
            logger.info(f"OCR on region completed successfully for {image_path}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error performing OCR on region: {str(e)}")
            raise
    
    def extract_tables(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables from an image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            List[Dict[str, Any]]: Extracted tables
        """
        logger.info(f"Extracting tables from image: {image_path}")
        
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by size
            min_area = 5000  # Minimum area for a table
            table_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
            
            tables = []
            for i, contour in enumerate(table_contours):
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Extract table region
                table_region = image[y:y+h, x:x+w]
                
                # Save table image
                table_filename = f"table_{i+1}.jpg"
                table_path = os.path.join(self.output_dir, table_filename)
                cv2.imwrite(table_path, table_region)
                
                # Perform OCR on table
                table_text = pytesseract.image_to_string(table_region)
                
                # Parse table structure
                table_data = self._parse_table_structure(table_region, table_text)
                
                tables.append({
                    'table_id': i + 1,
                    'region': (x, y, w, h),
                    'text': table_text,
                    'data': table_data,
                    'image_path': table_path
                })
            
            logger.info(f"Extracted {len(tables)} tables from {image_path}")
            
            return tables
        
        except Exception as e:
            logger.error(f"Error extracting tables: {str(e)}")
            raise
    
    def _extract_words(self, ocr_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract words with position and confidence from OCR data.
        
        Args:
            ocr_data (Dict[str, Any]): OCR data from pytesseract
            
        Returns:
            List[Dict[str, Any]]: Extracted words
        """
        words = []
        n_boxes = len(ocr_data['text'])
        
        for i in range(n_boxes):
            # Skip empty text
            if ocr_data['text'][i].strip() == '':
                continue
            
            # Create word entry
            word = {
                'text': ocr_data['text'][i],
                'confidence': ocr_data['conf'][i],
                'position': {
                    'x': ocr_data['left'][i],
                    'y': ocr_data['top'][i],
                    'width': ocr_data['width'][i],
                    'height': ocr_data['height'][i]
                },
                'block_num': ocr_data['block_num'][i],
                'line_num': ocr_data['line_num'][i],
                'word_num': ocr_data['word_num'][i]
            }
            
            words.append(word)
        
        return words
    
    def _calculate_confidence(self, ocr_data: Dict[str, Any]) -> float:
        """
        Calculate overall OCR confidence.
        
        Args:
            ocr_data (Dict[str, Any]): OCR data from pytesseract
            
        Returns:
            float: Overall confidence score
        """
        confidences = [conf for conf in ocr_data['conf'] if conf != -1]
        if confidences:
            return sum(confidences) / len(confidences)
        return 0.0
    
    def _extract_paragraphs(self, image: np.ndarray, ocr_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract paragraphs from OCR data.
        
        Args:
            image (np.ndarray): Input image
            ocr_data (Dict[str, Any]): OCR data from pytesseract
            
        Returns:
            List[Dict[str, Any]]: Extracted paragraphs
        """
        # Group words by block and line
        blocks = {}
        for i in range(len(ocr_data['text'])):
            if ocr_data['text'][i].strip() == '':
                continue
            
            block_num = ocr_data['block_num'][i]
            line_num = ocr_data['line_num'][i]
            
            if block_num not in blocks:
                blocks[block_num] = {}
            
            if line_num not in blocks[block_num]:
                blocks[block_num][line_num] = []
            
            blocks[block_num][line_num].append({
                'text': ocr_data['text'][i],
                'confidence': ocr_data['conf'][i],
                'position': {
                    'x': ocr_data['left'][i],
                    'y': ocr_data['top'][i],
                    'width': ocr_data['width'][i],
                    'height': ocr_data['height'][i]
                }
            })
        
        # Combine lines into paragraphs
        paragraphs = []
        for block_num, lines in blocks.items():
            # Sort lines by line number
            sorted_lines = sorted(lines.items(), key=lambda x: x[0])
            
            # Combine text from all lines in the block
            text = ' '.join([
                ' '.join([word['text'] for word in line])
                for _, line in sorted_lines
            ])
            
            # Calculate paragraph bounding box
            all_words = [word for _, line in sorted_lines for word in line]
            min_x = min(word['position']['x'] for word in all_words)
            min_y = min(word['position']['y'] for word in all_words)
            max_x = max(word['position']['x'] + word['position']['width'] for word in all_words)
            max_y = max(word['position']['y'] + word['position']['height'] for word in all_words)
            
            # Create paragraph entry
            paragraph = {
                'text': text,
                'block_num': block_num,
                'position': {
                    'x': min_x,
                    'y': min_y,
                    'width': max_x - min_x,
                    'height': max_y - min_y
                },
                'line_count': len(lines)
            }
            
            paragraphs.append(paragraph)
        
        return paragraphs
    
    def _parse_table_structure(self, table_image: np.ndarray, table_text: str) -> List[List[str]]:
        """
        Parse table structure from OCR text.
        
        Args:
            table_image (np.ndarray): Table image
            table_text (str): OCR text from table
            
        Returns:
            List[List[str]]: Table data as rows and columns
        """
        # Split text into lines
        lines = table_text.strip().split('\n')
        
        # Find delimiter pattern (spaces or |)
        delimiter_pattern = None
        if '|' in table_text:
            delimiter_pattern = r'\|'
        else:
            # Assume space-delimited
            delimiter_pattern = r'\s{2,}'
        
        # Parse rows and columns
        table_data = []
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Split line into columns
            columns = re.split(delimiter_pattern, line.strip())
            
            # Remove empty columns
            columns = [col.strip() for col in columns if col.strip()]
            
            if columns:
                table_data.append(columns)
        
        return table_data
    
    def _save_result(self, result: Dict[str, Any], image_path: str, suffix: str = '') -> str:
        """
        Save OCR result to file.
        
        Args:
            result (Dict[str, Any]): OCR result
            image_path (str): Path to the original image
            suffix (str): Suffix for output filename
            
        Returns:
            str: Path to saved result
        """
        # Generate output filename
        base_name = os.path.basename(image_path)
        name, _ = os.path.splitext(base_name)
        output_filename = f"{name}{suffix}_ocr.json"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Save result as JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return output_path


class CloudOCREngine:
    """
    Class for performing OCR using cloud services.
    """
    
    def __init__(self, service_type: str = 'google', api_key: Optional[str] = None, output_dir: str = 'ocr_results'):
        """
        Initialize the cloud OCR engine.
        
        Args:
            service_type (str): Cloud service to use ('google', 'amazon', 'azure')
            api_key (str, optional): API key for the cloud service
            output_dir (str): Directory to save OCR results
        """
        self.service_type = service_type
        self.api_key = api_key
        self.output_dir = output_dir
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def perform_ocr(self, image_path: str) -> Dict[str, Any]:
        """
        Perform OCR using cloud service.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: OCR results
        """
        logger.info(f"Performing cloud OCR on image: {image_path}")
        
        if self.service_type == 'google':
            return self._google_vision_ocr(image_path)
        elif self.service_type == 'amazon':
            return self._amazon_textract_ocr(image_path)
        elif self.service_type == 'azure':
            return self._azure_ocr(image_path)
        else:
            raise ValueError(f"Unsupported cloud service: {self.service_type}")
    
    def _google_vision_ocr(self, image_path: str) -> Dict[str, Any]:
        """
        Perform OCR using Google Cloud Vision.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: OCR results
        """
        try:
            from google.cloud import vision
            
            # Initialize client
            client = vision.ImageAnnotatorClient()
            
            # Read image file
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            # Create image object
            image = vision.Image(content=content)
            
            # Perform OCR
            response = client.document_text_detection(image=image)
            
            # Process response
            full_text = response.full_text_annotation.text
            
            # Extract words
            words = []
            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            word_text = ''.join([symbol.text for symbol in word.symbols])
                            
                            # Get bounding box
                            vertices = word.bounding_box.vertices
                            x = vertices[0].x
                            y = vertices[0].y
                            width = vertices[2].x - x
                            height = vertices[2].y - y
                            
                            words.append({
                                'text': word_text,
                                'confidence': word.confidence,
                                'position': {
                                    'x': x,
                                    'y': y,
                                    'width': width,
                                    'height': height
                                }
                            })
            
            # Create result
            result = {
                'text': full_text,
                'words': words,
                'confidence': response.full_text_annotation.pages[0].blocks[0].confidence if response.full_text_annotation.pages else 0.0,
                'image_path': image_path,
                'service': 'google_vision'
            }
            
            # Save result
            self._save_result(result, image_path)
            
            logger.info(f"Google Cloud Vision OCR completed successfully for {image_path}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error performing Google Cloud Vision OCR: {str(e)}")
            raise
    
    def _amazon_textract_ocr(self, image_path: str) -> Dict[str, Any]:
        """
        Perform OCR using Amazon Textract.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: OCR results
        """
        try:
            import boto3
            
            # Initialize client
            textract = boto3.client('textract')
            
            # Read image file
            with open(image_path, 'rb') as image_file:
                bytes_data = image_file.read()
            
            # Perform OCR
            response = textract.detect_document_text(Document={'Bytes': bytes_data})
            
            # Process response
            full_text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
            
            # Extract words
            words = []
            for item in response['Blocks']:
                if item['BlockType'] == 'WORD':
                    geometry = item['Geometry']['BoundingBox']
                    
                    words.append({
                        'text': item['Text'],
                        'confidence': item['Confidence'] / 100,
                        'position': {
                            'x': int(geometry['Left'] * 1000),
                            'y': int(geometry['Top'] * 1000),
                            'width': int(geometry['Width'] * 1000),
                            'height': int(geometry['Height'] * 1000)
                        }
                    })
            
            # Calculate overall confidence
            confidence = sum(item['Confidence'] for item in response['Blocks'] if 'Confidence' in item)
            confidence /= len([item for item in response['Blocks'] if 'Confidence' in item])
            confidence /= 100  # Convert to 0-1 scale
            
            # Create result
            result = {
                'text': full_text,
                'words': words,
                'confidence': confidence,
                'image_path': image_path,
                'service': 'amazon_textract'
            }
            
            # Save result
            self._save_result(result, image_path)
            
            logger.info(f"Amazon Textract OCR completed successfully for {image_path}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error performing Amazon Textract OCR: {str(e)}")
            raise
    
    def _azure_ocr(self, image_path: str) -> Dict[str, Any]:
        """
        Perform OCR using Azure Computer Vision.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: OCR results
        """
        try:
            from azure.cognitiveservices.vision.computervision import ComputerVisionClient
            from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
            from msrest.authentication import CognitiveServicesCredentials
            
            # Initialize client
            endpoint = os.environ.get('AZURE_VISION_ENDPOINT')
            client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(self.api_key))
            
            # Read image file
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Perform OCR
            read_response = client.read_in_stream(image_data, raw=True)
            
            # Get operation location
            operation_location = read_response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]
            
            # Wait for result
            import time
            while True:
                read_result = client.get_read_result(operation_id)
                if read_result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                    break
                time.sleep(1)
            
            # Process response
            full_text = ''
            words = []
            
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        full_text += line.text + ' '
                        
                        for word in line.words:
                            # Get bounding box
                            bbox = word.bounding_box
                            x = bbox[0]
                            y = bbox[1]
                            width = bbox[2] - x
                            height = bbox[5] - y
                            
                            words.append({
                                'text': word.text,
                                'confidence': word.confidence,
                                'position': {
                                    'x': x,
                                    'y': y,
                                    'width': width,
                                    'height': height
                                }
                            })
            
            # Calculate overall confidence
            confidence = sum(word['confidence'] for word in words) / len(words) if words else 0.0
            
            # Create result
            result = {
                'text': full_text.strip(),
                'words': words,
                'confidence': confidence,
                'image_path': image_path,
                'service': 'azure_vision'
            }
            
            # Save result
            self._save_result(result, image_path)
            
            logger.info(f"Azure Computer Vision OCR completed successfully for {image_path}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error performing Azure Computer Vision OCR: {str(e)}")
            raise
    
    def _save_result(self, result: Dict[str, Any], image_path: str) -> str:
        """
        Save OCR result to file.
        
        Args:
            result (Dict[str, Any]): OCR result
            image_path (str): Path to the original image
            
        Returns:
            str: Path to saved result
        """
        # Generate output filename
        base_name = os.path.basename(image_path)
        name, _ = os.path.splitext(base_name)
        output_filename = f"{name}_{self.service_type}_ocr.json"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Save result as JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return output_path