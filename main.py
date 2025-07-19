# file này dùng để dự đoán
import pandas as pd
from model.modelV1 import ModelV1
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    # Khai báo
    model_v1 = ModelV1()

    # Lấy dataset
    df = pd.read_csv('dataset/dataset.csv')

    # Tiền xử lý
    labels_one_hot = [       
        'loai_nha', 
        'giay_to_phap_ly', 
        'vi_tri', 
        'mat_tien', 
        'tinh_trang_nha',
        'mo_ta'
    ]
    one_hot_data = model_v1.one_hot_encode(df, labels_one_hot) 

    labels_encode = [
        'dia_diem'
    ]
    df_final = model_v1.label_encode(one_hot_data, labels_encode)

    X = df_final.drop('gia', axis=1)
    y = df_final['gia']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train_scaled = model_v1.fit_transfrom(X_train)
    X_test_scaled = model_v1.transform(X_test)

    model = model_v1.train_linear_regression(X_train_scaled, y_train)

    mse, r2 = model_v1.evaluate(X_test_scaled, y_test)
    print(mse, r2)
# X = df_final.drop('gia', axis=1)   # 'gia' là cột giá trị cần dự đoán
# y = df_final['gia']
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42)
# # print(X_test)
# # print(X_train.shape)
# # print(y_train.shape)
# # print(X_train.columns)
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# linear = ModelV1()

# model = linear.train_linear_regression(X_train_scaled, y_train)
# mse, r2 = linear.evaluate(X_test_scaled, y_test)

#


# # from test import HousePriceModel
# # 
# # # Giả sử đã train rồi
# # model = HousePriceModel()
# # 
# # X, y = model.encode_features(df)
# # X_train, X_test, y_train, y_test = model.train_test_split(X, y)
# # model.train_model(X_train, y_train)

# # # Dự đoán input mới
# # input_data = {
# #     'dia_diem': 'bac_tu_liem',
# #     'so_phong_ngu': 3,
# #     'dien_tich': 80,
# #     'loai_nha': 'can_ho',
# #     'giay_to_phap_ly': 'so_do',
# #     'vi_tri': 'thuan_tien',
# #     'mat_tien': 'khac',
# #     'tinh_trang_nha': 'moi',
# #     'tang': 1,
# #     'mo_ta': 'khac'
# # }

# # predicted_price = model.predict_one(input_data)
# # print("Giá dự đoán:", predicted_price)
# import pandas as pd
# from bat_dong_san.model.modelV1 import HousePricePredictor_v1

# def processing():
#     df = pd.read_csv('dataset/dataset.csv')
    
#     predictor = HousePricePredictor_v1()
    
#     X_train, X_test, y_train, y_test = predictor.preprocess(df)
#     X_train_scaled, X_test_scaled = predictor.scale(X_train, X_test)
    
#     predictor.train_linear_regression(X_train_scaled, y_train)
#     mse, r2 = predictor.evaluate(X_test_scaled, y_test)
    
#     print("mse:", mse, "r2:", r2)

#     # Dự đoán giá
#     price = predictor.predict(
#         dia_diem='bac_tu_liem',
#         so_phong_ngu=3,
#         dien_tich=80,
#         loai_nha='can_ho',
#         giay_to_phap_ly='so_do',
#         vi_tri='thuan_tien',
#         mat_tien='khac',
#         tinh_trang_nha='moi',
#         tang=1,
#         mo_ta='khac'
#     )
#     print("Dự đoán giá:", price)

#     print("Top feature ảnh hưởng:")
#     for f, v in predictor.top_features():
#         print(f"{f}: {v}")

# processing()
# #from flask import Flask, request, jsonify
# import joblib
# import bat_dong_san.model.modelV1 as modelV1
# import pandas as pd
# import sys

# def processing():
#     df = pd.read_csv('dataset/dataset.csv')

#     X_train, X_test, y_train, y_test, feature_columns, le = model.train_test_encoder(df)

#     X_train_scaler, X_test_scaler, scaler = model.scaler_data(X_train, X_test)

#     model = model.container_model(X_train_scaler, y_train)

#     mse, r2 = model.evaluate_model(model, X_test_scaler, y_test)
#     print('mse: ', mse, 'r2: ', r2)

#     predict_price = model.new_predict(
#         model=model,
#         scaler=scaler,
#         le=le,
#         feature_columns=feature_columns,
#         dia_diem='bac_tu_liem',
#         so_phong_ngu=3,
#         dien_tich=120,
#         loai_nha='can_ho',
#         giay_to_phap_ly='so_do',
#         vi_tri='thuan_tien',
#         mat_tien='khac',
#         tinh_trang_nha='moi',
#         tang=1,
#         mo_ta='khac'
#     )
#     print("Dự đoán giá:", predict_price)


    
#     top_f = model.top_features(model, feature_columns, 5)
#     print(top_f)
# processing()


# sys.exit()
# app = Flask(__name__)

# # Load model và các đối tượng đã fit
# modelV1 = joblib.load("model.pkl")
# scaler = joblib.load("scaler.pkl")
# le = joblib.load("label_encoder.pkl")
# feature_columns = joblib.load("feature_columns.pkl")  # danh sách tên cột

# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.get_json()  # đọc JSON gửi lên
#         # ✅ gọi lại hàm new_predict bạn đã viết
#         predicted_price = modelV1.new_predict(
#             model=modelV1,
#             scaler=scaler,
#             le=le,
#             feature_columns=feature_columns,
#             dia_diem=data["dia_diem"],
#             so_phong_ngu=data["so_phong_ngu"],
#             dien_tich=data["dien_tich"],
#             loai_nha=data["loai_nha"],
#             giay_to_phap_ly=data["giay_to_phap_ly"],
#             khung_canh=data["khung_canh"],
#             mat_tien=data["mat_tien"],
#             tinh_trang_nha=data["tinh_trang_nha"],
#             tang=data["tang"]
#         )

#         return jsonify({"predicted_price": round(predicted_price, 2)})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)