from flask import Flask, request

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
    db = create_db_connection('test.db')
    result = db.execute(
        f"SELECT SUM(line_item_unblended_cost) FROM cur WHERE product_servicecode = '{product_servicecode}'").fetchall()
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
    return {'cost': cost}


if __name__ == "__main__":
    app.run(debug=True)
