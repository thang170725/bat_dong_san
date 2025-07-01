import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

class HousePricePredictor_v1:
    def __init__(self):
        self.le = LabelEncoder()
        self.feature_columns = []
        self.scaler = StandardScaler()
        self.model = None

    def preprocess(self, df):
        # lưu lại cột dia_diem trước khi one-hot để stratify
        stratify_col = df['dia_diem'].copy()

        # One-hot encode
        df_encoded = pd.get_dummies(data=df, columns=[
            'dia_diem', 'loai_nha', 'giay_to_phap_ly',
            'vi_tri', 'mat_tien', 'mo_ta'
        ], prefix="encode", dtype=int) 

        # Label encode
        df_encoded['encode_tinh_trang_nha'] = self.le.fit_transform(df_encoded['tinh_trang_nha'])

        # bỏ cột tinh_trang_nha
        df_encoded = df_encoded.drop('tinh_trang_nha', axis=1)

        # chia tập dữ liệu - features/label
        X = df_encoded.drop('gia', axis=1) 
        y = df_encoded['gia']

        #train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.15, stratify=stratify_col, random_state=42
        )
        
        # Mảng chứa tên các feature
        self.feature_columns = X_train.columns.tolist()
        
        return X_train, X_test, y_train, y_test

    def scale(self, X_train, X_test):
        # tính trung bình và chuẩn hóa dữ liệu
        # tính mean, std trên X_train, rồi chuẩn hóa
        X_train_scaled = self.scaler.fit_transform(X_train) 

        # dùng mean, std đã học ở trên để chuẩn hóa X_test
        X_test_scaled = self.scaler.transform(X_test) 
        # chỉ gọi transform không sử dụng fit lại ở test, 
        # điều này tránh rò rỉ thông tin từ test set vào mô hình, rất quan trọng trong thực tế
        return X_train_scaled, X_test_scaled

    def train_linear_regression(self, X, y, remove_outlier=True, threshold_scale=1.5):
        # Huấn luyện mô hình lần đầu
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        # Tính phần sai số (residuals)
        residuals = np.abs(y - y_pred)
        mse = mean_squared_error(y, y_pred)

        if remove_outlier:
            # Lọc những dòng có sai số thấp hơn ngưỡng
            threshold = threshold_scale * mse
            mask = residuals < threshold

            # Lọc lại X, y rồi huấn luyện mô hình lần 2
            X_clean = X[mask]
            y_clean = y[mask]

            model = LinearRegression()
            model.fit(X_clean, y_clean)

            print(f"Removed {len(X) - len(X_clean)} samples with residual > {threshold:.2f}")
        self.model = model
        return model

    def evaluate(self, X_test_scaled, y_test):
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return mse, r2

    def predict(self, **kwargs):
        if self.model is None or not hasattr(self.scaler, "mean_"):
            raise ValueError("Model hoặc scaler chưa được huấn luyện.")

        # Tạo DataFrame input 1 dòng
        input_df = pd.DataFrame([kwargs])

        # One-hot encode 
        input_df = pd.get_dummies(input_df, columns=[
            'dia_diem', 'loai_nha', 'giay_to_phap_ly', 
            'vi_tri', 'mat_tien', 'mo_ta'
        ], prefix="encode", dtype=int)

        # label encoder
        input_df['encode_tinh_trang_nha'] = self.le.transform(input_df['tinh_trang_nha'])
        input_df = input_df.drop('tinh_trang_nha', axis=1)

        # Loại bỏ cột bị trùng tên
        input_df = input_df.loc[:, ~input_df.columns.duplicated()]

        # Đảm bảo đủ cột và đúng thứ tự
        input_df = input_df.reindex(columns=self.feature_columns, fill_value=0)

        # scaler
        input_scaled = self.scaler.transform(input_df)

        # Debug để kiểm tra
        print("Input data after scaling:", input_scaled)

        # Dự đoán
        predicted_price = self.model.predict(input_scaled)

        print("Model coefficients:", self.model.coef_)
        print("Intercept:", self.model.intercept_)
        print("Cột input sau chuẩn hóa:", input_df.columns.tolist())
        print("Số cột:", len(input_df.columns), "vs", len(self.feature_columns))

        return predicted_price[0]


    def top_features(self, top_n=5):
        if self.model is None:
            raise ValueError("Model chưa được huấn luyện")
        
        coefs = self.model.coef_
        idx = np.argsort(np.abs(coefs))[::-1][:top_n]

        return [(self.feature_columns[i], coefs[i]) for i in idx]
