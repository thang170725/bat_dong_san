import pandas as pd
from build_model import HousePricePredictor_v1
def processing():
    df = pd.read_csv('dataset/dataset.csv')
    
    predictor = HousePricePredictor_v1()
    
    X_train, X_test, y_train, y_test = predictor.preprocess(df)
    X_train_scaled, X_test_scaled = predictor.scale(X_train, X_test)
    
    predictor.train_linear_regression(X_train_scaled, y_train)
    mse, r2 = predictor.evaluate(X_test_scaled, y_test)
    
    print("mse:", mse, "r2:", r2)

    # Dự đoán giá
    price = predictor.predict(
        dia_diem='cau_giay',
        so_phong_ngu=3,
        dien_tich=120,
        loai_nha='can_ho',
        giay_to_phap_ly='so_do',
        vi_tri='thuan_tien',
        mat_tien='khac',
        tinh_trang_nha='moi',
        tang=1,
        mo_ta='khac'
    )
    print("Dự đoán giá:", price)

    print("Top feature ảnh hưởng:")
    for f, v in predictor.top_features():
        print(f"{f}: {v}")

processing()
