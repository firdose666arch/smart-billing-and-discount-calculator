from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Billing Calculator</title>
    <style>
        body {
            font-family: Arial;
            background: #eef2f7;
            padding: 40px;
        }
        .container {
            max-width: 500px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            box-sizing: border-box;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }
        .result {
            background: #e0f2fe;
            padding: 15px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Smart Billing and Discount Calculator</h2>

    <form method="POST">
        <input name="product" placeholder="Product Name" required>
        <input name="quantity" type="number" min="1" placeholder="Quantity" required>
        <input name="price" type="number" min="0" step="0.01" placeholder="Price per item" required>
        <input name="discount" type="number" min="0" max="100" step="0.01" placeholder="Discount %" required>
        <button type="submit">Calculate Bill</button>
    </form>

    {% if result %}
    <div class="result">
        <h3>Bill Summary</h3>
        <p>Product: {{ result.product }}</p>
        <p>Quantity: {{ result.quantity }}</p>
        <p>Total Bill: ₹{{ result.total }}</p>
        <p>Discount: ₹{{ result.discount }}</p>
        <h3>Final Amount: ₹{{ result.final }}</h3>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        product = request.form["product"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        discount_percent = float(request.form["discount"])

        total = quantity * price
        discount = total * discount_percent / 100
        final = total - discount

        result = {
            "product": product,
            "quantity": quantity,
            "total": f"{total:.2f}",
            "discount": f"{discount:.2f}",
            "final": f"{final:.2f}"
        }

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)