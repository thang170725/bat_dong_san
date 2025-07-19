import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from model.data_preprocessor import DataPreprocessor
import sys

class Model:
    def __init__(self):
        self.model = None
        self.encoder = None
    
    # Encode những feature có thứ tự rõ ràng
    def ordinal_encode_feature(self, df_input, cat_cols=[
        'dia_diem', 
        'loai_nha', 
        'giay_to_phap_ly', 
        'vi_tri', 
        'tinh_trang_nha', 
        'mo_ta']):
        df= df_input.copy()

        # Tạo categories
        categories = [
            [
                "bac_tu_liem,"
            ],
            ["can_ho", "can_ho_cao_cap", "nha_dat", "biet_thu"],
            ["khac", "hop_dong_mua_ban", "so_do"],
            ["thuan_tien", "khu_vuc_phat_trien", "canh_song", "canh_ho", "can_goc"],
            ["cu", "binh_thuong", "moi"],
            ["ban_gap", "khac"]
        ]

        # Khởi tạo encoder
        self.encoder = OrdinalEncoder(
            categories=categories,
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )

        # Fit encoder và biến đổi
        df[cat_cols] = self.encoder.fit_transform(df[cat_cols])

        # Tách features và label
        X = df.drop(columns=['gia'])
        y = df['gia']
        return X, y

    def train_test_split(self, X, y, test_size=0.2):
        return train_test_split(X, y, test_size=test_size, random_state=42)

    def train_model(self, X_train, y_train):
        self.model = RandomForestRegressor(random_state=42)
        self.model.fit(X_train, y_train)

    def train_model_xgboost(self, X_train, y_train):
        self.model = XGBRegressor()
        self.model.fit(X_train, y_train)

    def predict_one(self, input_dict):
        cat_cols = ['dia_diem', 'loai_nha', 'giay_to_phap_ly', 'vi_tri', 'tinh_trang_nha', 'mo_ta']
        input_df = pd.DataFrame([input_dict])
        input_df[cat_cols] = self.encoder.transform(input_df[cat_cols])
        return self.model.predict(input_df)[0]
    
    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return mse, r2
    
    def top_features(self, feature_columns, top_n=5):
        if self.model is None:
            raise ValueError("Model chưa được huấn luyện")

        # Dùng feature_importances_ cho RandomForest
        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
        else:
            raise ValueError("Mô hình không hỗ trợ feature_importances_ (chỉ RandomForest, Tree, ...)")

        # Sắp xếp và lấy top_n
        idx = importances.argsort()[::-1][:top_n]
        return [(feature_columns[i], importances[i]) for i in idx]
    
    def remove_outlier_iqr(self, df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return df[(df[column] >= lower) & (df[column] <= upper)]
    
    def count_value_other(self, df, columns_name):
        return df[columns_name].nunique()

# ================== Dùng thử ==================
if __name__ == "__main__":
    # 1. Load dữ liệu
    df = pd.read_csv('dataset/dataset1.csv')
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    
    # # 2. Tiền xử  lý
    # preprocessor = DataPreprocessor()
    # preprocessor.load(df)
    # preprocessor.process_mat_tien()
    # df = preprocessor.get_processed_data()
    feature_columns = df.columns.tolist()

    model = Model()
    X, y = model.ordinal_encode_feature(df)

    X_train, X_test, y_train, y_test = model.train_test_split(X, y)
    model.train_model_xgboost(X_train, y_train)

    # 6. Đánh giá
    mse, r2 = model.evaluate(X_test, y_test)
    print('mse: ', mse)
    print('r2_score: ', r2)

    # dự đoán
    predict_data = {
        'dia_diem': 'bac_tu_liem',
        'so_phong_ngu': 5,
        'dien_tich': 300,
        'loai_nha': 'biet_thu',
        'giay_to_phap_ly': 'hop_dong_mua_ban',
        'vi_tri': 'can_goc',
        'mat_tien': 30,
        'tinh_trang_nha': 'khac',
        'tang': 2,
        'mo_ta': 'ban_gap',
#         'mat_tien_numeric': 12,   # Vì không yêu cầu mặt tiền
#         'mat_tien_khac': 0       # Đánh dấu đây là 'khác'
        }
    
    predict_price = model.predict_one(predict_data)
    print("Dự đoán giá:", predict_price)

    top_feature = model.top_features(feature_columns, top_n=5)
    print("top features: ", top_feature)
# df = df.drop(columns=['mat_tien'])  # XGBoost không chấp nhận object


# # 3. Loại bỏ outlier
# model = ModelV2()
# df = model.remove_outlier_iqr(df, 'dien_tich')
# df = model.remove_outlier_iqr(df, 'gia')

# # 4. Tạo features
# X, y = model.encode_features(df)
# # ✅ Thêm cột mặt tiền số và nhị phân vào feature
# X['mat_tien_numeric'] = df['mat_tien_numeric']
# X['mat_tien_khac'] = df['mat_tien_khac']

# # 5. train/test split
# X_train, X_test, y_train, y_test = model.train_test_split(X, y, test_size=0.2)
# model.train_model_xgboost(X_train, y_train)



# # 7. Dự đoán 


# # # Lưu ý: cần thêm thủ công các cột mới vào input
# predict_data['mat_tien_numeric'] = 12
# predict_data['mat_tien_khac'] = 0



