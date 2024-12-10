import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# Load and preprocess data
file_path = 'processed.csv'
data = pd.read_csv(file_path)

# Define mappings
category_mappings = {
    'gender': {0: 'Male', 1: 'Female'},
    'hypertension': {0: 'No', 1: 'Yes'},
    'heart_disease': {0: 'No', 1: 'Yes'},
    'smoking_status': {
        0: 'Never Smokes',
        1: 'Formerly Smokes',
        2: 'Smokes',
        3: 'Unknown'
    },
    'Residence_type': {0: 'Urban', 1: 'Rural'},
    'work_type': {
        0: 'Child',
        1: 'Never worked',
        2: 'Self-Employed',
        3: 'Private',
        4: 'Government employed'
    }
}

# Replace category values with mappings
for column, mapping in category_mappings.items():
    if column in data.columns:
        data[column] = data[column].replace(mapping)

# Define columns
numerical_columns = ['age', 'avg_glucose_level', 'bmi']
categorical_columns = ['gender', 'work_type', 'Residence_type', 'smoking_status', 'hypertension', 'heart_disease']

# Impute missing values
numerical_imputer = SimpleImputer(strategy='mean')
categorical_imputer = SimpleImputer(strategy='most_frequent')

data[numerical_columns] = numerical_imputer.fit_transform(data[numerical_columns])
data[categorical_columns] = categorical_imputer.fit_transform(data[categorical_columns])

# Define preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_columns),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_columns)
    ]
)

# Split data
X = data.drop(columns=['stroke'])
y = data['stroke']

# Preprocess and transform data
X_transformed = preprocessor.fit_transform(X)
X = pd.DataFrame(X_transformed, columns=preprocessor.get_feature_names_out())

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Oversample with SMOTE
print("Before SMOTE:", X_train.shape, y_train.shape)
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
print("After SMOTE:", X_train_resampled.shape, y_train_resampled.shape)

# Train model
rf_model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10)
rf_model.fit(X_train_resampled, y_train_resampled)

# Evaluate model
y_pred = rf_model.predict(X_test)
y_pred_proba = rf_model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_pred_proba))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save artifacts
joblib.dump(rf_model, 'model.pkl')
joblib.dump(preprocessor, 'preprocessor.pkl')
