import sqlite3
import os
import pandas as pd
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Dynamically resolve path to ensure it works across different environments
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'housing_datasets.sqlite')

# Structured SQL Query Repository (1-10)
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

def execute_analytics_query(query_id):
    """
    Centralized connection handler executing queries securely, 
    preventing resource leaks via explicit context cleanup.
    """
    query = QUERIES.get(query_id)
    if not query:
        return "<h1>Invalid Question Number</h1>", 404
        
    if not os.path.exists(DB_PATH):
        return jsonify({"error": f"Database file not found at expected destination: {DB_PATH}"}), 500

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        
        # Format the output into a crisp, responsive HTML Bootstrap table for presentation
        styled_html = df.to_html(classes='table table-striped table-hover table-bordered', index=False)
        return render_template_string(f"<html><head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'></head><body class='container mt-4'><h2>Analytics Query {query_id} Results</h2>{styled_html}</body></html>")
            
    except Exception as e:
        return jsonify({"error": f"Database execution error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/api/v1/analytics/<int:question_id>", methods=['GET'])
def get_analytics(question_id):
    return execute_analytics_query(question_id)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Housing Analytics REST API Operational</h1><p>Use endpoints: /api/v1/analytics/1 through 10</p>"

@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return "<h1>Invalid Endpoint Path</h1>", 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
