from flask import Flask, jsonify, request
​
app = Flask(name)
​
# Dummy inventory and pricing data
​
inventory = {
    1: {'name': 'Item 1', 'price': 20, 'inventory': 10, 'discount': 0.1},
    2: {'name': 'Item 2', 'price': 30, 'inventory': 5, 'discount': 0.2},
    3: {'name': 'Item 3', 'price': 25, 'inventory': 8, 'discount': 0.15},
}
​
@app.route('/calculate_price', methods=['POST'])
def calculate_price():
    data = request.get_json()
    item_id = data.get('id')
    quantity = data.get('quantity', 1)
​
    if item_id not in inventory:
      return jsonify({'error': 'Invalid item ID'}), 400
​
    item = inventory[item_id]
​
    if item['inventory'] < quantity:
      return jsonify({'error': 'Not enough inventory'}), 400
​
    total_price = quantity * item['price'] * (1 - item['discount'])
​
    # Update inventory (subtract purchased quantity)
    item['inventory'] -= quantity
​
    return jsonify({'total_price': total_price, 'item': item})
    
if name == 'main':
    app.run(debug=True)
