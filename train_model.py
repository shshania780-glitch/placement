import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("placement.csv")

# Features and target
X = df.drop("Placement_Status", axis=1)
y = df["Placement_Status"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2 , random_state=34)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("placement_model.pkl", "wb"))
print("Model trained and saved successfully!")