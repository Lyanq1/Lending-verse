"""
Main credit scoring module for LendingVerse platform.
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from preprocessing import FinancialDataPreprocessor, BusinessDataPreprocessor
from feature_engineering import FeatureCombiner
from models import CreditScoreClassifier, DefaultProbabilityEstimator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreditScoringSystem:
    """
    Main credit scoring system for assessing borrower creditworthiness.
    """
    
    def __init__(self, model_dir='models'):
        """
        Initialize the credit scoring system.
        
        Args:
            model_dir (str): Directory containing trained models
        """
        self.model_dir = model_dir
        self.credit_score_model = None
        self.default_probability_model = None
        self.financial_preprocessor = FinancialDataPreprocessor()
        self.business_preprocessor = BusinessDataPreprocessor()
        self.feature_combiner = FeatureCombiner()
        
        # Credit score categories and their corresponding numerical values
        self.credit_categories = {
            'A': {'score': 90, 'description': 'Excellent credit, very low risk'},
            'B': {'score': 80, 'description': 'Good credit, low risk'},
            'C': {'score': 70, 'description': 'Fair credit, moderate risk'},
            'D': {'score': 60, 'description': 'Below average credit, high risk'},
            'E': {'score': 50, 'description': 'Poor credit, very high risk'}
        }
        
        # Load models if available
        self._load_models()
    
    def _load_models(self):
        """Load trained models if available."""
        try:
            credit_score_path = os.path.join(self.model_dir, 'credit_score_model_ensemble.pkl')
            if os.path.exists(credit_score_path):
                self.credit_score_model = CreditScoreClassifier.load_model(credit_score_path)
                logger.info("Credit score model loaded successfully")
            
            default_prob_path = os.path.join(self.model_dir, 'default_probability_model.pkl')
            if os.path.exists(default_prob_path):
                self.default_probability_model = DefaultProbabilityEstimator.load_model(default_prob_path)
                logger.info("Default probability model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
    
    def preprocess_data(self, financial_data=None, business_data=None, credit_history_data=None):
        """
        Preprocess input data from various sources.
        
        Args:
            financial_data (pd.DataFrame): Financial statement data
            business_data (pd.DataFrame): Business profile data
            credit_history_data (pd.DataFrame): Credit history data
            
        Returns:
            dict: Preprocessed data
        """
        logger.info("Preprocessing input data")
        
        preprocessed_data = {}
        
        if financial_data is not None:
            preprocessed_data['financial'] = self.financial_preprocessor.calculate_financial_ratios(financial_data)
        
        if business_data is not None:
            business_processed = business_data.copy()
            if 'industry' in business_processed.columns:
                business_processed = self.business_preprocessor.encode_industry(business_processed)
            if 'founded_year' in business_processed.columns:
                business_processed = self.business_preprocessor.encode_company_age(business_processed)
            preprocessed_data['business'] = business_processed
        
        if credit_history_data is not None:
            preprocessed_data['credit_history'] = credit_history_data
        
        return preprocessed_data
    
    def extract_features(self, preprocessed_data):
        """
        Extract features from preprocessed data.
        
        Args:
            preprocessed_data (dict): Preprocessed data from different sources
            
        Returns:
            pd.DataFrame: Combined features
        """
        logger.info("Extracting features")
        
        return self.feature_combiner.transform(preprocessed_data)
    
    def score_borrower(self, financial_data=None, business_data=None, credit_history_data=None):
        """
        Generate credit score and default probability for a borrower.
        
        Args:
            financial_data (pd.DataFrame): Financial statement data
            business_data (pd.DataFrame): Business profile data
            credit_history_data (pd.DataFrame): Credit history data
            
        Returns:
            dict: Credit assessment results
        """
        logger.info("Scoring borrower")
        
        try:
            # Preprocess data
            preprocessed_data = self.preprocess_data(
                financial_data, business_data, credit_history_data
            )
            
            # Extract features
            features = self.extract_features(preprocessed_data)
            
            # Check if we have enough data
            if features.empty:
                return {
                    'error': 'Insufficient data for credit scoring',
                    'timestamp': datetime.now().isoformat()
                }
            
            # If models are not loaded, use heuristic scoring
            if self.credit_score_model is None:
                return self._heuristic_scoring(preprocessed_data, features)
            
            # Predict credit score category
            credit_category = self.credit_score_model.predict(features)[0]
            
            # Predict default probability
            default_probability = 0.0
            if self.default_probability_model is not None:
                default_probability = float(self.default_probability_model.predict_default_probability(features)[0])
            
            # Get category details
            category_details = self.credit_categories.get(credit_category, {
                'score': 0,
                'description': 'Unknown'
            })
            
            # Create result
            result = {
                'credit_score': {
                    'category': credit_category,
                    'numerical_score': category_details['score'],
                    'description': category_details['description']
                },
                'default_probability': default_probability,
                'risk_assessment': self._assess_risk(credit_category, default_probability),
                'timestamp': datetime.now().isoformat()
            }
            
            # Add explanatory factors if available
            if hasattr(self.credit_score_model, 'feature_importances_') and self.credit_score_model.feature_importances_ is not None:
                result['explanatory_factors'] = self._get_explanatory_factors(features)
            
            return result
        
        except Exception as e:
            logger.error(f"Error in credit scoring: {str(e)}")
            return {
                'error': f'Credit scoring failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _heuristic_scoring(self, preprocessed_data, features):
        """
        Generate credit score using heuristic rules when models are not available.
        
        Args:
            preprocessed_data (dict): Preprocessed data
            features (pd.DataFrame): Extracted features
            
        Returns:
            dict: Credit assessment results
        """
        logger.info("Using heuristic scoring (models not loaded)")
        
        score_factors = []
        
        # Financial factors
        if 'financial' in preprocessed_data:
            financial = preprocessed_data['financial']
            
            # Profitability
            if 'return_on_assets' in financial.columns:
                roa = financial['return_on_assets'].iloc[0]
                score_factors.append(min(max(roa * 100, 0), 100))
            
            # Liquidity
            if 'current_ratio' in financial.columns:
                cr = financial['current_ratio'].iloc[0]
                score_factors.append(min(max(cr * 25, 0), 100))
            
            # Leverage
            if 'debt_to_equity' in financial.columns:
                dte = financial['debt_to_equity'].iloc[0]
                score_factors.append(min(max(100 - dte * 20, 0), 100))
        
        # Business factors
        if 'business' in preprocessed_data:
            business = preprocessed_data['business']
            
            # Company age
            if 'company_age' in business.columns:
                age = business['company_age'].iloc[0]
                score_factors.append(min(max(age * 5, 0), 100))
            
            # Industry risk (inverse)
            if 'industry_risk' in business.columns:
                risk = business['industry_risk'].iloc[0]
                score_factors.append(min(max(100 - risk * 10, 0), 100))
        
        # Credit history factors
        if 'credit_history' in preprocessed_data:
            credit = preprocessed_data['credit_history']
            
            # Payment reliability
            if 'payment_reliability' in credit.columns:
                reliability = credit['payment_reliability'].iloc[0]
                score_factors.append(reliability)
            
            # Previous defaults (inverse)
            if 'previous_defaults' in credit.columns:
                defaults = credit['previous_defaults'].iloc[0]
                score_factors.append(max(100 - defaults * 25, 0))
        
        # Calculate overall score
        if score_factors:
            overall_score = sum(score_factors) / len(score_factors)
        else:
            overall_score = 50  # Default to middle score if no factors available
        
        # Determine credit category
        credit_category = 'E'
        if overall_score >= 90:
            credit_category = 'A'
        elif overall_score >= 80:
            credit_category = 'B'
        elif overall_score >= 70:
            credit_category = 'C'
        elif overall_score >= 60:
            credit_category = 'D'
        
        # Calculate default probability (simple heuristic)
        default_probability = max(0, min(1, 1 - (overall_score / 100)))
        
        # Get category details
        category_details = self.credit_categories.get(credit_category, {
            'score': overall_score,
            'description': 'Unknown'
        })
        
        # Create result
        result = {
            'credit_score': {
                'category': credit_category,
                'numerical_score': category_details['score'],
                'description': category_details['description']
            },
            'default_probability': float(default_probability),
            'risk_assessment': self._assess_risk(credit_category, default_probability),
            'timestamp': datetime.now().isoformat(),
            'note': 'Heuristic scoring used (models not loaded)'
        }
        
        return result
    
    def _assess_risk(self, credit_category, default_probability):
        """
        Assess overall risk based on credit category and default probability.
        
        Args:
            credit_category (str): Credit score category
            default_probability (float): Probability of default
            
        Returns:
            dict: Risk assessment
        """
        # Define risk levels
        if credit_category == 'A' and default_probability < 0.05:
            risk_level = 'Very Low'
            recommendation = 'Highly recommended for approval'
        elif credit_category in ['A', 'B'] and default_probability < 0.10:
            risk_level = 'Low'
            recommendation = 'Recommended for approval'
        elif credit_category in ['B', 'C'] and default_probability < 0.15:
            risk_level = 'Moderate'
            recommendation = 'Consider approval with standard terms'
        elif credit_category in ['C', 'D'] and default_probability < 0.25:
            risk_level = 'High'
            recommendation = 'Consider approval with stricter terms'
        else:
            risk_level = 'Very High'
            recommendation = 'Not recommended for approval'
        
        return {
            'risk_level': risk_level,
            'recommendation': recommendation
        }
    
    def _get_explanatory_factors(self, features):
        """
        Get explanatory factors for the credit score.
        
        Args:
            features (pd.DataFrame): Feature values
            
        Returns:
            list: Explanatory factors
        """
        if not hasattr(self.credit_score_model, 'feature_importances_'):
            return []
        
        # Get feature importances
        importances = self.credit_score_model.feature_importances_
        
        # Get feature names
        feature_names = features.columns.tolist()
        
        # Sort features by importance
        sorted_indices = np.argsort(importances)[::-1]
        
        # Get top factors
        top_factors = []
        for i in sorted_indices[:5]:  # Top 5 factors
            if i < len(feature_names):
                feature_name = feature_names[i]
                feature_value = features[feature_name].iloc[0]
                
                # Determine if factor is positive or negative
                impact = 'positive' if feature_value > 0 else 'negative'
                
                top_factors.append({
                    'factor': feature_name,
                    'importance': float(importances[i]),
                    'value': float(feature_value),
                    'impact': impact
                })
        
        return top_factors
    
    def save_assessment(self, assessment, output_dir='assessments'):
        """
        Save credit assessment to file.
        
        Args:
            assessment (dict): Credit assessment results
            output_dir (str): Directory to save assessment
            
        Returns:
            str: Path to saved assessment file
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"credit_assessment_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Save assessment
        with open(filepath, 'w') as f:
            json.dump(assessment, f, indent=2)
        
        logger.info(f"Credit assessment saved to {filepath}")
        
        return filepath