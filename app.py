from flask import Flask, render_template, request

from db import create_db_connection

app = Flask(__name__)

discounts = {
    'AmazonS3': 0.88,  # 12% off
    'AmazonEC2': 0.5,  # 50% off
    'AWSDataTransfer': 0.7,  # 3% off
    'AWSGlue': 0.95,  # 5% off
    'AmazonGuardDuty': 0.25,  # 75% off
}


def get_discounted_service_cost(product_servicecode: str) -> float:
    '''Get discounted cost by product_servicecode. If no discount is found, return the undiscounted cost'''
    discount = discounts.get(product_servicecode)
    undiscounted_cost = get_service_cost(product_servicecode)
    if not discount:
        return undiscounted_cost

    discounted_cost = undiscounted_cost * discount
    return discounted_cost


def get_service_cost(product_servicecode: str) -> float:
    '''Get undiscounted cost by product_servicecode'''
    db = create_db_connection('data/test.db')
    result = db.execute(
        f"SELECT SUM(line_item_unblended_cost) FROM cur WHERE product_servicecode = '{product_servicecode}'").fetchall()
    return result[0][0]


def get_total_undiscounted_cost() -> float:
    '''Get total undiscounted cost'''
    db = create_db_connection('data/test.db')
    result = db.execute(
        f"SELECT SUM(line_item_unblended_cost) FROM cur").fetchall()
    return result[0][0]


def get_total_discounted_cost() -> float:
    '''Get total discounted cost'''
    db = create_db_connection('data/test.db')

    query = """
        SELECT
            SUM(
                c.line_item_unblended_cost * COALESCE(d.percent_total, 1)
            ) AS total_discounted_cost
        FROM
            cur c
        LEFT JOIN
            discounts d
        ON
            c.product_servicecode = d.product_servicecode;
        """

    result = db.execute(query).fetchall()
    return result[0][0]


@app.get('/api/cost')
def get_cost():
    '''get cost by product_servicecode'''
    args = request.args
    print(args)
    product_servicecode = args.get('product_servicecode')
    if not product_servicecode:
        return 'product_servicecode is required', 400

    use_discount = args.get('use_discount')
    print('use_discount', use_discount)
    if use_discount and use_discount.lower() == 'true':
        cost = get_discounted_service_cost(product_servicecode)
    else:
        cost = get_service_cost(product_servicecode)
    return {'cost': round(cost, 2)}


@app.get('/api/blended')
def get_blended_rate():
    '''calculates the blended rate for all usage'''

    total_discounted_cost = get_total_discounted_cost()
    total_undiscounted_cost = get_total_undiscounted_cost()

    blended_rate = 1 - total_discounted_cost / total_undiscounted_cost

    return {
        'blended_rate': f"{round(blended_rate, 2) * 100}%"
    }


@app.get('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
