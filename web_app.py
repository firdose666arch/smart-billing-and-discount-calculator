from flask import Flask, render_template_string, request , redirect
from invoice import generate_invoice

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

@app.route("/calculator", methods=["GET", "POST"])
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
from flask import send_file

@app.route("/download-invoice", methods=["POST"])
def download_invoice():
    data = {
        "business": request.form["business"],
        "business_address": request.form["business_address"],
        "business_gstin": request.form.get("business_gstin", ""),
        "customer": request.form["customer"],
        "customer_address": request.form["customer_address"],
        "customer_gstin": request.form.get("customer_gstin", ""),
        "product": request.form["product"],
        "quantity": request.form["quantity"],
        "price": request.form["price"],
        "discount": request.form["discount"],
        "gst_rate": request.form["gst_rate"],
        "tax_type": request.form["tax_type"]
    }

    pdf_path, invoice_number = generate_invoice(data)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{invoice_number}.pdf"
    )
@app.route("/")
def index():
    return redirect("/invoice")

@app.route("/invoice")
def invoice_page():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Professional GST Invoice</title>
        <style>
            body {
                font-family: Arial;
                background: #eef2f7;
                padding: 25px;
            }
            .container {
                max-width: 650px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
            }
            input, select, button {
                width: 100%;
                padding: 12px;
                margin: 8px 0;
                box-sizing: border-box;
            }
            h2 { color: #1d4ed8; }
            button {
                background: #1d4ed8;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h2>Professional GST Invoice</h2>

        <form action="/download-invoice" method="POST">

            <h3>Business Details</h3>
            <input name="business" placeholder="Business Name" required>
            <input name="business_address" placeholder="Business Address" required>
            <input name="business_gstin" placeholder="Business GSTIN">

            <h3>Customer Details</h3>
            <input name="customer" placeholder="Customer Name" required>
            <input name="customer_address" placeholder="Customer Address" required>
            <input name="customer_gstin" placeholder="Customer GSTIN">

            <h3>Product Details</h3>
            <input name="product" placeholder="Product Name" required>
            <input name="quantity" type="number" min="1" step="1" placeholder="Quantity" required>
            <input name="price" type="number" min="0" step="0.01" placeholder="Price per item" required>

            <h3>Discount and GST</h3>
            <input name="discount" type="number" min="0" max="100" step="0.01" value="0" placeholder="Discount percentage">

            <label>GST Rate</label>
            <select name="gst_rate">
                <option value="0">0% GST</option>
                <option value="5">5% GST</option>
                <option value="12">12% GST</option>
                <option value="18" selected>18% GST</option>
                <option value="28">28% GST</option>
            </select>

            <label>Tax Type</label>
            <select name="tax_type">
                <option value="Intrastate">Same State (CGST + SGST)</option>
                <option value="Interstate">Different State (IGST)</option>
            </select>

            <button type="submit">Generate & Download PDF Invoice</button>

        </form>
    </div>
    </body>
    </html>
    """)
if __name__ == "__main__":
    app.run(debug=True)