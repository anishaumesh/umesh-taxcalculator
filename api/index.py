from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tax Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; }
        p { font-size: 16px; }
    </style>
</head>
<body>
    <h2>Enter Income</h2>
    <form method="post">
        <input type="number" name="income" required>
        <button type="submit">Calculate</button>
    </form>
    {% if tax is not none %}
        <p>Tax: {{ tax }}</p>
        <p>Surcharge: {{ surcharge }}</p>
        <p>Cess: {{ cess }}</p>
        <h3>Total Tax: {{ final_tax }}</h3>
        <p>Marginal Relief Applied: {{ marginal_relief_applied }}</p>
        {% if marginal_relief_applied %}
            <p>Note: Marginal relief is applied on this gross salary</p>
        {% endif %}
        <p>Total tax paid as percentage of gross income: {{ (final_tax / income) * 100 | round(2) }}%</p>
    {% endif %}
</body>
</html>
'''

def calculate_tax(income):
    standard_deduction = 75000
    
    marginal_relief_a = 1344118
    marginal_relief_b = 1825000
    marginal_relief_c = 2341667
    marginal_relief_d = 2904286
    marginal_relief_surcharge = 5189140
    
    cess = 0
    tax = 0
    surcharge = 0
    marginal_relief_applied = False

    adjusted_income = income - standard_deduction
    if income <= 1275000:
        return 0, 0, 0, 0, False

    if income <= marginal_relief_a:
        tax = adjusted_income - 1200000
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, True
        
    if income <= 1675000:
        tax = 60000 + (adjusted_income - 1200000) * 0.15
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, False
       
    if income <= marginal_relief_b:
        tax = 120000 + adjusted_income - 1600000
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, True
        
    if income <= 2075000:
        tax = 120000 + (adjusted_income - 1600000) * 0.2
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, False
        
    if income <= marginal_relief_c:
        tax = 200000 + adjusted_income - 2000000
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, True
    
    if income <= 2475000:
        tax = 200000 + (adjusted_income - 2000000) * 0.25
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, False
        
    if income <= marginal_relief_d:
        tax = 300000 + (adjusted_income - 2400000)
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, True
        
    if income <= 5075000:
        tax = 300000 + (adjusted_income - 2400000) * 0.3
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, False
        
    if income <= marginal_relief_surcharge:
        tax = 1080000
        surcharge = adjusted_income - 5000000
        cess = (tax + surcharge) * 0.04
        return tax, surcharge, cess, (tax + surcharge + cess), True
        
    if income <= 10075000:
        tax = 300000 + (adjusted_income - 2400000) * 0.3
        surcharge = tax * 0.1
        cess = (tax + surcharge) * 0.04
        return tax, surcharge, cess, (tax + surcharge + cess), False

@app.route('/', methods=['GET', 'POST'])
def index():
    tax, surcharge, cess, final_tax, marginal_relief_applied = None, None, None, None, None
    income = None
    if request.method == 'POST':
        income = float(request.form.get('income', 0))
        tax, surcharge, cess, final_tax, marginal_relief_applied = calculate_tax(income)
    return render_template_string(HTML_TEMPLATE, tax=tax, surcharge=surcharge, cess=cess, final_tax=final_tax, marginal_relief_applied=marginal_relief_applied, income=income)

if __name__ == "__main__":
    app.run(debug=True)
