from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd

class ModelV1:
    def __init__(self):
        self.feature_columns = []
        self.model = None
        self.label_encoders = {}
        self.scaler = StandardScaler()

    def one_hot_encode(self, df, cols):
        return pd.get_dummies(
            data=df, 
            columns=cols, 
            prefix="encode", 
            dtype=int
        )
    
    def label_encode(self, df, cols):
        df_encoded = df.copy()
        for col in cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col])
            self.label_encoders[col] = le
        return df_encoded
    
    def fit_transfrom(self, X_train):
        X_train_scaled = self.scaler.fit_transform(X_train) 
        return pd.DataFrame(
            X_train_scaled, 
            columns=X_train.columns, 
            index=X_train.index
        )
    
    def transform(self, X):
        X_scaled = self.scaler.transform(X) 
        return pd.DataFrame(
            X_scaled, 
            columns=X.columns, 
            index=X.index
        )

    def train_linear_regression(self, X_train, y_train):
        self.feature_columns = X_train.columns.tolist()
        model = LinearRegression()
        model.fit(X_train, y_train)
        self.model = model
        return model

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return mse, r2
    
    def predict(self, X_input):
        if self.model is None:
            raise ValueError("Model chưa được huấn luyện.")
        return self.model.predict(X_input)

    def top_features(self, top_n=5):
        if self.model is None:
            raise ValueError("Model chưa được huấn luyện")
        
        coefs = self.model.coef_
        idx = np.argsort(np.abs(coefs))[::-1][:top_n]

        return [(self.feature_columns[i], coefs[i]) for i in idx]