
# Import statements
import pandas as pd
from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier
import os

# Create Flask application
app = Flask(__name__)

# Load CSV data
data = pd.read_csv("products.csv")

# Convert expiry date
data["Expiry_Date"] = pd.to_datetime(data["Expiry_Date"])

# Calculate remaining days
data["Remaining_Days"] = (
    data["Expiry_Date"] - pd.Timestamp.today().normalize()
).dt.days

# Separate input and output
X = data[["Remaining_Days"]]
y = data["Status"]

# Create Decision Tree model
model = DecisionTreeClassifier()

# Train the model
model.fit(X, y)


# Flask home page
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        expiry = pd.to_datetime(request.form["expiry"])

        days = (
            expiry - pd.Timestamp.today().normalize()
        ).days

        prediction = model.predict(
            pd.DataFrame({"Remaining_Days": [days]})
        )

        result = prediction[0]

    return render_template("index.html", result=result)


# Run application on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
