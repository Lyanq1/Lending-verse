"""
Feature engineering module for credit scoring system.
"""

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extract features from financial data for credit scoring.
    """
    
    def __init__(self):
        """Initialize the feature extractor."""
        pass
    
    def fit(self, X, y=None):
        """
        Fit the feature extractor (no-op for this transformer).
        
        Args:
            X: Input features
            y: Target variable (not used)
            
        Returns:
            self: Fitted transformer
        """
        return self
    
    def transform(self, X):
        """
        Transform the data by extracting financial features.
        
        Args:
            X (pd.DataFrame): Financial data
            
        Returns:
            pd.DataFrame: Transformed data with extracted features
        """
        logger.info("Extracting financial features")
        
        # Make a copy to avoid modifying the original data
        X_transformed = X.copy()
        
        try:
            # Calculate growth rates (if multiple periods available)
            if 'revenue' in X_transformed.columns and 'previous_revenue' in X_transformed.columns:
                X_transformed['revenue_growth'] = (X_transformed['revenue'] - X_transformed['previous_revenue']) / X_transformed['previous_revenue']
                
            if 'net_income' in X_transformed.columns and 'previous_net_income' in X_transformed.columns:
                X_transformed['profit_growth'] = (X_transformed['net_income'] - X_transformed['previous_net_income']) / X_transformed['previous_net_income']
            
            # Calculate cash flow features
            if 'operating_cash_flow' in X_transformed.columns and 'net_income' in X_transformed.columns:
                X_transformed['cash_flow_to_income'] = X_transformed['operating_cash_flow'] / X_transformed['net_income']
                
            if 'operating_cash_flow' in X_transformed.columns and 'total_debt' in X_transformed.columns:
                X_transformed['cash_flow_to_debt'] = X_transformed['operating_cash_flow'] / X_transformed['total_debt']
            
            # Calculate interest coverage ratio
            if 'ebit' in X_transformed.columns and 'interest_expense' in X_transformed.columns:
                X_transformed['interest_coverage'] = X_transformed['ebit'] / X_transformed['interest_expense']
            
            # Calculate working capital
            if 'current_assets' in X_transformed.columns and 'current_liabilities' in X_transformed.columns:
                X_transformed['working_capital'] = X_transformed['current_assets'] - X_transformed['current_liabilities']
                
                # Working capital ratio
                if 'revenue' in X_transformed.columns:
                    X_transformed['working_capital_ratio'] = X_transformed['working_capital'] / X_transformed['revenue']
            
            # Calculate debt service coverage ratio
            if 'operating_cash_flow' in X_transformed.columns and 'debt_service' in X_transformed.columns:
                X_transformed['debt_service_coverage'] = X_transformed['operating_cash_flow'] / X_transformed['debt_service']
            
            # Replace infinities and NaNs
            X_transformed = X_transformed.replace([np.inf, -np.inf], np.nan)
            
        except Exception as e:
            logger.error(f"Error extracting financial features: {str(e)}")
        
        return X_transformed


class BusinessFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extract features from business profile data for credit scoring.
    """
    
    def __init__(self):
        """Initialize the feature extractor."""
        pass
    
    def fit(self, X, y=None):
        """
        Fit the feature extractor (no-op for this transformer).
        
        Args:
            X: Input features
            y: Target variable (not used)
            
        Returns:
            self: Fitted transformer
        """
        return self
    
    def transform(self, X):
        """
        Transform the data by extracting business features.
        
        Args:
            X (pd.DataFrame): Business profile data
            
        Returns:
            pd.DataFrame: Transformed data with extracted features
        """
        logger.info("Extracting business features")
        
        # Make a copy to avoid modifying the original data
        X_transformed = X.copy()
        
        try:
            # Calculate employee productivity
            if 'revenue' in X_transformed.columns and 'employee_count' in X_transformed.columns:
                X_transformed['revenue_per_employee'] = X_transformed['revenue'] / X_transformed['employee_count']
                
            if 'net_income' in X_transformed.columns and 'employee_count' in X_transformed.columns:
                X_transformed['profit_per_employee'] = X_transformed['net_income'] / X_transformed['employee_count']
            
            # Calculate business stability score
            stability_factors = []
            
            # Age factor
            if 'company_age' in X_transformed.columns:
                age_score = np.minimum(X_transformed['company_age'] / 10, 1) * 100
                stability_factors.append(age_score)
            
            # Size factor
            if 'employee_count' in X_transformed.columns:
                size_score = np.minimum(X_transformed['employee_count'] / 100, 1) * 100
                stability_factors.append(size_score)
            
            # Revenue factor
            if 'revenue' in X_transformed.columns:
                revenue_score = np.minimum(X_transformed['revenue'] / 1000000, 1) * 100
                stability_factors.append(revenue_score)
            
            # Combine stability factors
            if stability_factors:
                X_transformed['business_stability'] = np.mean(stability_factors, axis=0)
            
            # Replace infinities and NaNs
            X_transformed = X_transformed.replace([np.inf, -np.inf], np.nan)
            
        except Exception as e:
            logger.error(f"Error extracting business features: {str(e)}")
        
        return X_transformed


class CreditHistoryFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Extract features from credit history data for credit scoring.
    """
    
    def __init__(self):
        """Initialize the feature extractor."""
        pass
    
    def fit(self, X, y=None):
        """
        Fit the feature extractor (no-op for this transformer).
        
        Args:
            X: Input features
            y: Target variable (not used)
            
        Returns:
            self: Fitted transformer
        """
        return self
    
    def transform(self, X):
        """
        Transform the data by extracting credit history features.
        
        Args:
            X (pd.DataFrame): Credit history data
            
        Returns:
            pd.DataFrame: Transformed data with extracted features
        """
        logger.info("Extracting credit history features")
        
        # Make a copy to avoid modifying the original data
        X_transformed = X.copy()
        
        try:
            # Calculate payment behavior features
            if 'payments_on_time' in X_transformed.columns and 'total_payments' in X_transformed.columns:
                X_transformed['payment_reliability'] = X_transformed['payments_on_time'] / X_transformed['total_payments'] * 100
            
            # Calculate credit utilization
            if 'current_debt' in X_transformed.columns and 'credit_limit' in X_transformed.columns:
                X_transformed['credit_utilization'] = X_transformed['current_debt'] / X_transformed['credit_limit'] * 100
            
            # Calculate debt ratio
            if 'total_debt' in X_transformed.columns and 'total_assets' in X_transformed.columns:
                X_transformed['debt_ratio'] = X_transformed['total_debt'] / X_transformed['total_assets'] * 100
            
            # Calculate default risk indicators
            risk_factors = []
            
            # Late payment factor
            if 'late_payments' in X_transformed.columns and 'total_payments' in X_transformed.columns:
                late_payment_ratio = X_transformed['late_payments'] / X_transformed['total_payments']
                late_payment_risk = late_payment_ratio * 100
                risk_factors.append(late_payment_risk)
            
            # Default history factor
            if 'previous_defaults' in X_transformed.columns:
                default_risk = X_transformed['previous_defaults'] * 25
                risk_factors.append(default_risk)
            
            # Credit utilization factor
            if 'credit_utilization' in X_transformed.columns:
                utilization_risk = X_transformed['credit_utilization'] * 0.5
                risk_factors.append(utilization_risk)
            
            # Combine risk factors
            if risk_factors:
                X_transformed['default_risk_score'] = np.mean(risk_factors, axis=0)
            
            # Replace infinities and NaNs
            X_transformed = X_transformed.replace([np.inf, -np.inf], np.nan)
            
        except Exception as e:
            logger.error(f"Error extracting credit history features: {str(e)}")
        
        return X_transformed


class FeatureCombiner(BaseEstimator, TransformerMixin):
    """
    Combine features from different data sources for credit scoring.
    """
    
    def __init__(self):
        """Initialize the feature combiner."""
        pass
    
    def fit(self, X, y=None):
        """
        Fit the feature combiner (no-op for this transformer).
        
        Args:
            X: Input features
            y: Target variable (not used)
            
        Returns:
            self: Fitted transformer
        """
        return self
    
    def transform(self, X):
        """
        Transform the data by combining features.
        
        Args:
            X (dict): Dictionary of DataFrames from different sources
                - X['financial']: Financial data
                - X['business']: Business profile data
                - X['credit_history']: Credit history data
            
        Returns:
            pd.DataFrame: Combined features
        """
        logger.info("Combining features from different sources")
        
        combined_features = pd.DataFrame()
        
        try:
            # Extract features from each source
            if 'financial' in X:
                financial_extractor = FinancialFeatureExtractor()
                financial_features = financial_extractor.transform(X['financial'])
                
                # Select relevant columns
                financial_cols = [
                    'current_ratio', 'cash_ratio', 'return_on_assets', 'return_on_equity',
                    'gross_margin', 'net_profit_margin', 'debt_to_assets', 'debt_to_equity',
                    'asset_turnover', 'inventory_turnover', 'revenue_growth', 'profit_growth',
                    'cash_flow_to_income', 'cash_flow_to_debt', 'interest_coverage',
                    'working_capital_ratio', 'debt_service_coverage'
                ]
                
                # Only include columns that exist
                existing_cols = [col for col in financial_cols if col in financial_features.columns]
                if existing_cols:
                    combined_features = pd.concat([combined_features, financial_features[existing_cols]], axis=1)
            
            if 'business' in X:
                business_extractor = BusinessFeatureExtractor()
                business_features = business_extractor.transform(X['business'])
                
                # Select relevant columns
                business_cols = [
                    'company_age', 'industry_risk', 'age_risk', 'revenue_per_employee',
                    'profit_per_employee', 'business_stability', 'employee_count'
                ]
                
                # Only include columns that exist
                existing_cols = [col for col in business_cols if col in business_features.columns]
                if existing_cols:
                    combined_features = pd.concat([combined_features, business_features[existing_cols]], axis=1)
            
            if 'credit_history' in X:
                credit_extractor = CreditHistoryFeatureExtractor()
                credit_features = credit_extractor.transform(X['credit_history'])
                
                # Select relevant columns
                credit_cols = [
                    'payment_reliability', 'credit_utilization', 'debt_ratio',
                    'default_risk_score', 'previous_defaults', 'late_payments'
                ]
                
                # Only include columns that exist
                existing_cols = [col for col in credit_cols if col in credit_features.columns]
                if existing_cols:
                    combined_features = pd.concat([combined_features, credit_features[existing_cols]], axis=1)
            
            # Create interaction features
            if 'debt_to_assets' in combined_features.columns and 'company_age' in combined_features.columns:
                combined_features['debt_age_interaction'] = combined_features['debt_to_assets'] * (1 / (combined_features['company_age'] + 1))
                
            if 'return_on_assets' in combined_features.columns and 'industry_risk' in combined_features.columns:
                combined_features['industry_adjusted_roa'] = combined_features['return_on_assets'] / combined_features['industry_risk']
                
            if 'default_risk_score' in combined_features.columns and 'business_stability' in combined_features.columns:
                combined_features['stability_adjusted_risk'] = combined_features['default_risk_score'] / (combined_features['business_stability'] + 1)
            
            # Replace infinities and NaNs
            combined_features = combined_features.replace([np.inf, -np.inf], np.nan)
            combined_features = combined_features.fillna(combined_features.median())
            
        except Exception as e:
            logger.error(f"Error combining features: {str(e)}")
        
        return combined_features