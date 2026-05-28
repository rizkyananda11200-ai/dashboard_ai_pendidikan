import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Membaca dataset
df = pd.read_csv("data/data.csv")

# Menghapus kolom kosong
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Menghapus data kosong
df = df.dropna()

# Mengambil kolom numerik
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

# Menentukan fitur
X = df[numeric_columns]

# Membuat kategori sederhana
target_column = numeric_columns[0]

df["kategori"] = [
    "Layak"
    if x > df[target_column].mean()
    else "Kurang Layak"
    for x in df[target_column]
]

# Target
y = df["kategori"]

# Encode label
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Membagi data training dan testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Membuat model
model = RandomForestClassifier()

# Training model
model.fit(X_train, y_train)

# Simpan model
joblib.dump(model, "model.pkl")

print("Model berhasil dibuat!")