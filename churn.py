import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

# Enhanced dataset
data = {
    'subscription_history': [12, 5, 3, 8, 2, 15],
    'activity_logs': [100, 20, 5, 50, 3, 200],
    'customer_service_interactions': [1, 3, 5, 2, 6, 0],
    'monthly_expenses': [50, 20, 15, 40, 10, 60],
    'region': ['A', 'B', 'A', 'C', 'B', 'A'],  # Categorical feature
    'churn': [0, 1, 1, 0, 1, 0]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Features and target
X = df.drop(columns='churn')
y = df['churn']

# Identify numeric and categorical columns
numeric_features = ['subscription_history', 'activity_logs', 'customer_service_interactions', 'monthly_expenses']
categorical_features = ['region']

# Preprocessing for numeric and categorical data
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessors in a column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Build a pipeline with preprocessing and classifier
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(pipeline, 'churn_prediction_model.pkl')
print("Model saved as 'churn_prediction_model.pkl'.")
