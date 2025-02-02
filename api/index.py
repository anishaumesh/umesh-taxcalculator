from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tax Calculator</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0;
            padding: 0;  /* Added padding reset to avoid unexpected gaps */
        }
        .container {
            text-align: center;
            width: 50%;
            margin-top: -10%;  /* Reduces the top margin */
        }
        table {
            margin-top: 20px;
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            padding: 8px 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Enter Income</h2>
        <form method="post">
            <input type="number" name="income" required>
            <button type="submit">Calculate</button>
        </form>
        {% if tax is not none %}
            <table>
                <tr>
                    <th>Gross Income</th>
                    <td>{{ income }}</td>
                </tr>
                <tr>
                    <th>Taxable Income</th>
                    <td>{{ income - 75000 }}</td>
                </tr>
                <tr>
                    <th>Tax</th>
                    <td>{{ tax }}</td>
                </tr>
                {% if surcharge > 0 %}
                    <tr>
                        <th>Surcharge</th>
                        <td>{{ surcharge }}</td>
                    </tr>
                {% endif %}
                <tr>
                    <th>Cess</th>
                    <td>{{ cess }}</td>
                </tr>
                <tr>
                    <th>Total Tax</th>
                    <td>{{ final_tax }}</td>
                </tr>
                {% if marginal_relief_applied %}
                    <tr>
                        <td colspan="2">
                            <p>Note: Marginal relief is applied on this gross salary</p>
                        </td>
                    </tr>
                {% endif %}
                <tr>
                    <th>Total tax paid as percentage of gross income</th>
                    <td>{{ percentage }}%</td>
                </tr>
            </table>
        {% endif %}
    </div>
</body>
</html>
'''

def calculate_tax(income):
    standard_deduction = 75000
    
    marginal_relief_a = 1345588
    marginal_relief_surcharge = 5189140
    
    cess = 0
    tax = 0
    surcharge = 0
    marginal_relief_applied = False

    adjusted_income = income - standard_deduction
    if income <= 1275000:
        return 0, 0, 0, 0, False

    if income <= marginal_relief_a:
        tax = min((adjusted_income - 1200000), 600000 + (adjusted_income - 1200000) * 0.15)
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, True
        
    if income <= 1675000:
        tax = 60000 + (adjusted_income - 1200000) * 0.15
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, False
        
    if income <= 2075000:
        tax = 120000 + (adjusted_income - 1600000) * 0.2
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, False
    
    if income <= 2475000:
        tax = 200000 + (adjusted_income - 2000000) * 0.25
        cess = tax * 0.04
        return tax, 0, cess, tax + cess, False
        
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
    
    if income <= 20075000:
        tax = 300000 + (adjusted_income - 2400000) * 0.3
        surcharge = tax * 0.15
        cess = (tax + surcharge) * 0.04
        return tax, surcharge, cess, (tax + surcharge + cess), False

    if income >= 20075000:
        tax = 300000 + (adjusted_income - 2400000) * 0.3
        surcharge = tax * 0.25
        cess = (tax + surcharge) * 0.04
        return tax, surcharge, cess, (tax + surcharge + cess), False

@app.route('/', methods=['GET', 'POST'])
def index():
    tax, surcharge, cess, final_tax, marginal_relief_applied = None, None, None, None, None
    income, percentage = None, None
    if request.method == 'POST':
        income = float(request.form.get('income', 0))
        tax, surcharge, cess, final_tax, marginal_relief_applied = calculate_tax(income)
        percentage = round((final_tax / income) * 100, 2)
    return render_template_string(HTML_TEMPLATE, tax=tax, surcharge=surcharge, cess=cess, final_tax=final_tax, marginal_relief_applied=marginal_relief_applied, income=income, percentage=percentage)

if __name__ == "__main__":
    app.run(debug=True)
