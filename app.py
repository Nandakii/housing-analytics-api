import sqlite3
import pandas as pd
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# SQL Queries mapped to route IDs for clean code management
QUERIES = {
    1: 'SELECT * FROM property_details JOIN property_price_details ON property_price_details.id = property_details.id WHERE price > 1000000 AND (l1 = "Estados Unidos")',
    2: 'SELECT property_details.id, surface_total, CASE WHEN surface_total < 50 THEN "Small" WHEN surface_total BETWEEN 50 AND 100 THEN "Medium" WHEN surface_total > 100 THEN "Large" END AS surface_area_category FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id',
    3: 'SELECT * FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id WHERE l3 = "Belgrano" AND bedrooms=bathrooms ORDER BY bedrooms DESC',
    4: 'SELECT property_price_details.property_type, l3, AVG(price / surface_total) as avg_price_per_sqm FROM property_details JOIN property_price_details ON property_price_details.id = property_details.id WHERE property_details.l3 = "Belgrano" GROUP BY property_price_details.property_type',
    5: 'SELECT property_details.id, property_details.bedrooms, property_details.bathrooms, property_price_details.price FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id WHERE property_price_details.price > (SELECT AVG(p2.price) FROM property_details d2 JOIN property_price_details p2 ON d2.id = p2.id WHERE d2.bedrooms = d2.bathrooms) ORDER BY price DESC',
    6: 'SELECT property_type, price, created_on, SUM(property_price_details.price) OVER (PARTITION BY property_type ORDER BY created_on) AS cumulative_price FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id ORDER BY created_on',
    7: 'SELECT operation_type, property_details.l3, SUM(surface_total) AS total_surface_area FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id WHERE operation_type = "Venta" GROUP BY l3 ORDER BY total_surface_area DESC LIMIT 10',
    8: 'SELECT * FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id WHERE l3 = "Palermo" AND start_date BETWEEN "8/1/2020" AND "9/1/2020" ORDER BY price DESC LIMIT 5',
    9: 'SELECT *, property_price_details.price / property_details.surface_total AS price_per_square_meter FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id ORDER BY property_type, price_per_square_meter DESC LIMIT 3',
    10: 'SELECT *, COUNT(property_details.id), property_details.l1, property_details.l2, property_details.l3, AVG(price / surface_total) AS avg_price_per_square_meter FROM property_details JOIN property_price_details ON property_details.id = property_price_details.id WHERE operation_type = "Venta" AND start_date LIKE "%2020" GROUP BY l1, l2, l3 HAVING COUNT(property_details.id) >= 10 ORDER BY avg_price_per_square_meter DESC LIMIT 3'
}

def execute_query(query_id, response_format='html'):
    conn = None
    try:
        conn = sqlite3.connect('housing_dataset.sqlite')
        query = QUERIES.get(query_id)
        if not query:
            return "<h1>Invalid Question Number</h1>", 404
        
        df = pd.read_sql(query, conn)
        
        if response_format == 'json':
            return jsonify(df.to_dict(orient='records'))
        else:
            return render_template_string(df.to_html(classes='table table-striped'))
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route("/api/v1/analytics/<int:question_id>", methods=['GET'])
def get_analytics(question_id):
    # Defaults to HTML view as per original architecture, allows JSON extension
    return execute_query(question_id, response_format='html')

@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return "<h1>Invalid Endpoints Path</h1>", 404

if __name__ == '__main__':
    # To run with ngrok, uncomment the following lines and run through your terminal pipeline
    # from flask_ngrok import run_with_ngrok
    # run_with_ngrok(app)
    app.run(debug=True)
