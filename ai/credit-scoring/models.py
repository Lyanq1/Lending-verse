"""
Credit scoring models for LendingVerse platform.
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, ClassifierMixin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreditScoreClassifier(BaseEstimator, ClassifierMixin):
    """
    Ensemble classifier for credit scoring.
    """
    
    def __init__(self, model_type='ensemble'):
        """
        Initialize the credit score classifier.
        
        Args:
            model_type (str): Type of model to use
                - 'ensemble': Ensemble of multiple models (default)
                - 'rf': Random Forest
                - 'gb': Gradient Boosting
                - 'lr': Logistic Regression
                - 'nn': Neural Network
        """
        self.model_type = model_type
        self.models = {}
        self.feature_importances_ = None
        self.classes_ = None
    
    def fit(self, X, y):
        """
        Fit the classifier to the training data.
        
        Args:
            X (pd.DataFrame): Training features
            y (pd.Series): Target variable (credit score categories)
            
        Returns:
            self: Fitted classifier
        """
        logger.info(f"Training {self.model_type} credit score classifier")
        
        # Store classes
        self.classes_ = np.unique(y)
        
        # Train models based on model_type
        if self.model_type == 'ensemble' or self.model_type == 'rf':
            logger.info("Training Random Forest model")
            rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            rf_model.fit(X, y)
            self.models['rf'] = rf_model
        
        if self.model_type == 'ensemble' or self.model_type == 'gb':
            logger.info("Training Gradient Boosting model")
            gb_model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
            gb_model.fit(X, y)
            self.models['gb'] = gb_model
        
        if self.model_type == 'ensemble' or self.model_type == 'lr':
            logger.info("Training Logistic Regression model")
            lr_model = LogisticRegression(
                C=1.0,
                penalty='l2',
                solver='lbfgs',
                multi_class='multinomial',
                max_iter=1000,
                random_state=42,
                n_jobs=-1
            )
            lr_model.fit(X, y)
            self.models['lr'] = lr_model
        
        if self.model_type == 'ensemble' or self.model_type == 'nn':
            logger.info("Training Neural Network model")
            nn_model = MLPClassifier(
                hidden_layer_sizes=(100, 50),
                activation='relu',
                solver='adam',
                alpha=0.0001,
                batch_size='auto',
                learning_rate='adaptive',
                max_iter=500,
                random_state=42
            )
            nn_model.fit(X, y)
            self.models['nn'] = nn_model
        
        # Calculate feature importances (if available)
        if 'rf' in self.models:
            self.feature_importances_ = self.models['rf'].feature_importances_
        elif 'gb' in self.models:
            self.feature_importances_ = self.models['gb'].feature_importances_
        
        return self
    
    def predict(self, X):
        """
        Predict credit score categories.
        
        Args:
            X (pd.DataFrame): Features
            
        Returns:
            np.ndarray: Predicted credit score categories
        """
        if not self.models:
            raise ValueError("Model has not been trained. Call fit() first.")
        
        # Get predictions from each model
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X)
        
        # If using a single model, return its predictions
        if self.model_type != 'ensemble':
            return list(predictions.values())[0]
        
        # For ensemble, use voting
        # Convert predictions to one-hot encoding
        one_hot = {}
        for name, preds in predictions.items():
            one_hot[name] = np.zeros((len(preds), len(self.classes_)))
            for i, pred in enumerate(preds):
                class_idx = np.where(self.classes_ == pred)[0][0]
                one_hot[name][i, class_idx] = 1
        
        # Average the predictions
        ensemble_probs = np.zeros((len(X), len(self.classes_)))
        for name, oh in one_hot.items():
            ensemble_probs += oh
        ensemble_probs /= len(self.models)
        
        # Get the class with highest probability
        ensemble_preds = self.classes_[np.argmax(ensemble_probs, axis=1)]
        
        return ensemble_preds
    
    def predict_proba(self, X):
        """
        Predict class probabilities.
        
        Args:
            X (pd.DataFrame): Features
            
        Returns:
            np.ndarray: Predicted class probabilities
        """
        if not self.models:
            raise ValueError("Model has not been trained. Call fit() first.")
        
        # Get probability predictions from each model
        probas = {}
        for name, model in self.models.items():
            probas[name] = model.predict_proba(X)
        
        # If using a single model, return its probabilities
        if self.model_type != 'ensemble':
            return list(probas.values())[0]
        
        # For ensemble, average the probabilities
        ensemble_proba = np.zeros_like(list(probas.values())[0])
        for proba in probas.values():
            ensemble_proba += proba
        ensemble_proba /= len(self.models)
        
        return ensemble_proba
    
    def get_feature_importance(self, feature_names=None):
        """
        Get feature importances.
        
        Args:
            feature_names (list): List of feature names
            
        Returns:
            pd.DataFrame: Feature importances
        """
        if self.feature_importances_ is None:
            raise ValueError("Feature importances not available. Model may not support feature importances.")
        
        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(len(self.feature_importances_))]
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.feature_importances_
        })
        
        return importance_df.sort_values('importance', ascending=False)
    
    def save_model(self, model_dir):
        """
        Save the model to disk.
        
        Args:
            model_dir (str): Directory to save the model
        """
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        model_path = os.path.join(model_dir, f"credit_score_model_{self.model_type}.pkl")
        joblib.dump(self, model_path)
        logger.info(f"Model saved to {model_path}")
    
    @classmethod
    def load_model(cls, model_path):
        """
        Load a model from disk.
        
        Args:
            model_path (str): Path to the saved model
            
        Returns:
            CreditScoreClassifier: Loaded model
        """
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        return model


class CreditScoreTrainer:
    """
    Trainer for credit scoring models.
    """
    
    def __init__(self, model_type='ensemble'):
        """
        Initialize the trainer.
        
        Args:
            model_type (str): Type of model to train
        """
        self.model_type = model_type
        self.model = None
        self.feature_names = None
    
    def train(self, X, y, feature_names=None, test_size=0.2, random_state=42):
        """
        Train a credit scoring model.
        
        Args:
            X (pd.DataFrame): Features
            y (pd.Series): Target variable (credit score categories)
            feature_names (list): List of feature names
            test_size (float): Proportion of data to use for testing
            random_state (int): Random seed for reproducibility
            
        Returns:
            dict: Training results
        """
        logger.info(f"Training credit scoring model with {self.model_type} algorithm")
        
        # Store feature names
        self.feature_names = feature_names if feature_names is not None else X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Create and train model
        self.model = CreditScoreClassifier(model_type=self.model_type)
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        classification_rep = classification_report(y_test, y_pred, output_dict=True)
        
        try:
            y_proba = self.model.predict_proba(X_test)
            roc_auc = roc_auc_score(
                pd.get_dummies(y_test), y_proba, multi_class='ovr', average='macro'
            )
        except:
            roc_auc = None
        
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        # Get feature importances if available
        try:
            feature_importance = self.model.get_feature_importance(self.feature_names)
            top_features = feature_importance.head(10).to_dict('records')
        except:
            top_features = None
        
        # Return results
        results = {
            'model_type': self.model_type,
            'classification_report': classification_rep,
            'roc_auc_score': roc_auc,
            'confusion_matrix': conf_matrix.tolist(),
            'top_features': top_features
        }
        
        logger.info(f"Model training completed. Accuracy: {classification_rep['accuracy']:.4f}")
        
        return results
    
    def save_model(self, model_dir):
        """
        Save the trained model.
        
        Args:
            model_dir (str): Directory to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        self.model.save_model(model_dir)
    
    @classmethod
    def load_model(cls, model_path):
        """
        Load a trained model.
        
        Args:
            model_path (str): Path to the saved model
            
        Returns:
            CreditScoreTrainer: Trainer with loaded model
        """
        model = CreditScoreClassifier.load_model(model_path)
        trainer = cls(model_type=model.model_type)
        trainer.model = model
        return trainer


class DefaultProbabilityEstimator:
    """
    Estimator for loan default probability.
    """
    
    def __init__(self):
        """Initialize the default probability estimator."""
        self.model = None
    
    def train(self, X, y, test_size=0.2, random_state=42):
        """
        Train a default probability model.
        
        Args:
            X (pd.DataFrame): Features
            y (pd.Series): Target variable (1 for default, 0 for non-default)
            test_size (float): Proportion of data to use for testing
            random_state (int): Random seed for reproducibility
            
        Returns:
            dict: Training results
        """
        logger.info("Training default probability model")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Define model pipeline
        pipeline = Pipeline([
            ('classifier', GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=random_state
            ))
        ])
        
        # Define parameter grid for hyperparameter tuning
        param_grid = {
            'classifier__n_estimators': [50, 100, 200],
            'classifier__learning_rate': [0.01, 0.1, 0.2],
            'classifier__max_depth': [3, 5, 7]
        }
        
        # Perform grid search
        grid_search = GridSearchCV(
            pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        # Get best model
        self.model = grid_search.best_estimator_
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]  # Probability of default
        
        # Calculate metrics
        classification_rep = classification_report(y_test, y_pred, output_dict=True)
        roc_auc = roc_auc_score(y_test, y_proba)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        # Return results
        results = {
            'best_params': grid_search.best_params_,
            'classification_report': classification_rep,
            'roc_auc_score': roc_auc,
            'confusion_matrix': conf_matrix.tolist()
        }
        
        logger.info(f"Default probability model training completed. ROC AUC: {roc_auc:.4f}")
        
        return results
    
    def predict_default_probability(self, X):
        """
        Predict the probability of default.
        
        Args:
            X (pd.DataFrame): Features
            
        Returns:
            np.ndarray: Predicted default probabilities
        """
        if self.model is None:
            raise ValueError("Model has not been trained. Call train() first.")
        
        return self.model.predict_proba(X)[:, 1]
    
    def save_model(self, model_path):
        """
        Save the model to disk.
        
        Args:
            model_path (str): Path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        joblib.dump(self.model, model_path)
        logger.info(f"Default probability model saved to {model_path}")
    
    @classmethod
    def load_model(cls, model_path):
        """
        Load a model from disk.
        
        Args:
            model_path (str): Path to the saved model
            
        Returns:
            DefaultProbabilityEstimator: Loaded model
        """
        estimator = cls()
        estimator.model = joblib.load(model_path)
        logger.info(f"Default probability model loaded from {model_path}")
        return estimator