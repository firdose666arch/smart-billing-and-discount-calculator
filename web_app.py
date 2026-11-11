
from flask import Flask, render_template_string, request, redirect, send_file
from invoice import generate_invoice

app = Flask(__name__)

STYLE = """
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #090e20;
    color: #f1f5f9;
}

.layout {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 245px;
    background: #111831;
    padding: 28px 18px;
    border-right: 1px solid #293353;
    flex-shrink: 0;
}

.brand {
    font-size: 21px;
    font-weight: 800;
    color: #a78bfa;
    margin: 5px 10px 35px;
}

.nav {
    display: block;
    padding: 14px;
    margin: 9px 0;
    color: #aab6d1;
    text-decoration: none;
    border-radius: 10px;
    transition: .2s;
}

.nav:hover, .nav.active {
    background: linear-gradient(90deg, #5428a8, #244a9b);
    color: white;
}

.main {
    flex: 1;
    padding: 35px;
    min-width: 0;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    margin-bottom: 30px;
}

h1 { font-size: 29px; margin: 0; }
h2 { color: #c4b5fd; }
h3 { color: #93c5fd; }

.subtitle { color: #94a3b8; margin-top: 8px; }

.panel {
    background: #151e39;
    border: 1px solid #2d3a60;
    border-radius: 17px;
    padding: 25px;
    margin-bottom: 22px;
    box-shadow: 0 12px 30px #0003;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 18px;
    margin: 25px 0;
}

.stat {
    background: linear-gradient(135deg, #202b50, #28204e);
    padding: 24px;
    border: 1px solid #45416f;
    border-radius: 15px;
}

.stat small { color: #a5b4fc; }
.stat h2 { font-size: 25px; margin-bottom: 0; }

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 18px;
}

input, select {
    display: block;
    width: 100%;
    padding: 13px;
    margin: 10px 0 17px;
    background: #0c1530;
    color: white;
    border: 1px solid #39476c;
    border-radius: 9px;
    outline: none;
}

input:focus, select:focus {
    border-color: #9b7aff;
    box-shadow: 0 0 9px #8054e955;
}

input::placeholder { color: #8995b0; }
label { color: #cbd5e1; font-size: 14px; }

button, .btn {
    display: inline-block;
    padding: 13px 20px;
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white;
    border: none;
    border-radius: 9px;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
    transition: .25s;
}

button:hover, .btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px #7c3aed66;
}

.result {
    background: #102b40;
    border: 1px solid #256b83;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}

.result p { color: #dbeafe; }

.accent { color: #a78bfa; }
.muted { color: #94a3b8; }
.full { width: 100%; }

@media(max-width: 700px) {
    .layout { display: block; }
    .sidebar { width: 100%; padding: 15px; }
    .brand { margin: 5px 5px 15px; }
    .nav { display: inline-block; padding: 9px; margin: 3px; }
    .main { padding: 20px 14px; }
    h1 { font-size: 23px; }
}
</style>
"""

SHELL = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }} | Midnight Pro</title>
    """ + STYLE + """
</head>
<body>
<div class="layout">
    <aside class="sidebar">
        <div class="brand">✦ BILLCRAFT </div>
        <a class="nav {{ 'active' if active == 'home' else '' }}" href="/">▦ Dashboard</a>
        <a class="nav {{ 'active' if active == 'calculator' else '' }}" href="/calculator">▣ Smart Billing</a>
        <a class="nav {{ 'active' if active == 'invoice' else '' }}" href="/invoice">▤ GST Invoice</a>
        <div class="nav muted">✧ Billing Suite</div>
    </aside>

    <main class="main">
        <div class="topbar">
            <div>
                <h1>{{ title }}</h1>
                <div class="subtitle">Your smart business billing workspace</div>
            </div>
            <div class="accent">● System Ready</div>
        </div>
        {{ content|safe }}
    </main>
</div>
</body>
</html>
"""


def page(title, content, active):
    return render_template_string(
        SHELL,
        title=title,
        content=content,
        active=active
    )


@app.route("/")
def index():
    content = """
    <div class="panel">
        <h2>Welcome to Smart billing calculator✨</h2>
        <p class="muted">
            Manage your billing, discounts and professional GST invoices
            from one beautiful workspace.
        </p>
        <a class="btn" href="/invoice">Create an Invoice →</a>
    </div>

    <div class="cards">
        <div class="stat">
            <small>APPLICATION</small>
            <h2>Smart Billing</h2>
            <p class="muted">Calculate bills easily</p>
        </div>
        <div class="stat">
            <small>INVOICE SYSTEM</small>
            <h2>PDF Ready</h2>
            <p class="muted">Generate professional invoices</p>
        </div>
        <div class="stat">
            <small>TAX SUPPORT</small>
            <h2>GST</h2>
            <p class="muted">CGST, SGST and IGST</p>
        </div>
    </div>

    <div class="grid">
        <div class="panel">
            <h3>▣ Smart Calculator</h3>
            <p class="muted">Calculate product prices and discounts.</p>
            <a class="btn" href="/calculator">Open Calculator</a>
        </div>
        <div class="panel">
            <h3>▤ Professional Invoice</h3>
            <p class="muted">Create downloadable PDF invoices.</p>
            <a class="btn" href="/invoice">Create Invoice</a>
        </div>
    </div>
    """
    return page("Dashboard", content, "home")


@app.route("/calculator", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        product = request.form["product"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        discount_percent = float(request.form["discount"])

        if quantity < 1 or price < 0 or not 0 <= discount_percent <= 100:
            return "Invalid billing values", 400

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

    content = """
    <div class="panel">
        <h2>Smart Billing Calculator</h2>
        <p class="muted">Enter your product details to calculate the bill.</p>

        <form method="POST">
            <label>Product Name</label>
            <input name="product" placeholder="Enter product name" required>

            <div class="grid">
                <div>
                    <label>Quantity</label>
                    <input name="quantity" type="number" min="1" placeholder="Quantity" required>
                </div>
                <div>
                    <label>Price per item (₹)</label>
                    <input name="price" type="number" min="0" step="0.01" placeholder="Price" required>
                </div>
            </div>

            <label>Discount Percentage (%)</label>
            <input name="discount" type="number" min="0" max="100" step="0.01" value="0" required>

            <button class="full" type="submit">Calculate My Bill ✦</button>
        </form>

        {% if result %}
        <div class="result">
            <h3>✦ Bill Summary</h3>
            <p>Product: {{ result.product }}</p>
            <p>Quantity: {{ result.quantity }}</p>
            <p>Total: ₹{{ result.total }}</p>
            <p>Discount: ₹{{ result.discount }}</p>
            <h2>Final Amount: ₹{{ result.final }}</h2>
        </div>
        {% endif %}
    </div>
    """

    rendered = render_template_string(content, result=result)
    return page("Smart Billing", rendered, "calculator")


@app.route("/invoice")
def invoice_page():
    content = """
    <div class="panel">
        <h2>✦ Professional GST Invoice</h2>
        <p class="muted">Complete the details to generate your PDF invoice.</p>

        <form action="/download-invoice" method="POST">

            <h3>01 — Business Details</h3>
            <label>Business Name</label>
            <input name="business" placeholder="Your business name" required>

            <label>Business Address</label>
            <input name="business_address" placeholder="Business address" required>

            <label>Business GSTIN (optional)</label>
            <input name="business_gstin" placeholder="GSTIN">

            <h3>02 — Customer Details</h3>
            <label>Customer Name</label>
            <input name="customer" placeholder="Customer name" required>

            <label>Customer Address</label>
            <input name="customer_address" placeholder="Customer address" required>

            <label>Customer GSTIN (optional)</label>
            <input name="customer_gstin" placeholder="Customer GSTIN">

            <h3>03 — Product Details</h3>
            <label>Product Name</label>
            <input name="product" placeholder="Product name" required>

            <div class="grid">
                <div>
                    <label>Quantity</label>
                    <input name="quantity" type="number" min="1" step="1" required>
                </div>
                <div>
                    <label>Price per item (₹)</label>
                    <input name="price" type="number" min="0" step="0.01" required>
                </div>
            </div>

            <h3>04 — Discount and GST</h3>
            <label>Discount (%)</label>
            <input name="discount" type="number" min="0" max="100" step="0.01" value="0" required>

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

            <button class="full" type="submit">
                ↓ Generate & Download PDF Invoice
            </button>
        </form>
    </div>
    """

    return page("GST Invoice Generator", content, "invoice")


@app.route("/download-invoice", methods=["POST"])
def download_invoice():
    try:
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

        quantity = float(data["quantity"])
        price = float(data["price"])
        discount = float(data["discount"])
        gst = float(data["gst_rate"])

        if quantity < 1 or price < 0 or not 0 <= discount <= 100:
            return "Invalid billing values", 400

        if gst not in (0, 5, 12, 18, 28):
            return "Invalid GST rate", 400

        pdf_path, invoice_number = generate_invoice(data)

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{invoice_number}.pdf"
        )

    except (ValueError, KeyError):
        return "Please check the invoice details and try again.", 400


if __name__ == "__main__":
    app.run(debug=True)
