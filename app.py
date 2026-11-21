
# Import statements
import pandas as pd
from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Load CSV data
data = pd.read_csv("products.csv")

# Convert expiry date
data["Expiry_Date"] = pd.to_datetime(data["Expiry_Date"])
data["Remaining_Days"] = (data["Expiry_Date"] - pd.Timestamp.today().normalize()).dt.days

# Separate X and Y
X = data[["Remaining_Days"]]
y = data["Status"]

# Model selection
model = DecisionTreeClassifier()

# Train model
model.fit(X, y)

# Flask application
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        expiry = pd.to_datetime(request.form["expiry"])
        days = (expiry - pd.Timestamp.today().normalize()).days
        result = model.predict(pd.DataFrame({"Remaining_Days": [days]}))[0]
    return render_template("index.html", result=result)

app.run(debug=True)
