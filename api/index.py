from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tax Calculator</title>
</head>
<body>
    <h2>Enter Income</h2>
    <form method="post">
        <input type="number" name="income" required>
        <button type="submit">Calculate</button>
    </form>
    {% if tax is not none %}
        <h3>Calculated Tax: {{ tax }}</h3>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    tax = None
    if request.method == 'POST':
        income = float(request.form.get('income', 0))
        tax = 0.3 * income
    return render_template_string(HTML_TEMPLATE, tax=tax)

if __name__ == "__main__":
    app.run(debug=True)
