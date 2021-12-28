from flask import Flask, request, render_template
from results import prepare_results

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def get_results():
    # Handle the search form
    if request.method == 'POST':
        market_index = request.form['index']
        stock = request.form['stock']
        results = prepare_results(market_index=market_index, stock=stock)

        table_headings = ('DATE', stock, market_index)
        table_rows = results[0]
        beta_number = results[1]

        return render_template('results.html', table_headings=table_headings, table_rows=table_rows,
                               beta_number=beta_number)
    elif request.method == 'GET':
        return index()


if __name__ == '__main__':
    app.run()
