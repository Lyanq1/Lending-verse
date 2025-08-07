"""
Data preprocessing module for credit scoring system.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """
    Class for preprocessing financial and business data for credit scoring.
    """
    
    def __init__(self):
        """Initialize the preprocessor with default transformers."""
        self.numerical_transformer = None
        self.categorical_transformer = None
        self.preprocessor = None
        self.numerical_features = None
        self.categorical_features = None
        
    def fit(self, data, numerical_features=None, categorical_features=None):
        """
        Fit the preprocessor to the data.
        
        Args:
            data (pd.DataFrame): Input data
            numerical_features (list): List of numerical feature names
            categorical_features (list): List of categorical feature names
        
        Returns:
            self: Fitted preprocessor
        """
        logger.info("Fitting data preprocessor")
        
        # If features not specified, infer from data types
        if numerical_features is None:
            self.numerical_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
        else:
            self.numerical_features = numerical_features
            
        if categorical_features is None:
            self.categorical_features = data.select_dtypes(include=['object', 'category']).columns.tolist()
        else:
            self.categorical_features = categorical_features
        
        logger.info(f"Numerical features: {self.numerical_features}")
        logger.info(f"Categorical features: {self.categorical_features}")
        
        # Create transformers for numerical and categorical data
        self.numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        self.categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Combine transformers in a column transformer
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', self.numerical_transformer, self.numerical_features),
                ('cat', self.categorical_transformer, self.categorical_features)
            ])
        
        # Fit the preprocessor
        self.preprocessor.fit(data)
        
        return self
    
    def transform(self, data):
        """
        Transform data using the fitted preprocessor.
        
        Args:
            data (pd.DataFrame): Input data to transform
            
        Returns:
            np.ndarray: Transformed data
        """
        logger.info("Transforming data")
        
        if self.preprocessor is None:
            raise ValueError("Preprocessor has not been fitted. Call fit() first.")
        
        # Transform the data
        transformed_data = self.preprocessor.transform(data)
        
        return transformed_data
    
    def fit_transform(self, data, numerical_features=None, categorical_features=None):
        """
        Fit the preprocessor and transform the data.
        
        Args:
            data (pd.DataFrame): Input data
            numerical_features (list): List of numerical feature names
            categorical_features (list): List of categorical feature names
            
        Returns:
            np.ndarray: Transformed data
        """
        return self.fit(data, numerical_features, categorical_features).transform(data)
    
    def get_feature_names(self):
        """
        Get feature names after transformation.
        
        Returns:
            list: Feature names
        """
        if self.preprocessor is None:
            raise ValueError("Preprocessor has not been fitted. Call fit() first.")
        
        # Get feature names from the column transformer
        num_features = self.numerical_features
        
        # Get one-hot encoded feature names
        cat_features = []
        if self.categorical_features:
            encoder = self.preprocessor.named_transformers_['cat'].named_steps['onehot']
            cat_features = [f"{feature}_{category}" for feature, categories in 
                           zip(self.categorical_features, encoder.categories_) 
                           for category in categories]
        
        return num_features + cat_features


class FinancialDataPreprocessor(DataPreprocessor):
    """
    Specialized preprocessor for financial statement data.
    """
    
    def __init__(self):
        """Initialize the financial data preprocessor."""
        super().__init__()
        
    def calculate_financial_ratios(self, financial_data):
        """
        Calculate financial ratios from financial statements.
        
        Args:
            financial_data (pd.DataFrame): Financial statement data
            
        Returns:
            pd.DataFrame: Data with additional financial ratios
        """
        logger.info("Calculating financial ratios")
        
        # Make a copy to avoid modifying the original data
        data = financial_data.copy()
        
        try:
            # Liquidity ratios
            if 'current_assets' in data.columns and 'current_liabilities' in data.columns:
                data['current_ratio'] = data['current_assets'] / data['current_liabilities']
                
            if 'cash' in data.columns and 'current_liabilities' in data.columns:
                data['cash_ratio'] = data['cash'] / data['current_liabilities']
            
            # Profitability ratios
            if 'net_income' in data.columns and 'total_assets' in data.columns:
                data['return_on_assets'] = data['net_income'] / data['total_assets']
                
            if 'net_income' in data.columns and 'total_equity' in data.columns:
                data['return_on_equity'] = data['net_income'] / data['total_equity']
                
            if 'gross_profit' in data.columns and 'revenue' in data.columns:
                data['gross_margin'] = data['gross_profit'] / data['revenue']
                
            if 'net_income' in data.columns and 'revenue' in data.columns:
                data['net_profit_margin'] = data['net_income'] / data['revenue']
            
            # Solvency ratios
            if 'total_debt' in data.columns and 'total_assets' in data.columns:
                data['debt_to_assets'] = data['total_debt'] / data['total_assets']
                
            if 'total_debt' in data.columns and 'total_equity' in data.columns:
                data['debt_to_equity'] = data['total_debt'] / data['total_equity']
            
            # Efficiency ratios
            if 'revenue' in data.columns and 'total_assets' in data.columns:
                data['asset_turnover'] = data['revenue'] / data['total_assets']
                
            if 'cost_of_goods_sold' in data.columns and 'inventory' in data.columns:
                data['inventory_turnover'] = data['cost_of_goods_sold'] / data['inventory']
                
            # Replace infinities and NaNs
            data = data.replace([np.inf, -np.inf], np.nan)
            
        except Exception as e:
            logger.error(f"Error calculating financial ratios: {str(e)}")
        
        return data
    
    def fit_transform(self, data, calculate_ratios=True, numerical_features=None, categorical_features=None):
        """
        Fit the preprocessor and transform the financial data.
        
        Args:
            data (pd.DataFrame): Financial statement data
            calculate_ratios (bool): Whether to calculate financial ratios
            numerical_features (list): List of numerical feature names
            categorical_features (list): List of categorical feature names
            
        Returns:
            np.ndarray: Transformed data
        """
        if calculate_ratios:
            data = self.calculate_financial_ratios(data)
            
        return super().fit_transform(data, numerical_features, categorical_features)


class BusinessDataPreprocessor(DataPreprocessor):
    """
    Specialized preprocessor for business profile data.
    """
    
    def __init__(self):
        """Initialize the business data preprocessor."""
        super().__init__()
        
    def encode_industry(self, data, industry_column='industry'):
        """
        Encode industry information with risk factors.
        
        Args:
            data (pd.DataFrame): Business data
            industry_column (str): Name of the industry column
            
        Returns:
            pd.DataFrame: Data with industry risk factors
        """
        logger.info("Encoding industry information")
        
        # Make a copy to avoid modifying the original data
        data_copy = data.copy()
        
        # Define industry risk mappings (these would be based on historical data)
        industry_risk = {
            'technology': 3,
            'healthcare': 2,
            'finance': 4,
            'retail': 5,
            'manufacturing': 4,
            'real_estate': 5,
            'education': 2,
            'energy': 4,
            'transportation': 3,
            'agriculture': 3,
            'construction': 5,
            'hospitality': 6,
            'entertainment': 5
        }
        
        # Apply risk factor if industry column exists
        if industry_column in data_copy.columns:
            data_copy['industry_risk'] = data_copy[industry_column].str.lower().map(industry_risk).fillna(4)
        
        return data_copy
    
    def encode_company_age(self, data, founded_year_column='founded_year'):
        """
        Calculate company age and encode it as a risk factor.
        
        Args:
            data (pd.DataFrame): Business data
            founded_year_column (str): Name of the founded year column
            
        Returns:
            pd.DataFrame: Data with company age features
        """
        logger.info("Encoding company age")
        
        # Make a copy to avoid modifying the original data
        data_copy = data.copy()
        
        if founded_year_column in data_copy.columns:
            # Calculate company age
            current_year = pd.Timestamp.now().year
            data_copy['company_age'] = current_year - data_copy[founded_year_column]
            
            # Create age brackets
            data_copy['age_bracket'] = pd.cut(
                data_copy['company_age'],
                bins=[0, 2, 5, 10, 20, float('inf')],
                labels=['startup', 'early_stage', 'established', 'mature', 'legacy']
            )
            
            # Create age risk factor (higher age = lower risk)
            data_copy['age_risk'] = pd.cut(
                data_copy['company_age'],
                bins=[0, 2, 5, 10, 20, float('inf')],
                labels=[5, 4, 3, 2, 1]
            ).astype(int)
        
        return data_copy
    
    def fit_transform(self, data, encode_industries=True, encode_age=True, 
                     numerical_features=None, categorical_features=None):
        """
        Fit the preprocessor and transform the business data.
        
        Args:
            data (pd.DataFrame): Business data
            encode_industries (bool): Whether to encode industry information
            encode_age (bool): Whether to encode company age
            numerical_features (list): List of numerical feature names
            categorical_features (list): List of categorical feature names
            
        Returns:
            np.ndarray: Transformed data
        """
        processed_data = data.copy()
        
        if encode_industries:
            processed_data = self.encode_industry(processed_data)
            
        if encode_age:
            processed_data = self.encode_company_age(processed_data)
            
        return super().fit_transform(processed_data, numerical_features, categorical_features)