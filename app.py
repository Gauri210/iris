from flask import Flask, request, render_template_string
from sklearn.datasets import load_iris
import pandas as pd

app = Flask(__name__)

# Load dataset
iris = load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["species"] = iris.target
df["species"] = df["species"].apply(lambda x: iris.target_names[x])

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Iris Dataset Viewer</title>
</head>
<body>

<h2>Iris Dataset Filter</h2>

<form method="POST">
    Enter Species:
    <input type="text" name="species" placeholder="setosa / versicolor / virginica">
    <input type="submit" value="Search">
</form>

{% if tables %}
<h3>Results</h3>
{{ tables|safe }}
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():

    tables = None

    if request.method == "POST":
        species = request.form.get("species").lower()

        filtered = df[df["species"] == species]

        if not filtered.empty:
            tables = filtered.to_html()
        else:
            tables = "<p>No results found</p>"

    return render_template_string(HTML, tables=tables)

if __name__ == "__main__":
    app.run(debug=True)