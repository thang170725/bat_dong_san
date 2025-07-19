import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Đọc dữ liệu
df = pd.read_csv('dataset/dataset.csv')

# Hàm loại bỏ outlier bằng IQR
def remove_outlier_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Làm sạch dữ liệu
df_clean = remove_outlier_iqr(df, 'dien_tich')
df_clean = remove_outlier_iqr(df_clean, 'gia')

# Vẽ biểu đồ scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_clean, x='dien_tich', y='gia', hue='dia_diem', palette='Set2')

# Tùy chỉnh
plt.title("Mối quan hệ giữa diện tích và giá")
plt.xlabel("Diện tích (m2)")
plt.ylabel("Giá (tỷ)")
plt.legend(title='Địa điểm', loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()

# Lưu ảnh
plt.savefig('chart/scatter_plot.png')
plt.close()
