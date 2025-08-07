"""
Document classification module for identifying document types.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
import logging
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentClassifier:
    """
    Class for classifying document types based on OCR text.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the document classifier.
        
        Args:
            model_path (str, optional): Path to pre-trained model
        """
        self.model = None
        self.document_types = [
            'financial_statement',
            'balance_sheet',
            'income_statement',
            'cash_flow_statement',
            'tax_return',
            'business_registration',
            'bank_statement',
            'identity_document',
            'business_plan',
            'invoice',
            'receipt',
            'contract',
            'other'
        ]
        
        # Load model if provided
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def train(self, training_data: List[Dict[str, Any]], model_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Train the document classifier.
        
        Args:
            training_data (List[Dict[str, Any]]): List of documents with text and type
            model_path (str, optional): Path to save the trained model
            
        Returns:
            Dict[str, Any]: Training results
        """
        logger.info("Training document classifier")
        
        try:
            # Extract features and labels
            texts = [doc['text'] for doc in training_data]
            labels = [doc['document_type'] for doc in training_data]
            
            # Create pipeline
            pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),
                    stop_words='english'
                )),
                ('classifier', RandomForestClassifier(
                    n_estimators=100,
                    random_state=42
                ))
            ])
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                texts, labels, test_size=0.2, random_state=42
            )
            
            # Train model
            pipeline.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = pipeline.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)
            
            # Save model
            self.model = pipeline
            if model_path:
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                joblib.dump(pipeline, model_path)
                logger.info(f"Model saved to {model_path}")
            
            logger.info(f"Model training completed. Accuracy: {report['accuracy']:.4f}")
            
            return {
                'accuracy': report['accuracy'],
                'classification_report': report,
                'model_path': model_path
            }
        
        except Exception as e:
            logger.error(f"Error training document classifier: {str(e)}")
            raise
    
    def load_model(self, model_path: str) -> None:
        """
        Load a trained model.
        
        Args:
            model_path (str): Path to the trained model
        """
        logger.info(f"Loading model from {model_path}")
        
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def classify(self, text: str) -> Dict[str, Any]:
        """
        Classify a document based on its text.
        
        Args:
            text (str): Document text
            
        Returns:
            Dict[str, Any]: Classification result
        """
        logger.info("Classifying document")
        
        try:
            if self.model is None:
                # Use rule-based classification if no model is available
                return self._rule_based_classification(text)
            
            # Predict document type
            document_type = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            
            # Get class probabilities
            class_probs = {}
            for i, class_name in enumerate(self.model.classes_):
                class_probs[class_name] = float(probabilities[i])
            
            # Get top keywords
            keywords = self._extract_keywords(text, document_type)
            
            # Create result
            result = {
                'document_type': document_type,
                'confidence': float(max(probabilities)),
                'class_probabilities': class_probs,
                'keywords': keywords
            }
            
            logger.info(f"Document classified as {document_type} with confidence {result['confidence']:.4f}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error classifying document: {str(e)}")
            raise
    
    def _rule_based_classification(self, text: str) -> Dict[str, Any]:
        """
        Classify document using rule-based approach.
        
        Args:
            text (str): Document text
            
        Returns:
            Dict[str, Any]: Classification result
        """
        logger.info("Using rule-based classification")
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Define patterns for each document type
        patterns = {
            'balance_sheet': [
                r'balance\s+sheet',
                r'assets\s+and\s+liabilities',
                r'total\s+assets',
                r'total\s+liabilities',
                r'shareholder\'?s?\s+equity',
                r'current\s+assets',
                r'non-current\s+assets'
            ],
            'income_statement': [
                r'income\s+statement',
                r'profit\s+and\s+loss',
                r'revenue',
                r'net\s+income',
                r'gross\s+profit',
                r'operating\s+expenses',
                r'ebitda'
            ],
            'cash_flow_statement': [
                r'cash\s+flow\s+statement',
                r'operating\s+activities',
                r'investing\s+activities',
                r'financing\s+activities',
                r'net\s+cash\s+flow'
            ],
            'tax_return': [
                r'tax\s+return',
                r'form\s+1040',
                r'form\s+1120',
                r'taxable\s+income',
                r'tax\s+year',
                r'irs'
            ],
            'business_registration': [
                r'certificate\s+of\s+incorporation',
                r'business\s+license',
                r'registration\s+certificate',
                r'articles\s+of\s+incorporation',
                r'company\s+registration'
            ],
            'bank_statement': [
                r'bank\s+statement',
                r'account\s+statement',
                r'opening\s+balance',
                r'closing\s+balance',
                r'transaction\s+history',
                r'withdrawal',
                r'deposit'
            ],
            'identity_document': [
                r'passport',
                r'driver\'?s?\s+license',
                r'identity\s+card',
                r'date\s+of\s+birth',
                r'expiration\s+date',
                r'identification'
            ],
            'business_plan': [
                r'business\s+plan',
                r'executive\s+summary',
                r'market\s+analysis',
                r'competitive\s+analysis',
                r'financial\s+projections',
                r'swot\s+analysis'
            ],
            'invoice': [
                r'invoice',
                r'bill\s+to',
                r'invoice\s+number',
                r'due\s+date',
                r'payment\s+terms',
                r'subtotal',
                r'total\s+due'
            ],
            'receipt': [
                r'receipt',
                r'payment\s+received',
                r'thank\s+you\s+for\s+your\s+purchase',
                r'amount\s+paid',
                r'cashier'
            ],
            'contract': [
                r'agreement',
                r'contract',
                r'terms\s+and\s+conditions',
                r'parties',
                r'hereby\s+agree',
                r'signature'
            ]
        }
        
        # Count matches for each document type
        matches = {}
        for doc_type, patterns_list in patterns.items():
            count = 0
            matched_patterns = []
            
            for pattern in patterns_list:
                if re.search(pattern, text_lower):
                    count += 1
                    matched_patterns.append(pattern)
            
            matches[doc_type] = {
                'count': count,
                'patterns': matched_patterns
            }
        
        # Find document type with most matches
        best_match = max(matches.items(), key=lambda x: x[1]['count'])
        document_type = best_match[0]
        match_count = best_match[1]['count']
        matched_patterns = best_match[1]['patterns']
        
        # If no strong match, classify as 'other'
        if match_count < 2:
            document_type = 'other'
            confidence = 0.3
        else:
            # Calculate confidence based on match count
            pattern_count = len(patterns[document_type])
            confidence = min(0.9, match_count / pattern_count)
        
        # Handle financial statement types
        if document_type in ['balance_sheet', 'income_statement', 'cash_flow_statement']:
            # Also mark as financial_statement
            financial_statement_confidence = confidence * 0.9
            
            # Create result with hierarchical classification
            result = {
                'document_type': document_type,
                'parent_type': 'financial_statement',
                'confidence': confidence,
                'parent_confidence': financial_statement_confidence,
                'matched_patterns': matched_patterns
            }
        else:
            # Create result
            result = {
                'document_type': document_type,
                'confidence': confidence,
                'matched_patterns': matched_patterns
            }
        
        logger.info(f"Rule-based classification: {document_type} with confidence {confidence:.4f}")
        
        return result
    
    def _extract_keywords(self, text: str, document_type: str) -> List[str]:
        """
        Extract keywords relevant to the document type.
        
        Args:
            text (str): Document text
            document_type (str): Document type
            
        Returns:
            List[str]: Extracted keywords
        """
        # Define keywords for each document type
        keywords_dict = {
            'financial_statement': [
                'assets', 'liabilities', 'equity', 'revenue', 'expenses',
                'profit', 'loss', 'balance', 'cash flow', 'income'
            ],
            'balance_sheet': [
                'assets', 'liabilities', 'equity', 'current assets',
                'non-current assets', 'current liabilities', 'long-term liabilities',
                'shareholder equity', 'retained earnings', 'total assets'
            ],
            'income_statement': [
                'revenue', 'sales', 'cost of goods sold', 'gross profit',
                'operating expenses', 'operating income', 'net income',
                'profit margin', 'ebitda', 'earnings'
            ],
            'cash_flow_statement': [
                'operating activities', 'investing activities', 'financing activities',
                'net cash flow', 'cash and cash equivalents', 'depreciation',
                'amortization', 'capital expenditures', 'dividends'
            ],
            'tax_return': [
                'taxable income', 'tax year', 'deductions', 'credits',
                'filing status', 'tax rate', 'tax liability', 'refund',
                'irs', 'form 1040', 'form 1120'
            ],
            'business_registration': [
                'incorporation', 'registration', 'certificate', 'business license',
                'articles', 'company name', 'registered address', 'business type',
                'ein', 'tax id'
            ],
            'bank_statement': [
                'account number', 'balance', 'transaction', 'deposit',
                'withdrawal', 'opening balance', 'closing balance',
                'statement period', 'bank name', 'account holder'
            ],
            'identity_document': [
                'name', 'date of birth', 'address', 'photo', 'signature',
                'expiration date', 'identification number', 'nationality',
                'gender', 'issuing authority'
            ],
            'business_plan': [
                'executive summary', 'market analysis', 'competitive analysis',
                'marketing strategy', 'financial projections', 'swot',
                'management team', 'operations', 'funding request'
            ],
            'invoice': [
                'invoice number', 'bill to', 'ship to', 'payment terms',
                'due date', 'subtotal', 'tax', 'total', 'item description',
                'quantity', 'unit price'
            ],
            'receipt': [
                'receipt number', 'date', 'amount', 'payment method',
                'merchant', 'item', 'total', 'tax', 'cashier', 'thank you'
            ],
            'contract': [
                'agreement', 'parties', 'terms', 'conditions', 'effective date',
                'termination', 'signature', 'obligations', 'payment terms',
                'confidentiality', 'governing law'
            ],
            'other': [
                'document', 'page', 'date', 'reference', 'signature',
                'company', 'information', 'contact', 'address', 'phone'
            ]
        }
        
        # Get keywords for document type
        target_keywords = keywords_dict.get(document_type, keywords_dict['other'])
        
        # Find matches in text
        matched_keywords = []
        text_lower = text.lower()
        
        for keyword in target_keywords:
            if keyword.lower() in text_lower:
                matched_keywords.append(keyword)
        
        return matched_keywords