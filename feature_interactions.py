# Import libraries
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# create a custom transformer for creating new feature interactions
class FeatureInteractions(BaseEstimator, TransformerMixin):
    
    # Initialize
    def __init__(self, weight_foreign=2.0, weight_sim_swap=2.5):
        self.weight_foreign = weight_foreign # 0.967 for 3.3% prevalence
        self.weight_sim_swap = weight_sim_swap # 0.99 for 1% prevalence
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        
        # Feature: Log-transformed amount (handles skewness)
        X["amount_log"] = np.log1p(X["amount"])

        # Feature: Night transaction flag (0-5 AM based on uniform night activity)
        X["night_transaction"] = (X["time_of_day"] == "Night").astype(int)

        # Feature: User transaction frequency (high-frequency users as potential fraud)
        X["transaction_frequency"] = X.groupby("user_id")["transaction_id"].transform("count")

        # Feature: Average amount per user (skewed distribution)
        X["avg_amount_per_user"] = X.groupby("user_id")["amount"].transform("mean")
        
        # Create weighted binary features
        X["weighted_foreign"] = X["is_foreign_number"] * self.weight_foreign
        X["weighted_sim_swap"] = X["is_sim_recently_swapped"] * self.weight_sim_swap

        # Combine into a risk score (optional)
        X["fraud_risk_score"] = X["weighted_foreign"] + X["weighted_sim_swap"]
        
        return X