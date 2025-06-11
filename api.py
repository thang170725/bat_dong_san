#from flask import Flask, request, jsonify
import joblib
import build_model
import pandas as pd
import sys

def processing():
    df = pd.read_csv('./dataset.csv')

    X_train, X_test, y_train, y_test, feature_columns, le = build_model.train_test_encoder(df)

    X_train_scaler, X_test_scaler, scaler = build_model.scaler_data(X_train, X_test)

    model = build_model.container_model(X_train_scaler, y_train)

    mse, r2 = build_model.evaluate_model(model, X_test_scaler, y_test)
    print('mse: ', mse, 'r2: ', r2)

    predict_price = build_model.new_predict(model, scaler, le, feature_columns, 'bac_tu_liem', 2, 78, 'quy_can_ho', 'so_do', 'thuan_tien', 3, 'moi', 1, 'khac')
    print(predict_price)
    
    top_f = build_model.top_features(model, feature_columns, 5)
    print(top_f)
processing()


sys.exit()
app = Flask(__name__)

# Load model và các đối tượng đã fit
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
le = joblib.load("label_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")  # danh sách tên cột

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()  # đọc JSON gửi lên
        # ✅ gọi lại hàm new_predict bạn đã viết
        predicted_price = build_model.new_predict(
            model=model,
            scaler=scaler,
            le=le,
            feature_columns=feature_columns,
            dia_diem=data["dia_diem"],
            so_phong_ngu=data["so_phong_ngu"],
            dien_tich=data["dien_tich"],
            loai_nha=data["loai_nha"],
            giay_to_phap_ly=data["giay_to_phap_ly"],
            khung_canh=data["khung_canh"],
            mat_tien=data["mat_tien"],
            tinh_trang_nha=data["tinh_trang_nha"],
            tang=data["tang"]
        )

        return jsonify({"predicted_price": round(predicted_price, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
