#from connection import fetch_dataframe
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
def train_test_encoder(df):
    # thêm tập dữ liệu
    #query = 'SELECT * FROM bat_dong_san;'
    #df = fetch_dataframe(query)

    # mã hóa bằng one-hot encoding
    one_hot = pd.get_dummies(data=df, columns=['dia_diem', 'loai_nha', 'giay_to_phap_ly', 'vi_tri', 'mo_ta'], prefix="encode", dtype=int) 

    # sử dụng label encoding
    le = LabelEncoder()
    one_hot['encode_tinh_trang_nha'] = le.fit_transform(one_hot['tinh_trang_nha'])

    # bỏ cột tinh_trang_nha và cột id
    one_hot = one_hot.drop('tinh_trang_nha', axis=1)

    # chia tập dữ liệu - features/label
    X = one_hot.drop('gia', axis=1) 
    y = one_hot['gia']

    #train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1 ,random_state=42)
    feature_columns = X_train.columns.tolist()
    return X_train, X_test, y_train, y_test, feature_columns, le

def scaler_data(X_train, X_test):
    # tính trung bình và chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train) # tính mean, std trên X_train, rồi chuẩn hóa
    X_test_scaled = scaler.transform(X_test) # dùng mean, std đã học ở trên để chuẩn hóa X_test
    #chỉ gọi transform không sử dụng fit lại ở test, điều này tránh rò rỉ thông tin từ test set vào mô hình, rất quan trọng trong thực tế
    return X_train_scaled, X_test_scaled, scaler

def container_model(X, y):
    # huấn luyện mô hình
    model = LinearRegression()
    model.fit(X, y)
    return model

def evaluate_model(model, X_test_scaled, y_test):
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

def new_predict(model, scaler, le, feature_columns, dia_diem, so_phong_ngu, dien_tich, loai_nha, giay_to_phap_ly, vi_tri, mat_tien, tinh_trang_nha, tang, mo_ta):
    if not hasattr(le, "classes_"):
        raise ValueError("LabelEncoder chưa được fit.")
    if not hasattr(scaler, "mean_") or not hasattr(scaler, "scale_"):
        raise ValueError("StandardScaler chưa được fit.")

    input_data = pd.DataFrame([{# tạo dataframe mới với đầu vào 1 dòng dữ liệu
        'dia_diem': dia_diem,
        'so_phong_ngu': so_phong_ngu,
        'dien_tich': dien_tich,
        'loai_nha': loai_nha,
        'giay_to_phap_ly': giay_to_phap_ly,
        'vi_tri': vi_tri,
        'mat_tien': mat_tien,
        'tinh_trang_nha': tinh_trang_nha,
        'tang': tang,
        'mo_ta': mo_ta
    }])

    # sử dụng one-hot encoding cho dự đoán với đặc trưng mới
    input_data = pd.get_dummies(data=input_data, columns=['dia_diem', 'loai_nha', 'giay_to_phap_ly', 'vi_tri', 'mo_ta'], prefix="encode", dtype=int) 

    # sử dụng label encoding
    input_data['encode_tinh_trang_nha'] = le.transform(input_data['tinh_trang_nha'])

    # bỏ cột tinh_trang_nha và id
    input_data = input_data.drop('tinh_trang_nha', axis=1) 

    # bảo đảm có đủ tất cả các cột như X_train (bù thiếu bằng 0)
    for col in feature_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    # sắp xếp đúng thứ tự cột
    input_data = input_data[feature_columns]

    # chuẩn hóa
    input_scaled = scaler.transform(input_data)

    print("Input data after scaling:", input_scaled)

    predicted_price = model.predict(input_scaled)

    print("Model coefficients:", model.coef_)
    print("Intercept:", model.intercept_)
    return predicted_price[0]

def top_features(model, feature_name, top_n):
    coefs = model.coef_
    sorted_idx = np.argsort(np.abs(coefs))[::-1]

    top = []
    for i in range(top_n):
        idx = sorted_idx[i]
        top.append((feature_name[idx], coefs[idx]))   
    return top
