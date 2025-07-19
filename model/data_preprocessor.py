import pandas as pd

class DataPreprocessor:
    def __init__(self):
        self.df = None

    def load(self, df):
        self.df = df.copy()

    def process_mat_tien_xgboost(self):
        if self.df is None:
            raise ValueError("Chưa load dữ liệu!")

        self.df['mat_tien_numeric'] = pd.to_numeric(self.df['mat_tien'], errors='coerce')
        self.df['mat_tien_khac'] = self.df['mat_tien_numeric'].isna().astype(int)

    def get_processed_data(self):
        return self.df

# Test 
if __name__ == "__main__":
    data = {
        'mat_tien': [13, "khác"]
    }
    df = pd.DataFrame(data)

    data_preprocess = DataPreprocessor()
    data_preprocess.load(df)
    data_preprocess.process_mat_tien_xgboost()

    new_df = data_preprocess.get_processed_data()
    print(new_df)