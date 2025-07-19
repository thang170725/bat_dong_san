from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from model.data_preprocessor import DataPreprocessor
from model.model import Model

app = Flask(__name__)
CORS(app)  # Cho phép truy cập từ frontend khác cổng

@app.route('/api/du-lieu', methods=['POST'])
def nhan_du_lieu():
    data = request.get_json()
    print("Dữ liệu nhận được:", data)

    predict_data = {
        'dia_diem': data['dia_diem']['value'],
        'so_phong_ngu': int(data['so_phong_ngu']['value']),
        'dien_tich': float(data['dien_tich']['value']),
        'loai_nha': data['loai_nha']['value'],
        'giay_to_phap_ly': data['giay_to_phap_ly']['value'],
        'vi_tri': data['vi_tri']['value'],
        'tinh_trang_nha': data['tinh_trang_nha']['value'],
        'tang': int(data['tang']['value']),
        'mo_ta': data['mo_ta']['value']
    }

    if data.get("mat_tien", {}).get("value") == "khac":
        predict_data['mat_tien_numeric'] = 0
        predict_data['mat_tien_khac'] = 1
    else:
        try:
            predict_data['mat_tien_numeric'] = float(data['mat_tien']['value'])
        except:
            predict_data['mat_tien_numeric'] = 0
        predict_data['mat_tien_khac'] = 0

    print("[DEBUG] Predict Data:", predict_data)

    # ================== Dùng thử ==================

    # 1. Load dữ liệu
    df = pd.read_csv('dataset/dataset1.csv')
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    # 2. Tiền xử  lý
    preprocessor = DataPreprocessor()
    preprocessor.load(df)
    preprocessor.process_mat_tien_xgboost()
    df = preprocessor.get_processed_data()
    feature_columns = df.columns.tolist()

    df = df.drop(columns=['mat_tien'])  # XGBoost không chấp nhận object


    # 3. Loại bỏ outlier
    model = Model()
    df = model.remove_outlier_iqr(df, 'dien_tich')
    df = model.remove_outlier_iqr(df, 'gia')

    # 4. Tạo features
    X, y = model.ordinal_encode_feature(df)
    # ✅ Thêm cột mặt tiền số và nhị phân vào feature
    X['mat_tien_numeric'] = df['mat_tien_numeric']
    X['mat_tien_khac'] = df['mat_tien_khac']

    # 5. train/test split
    X_train, X_test, y_train, y_test = model.train_test_split(X, y, test_size=0.2)
    model.train_model_xgboost(X_train, y_train)

    # 6. Đánh giá
    mse, r2 = model.evaluate(X_test, y_test)
    print('mse: ', mse)
    print('r2_score: ', r2)

    # Lưu ý: cần thêm thủ công các cột mới vào input
    predict_data['mat_tien_numeric'] = 0
    predict_data['mat_tien_khac'] = 1

    predict_price = model.predict_one(predict_data)
    predict_price = int(predict_price)*1000000000
    print("Dự đoán giá:", predict_price)

    top_feature = model.top_features(feature_columns, top_n=5)
    print("top features: ", top_feature)

    # convert np.float32 to float để jsonify không lỗi
    top_feature_json = [(key, float(val)) for key, val in top_feature]
    print(top_feature_json)

    return jsonify({
        "price": f"{predict_price} VND",
        "top_feature": top_feature_json
    })

# if __name__ == '__main__':
#     app.run(debug=True)

# Cuối file server.py
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # lấy PORT từ biến môi trường
    app.run(host='0.0.0.0', port=port)        # chạy trên địa chỉ public

