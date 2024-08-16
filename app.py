from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Funktion zum Abfragen der Produktdetails
def query_inventory(product_name, attribute=None):
    """Fragt die Details eines Produkts in der SQLite-Datenbank ab."""
    conn = sqlite3.connect('erp_data.db')
    cursor = conn.cursor()
    
    if attribute is None:
        cursor.execute("SELECT * FROM inventory WHERE product_name LIKE ?", (f"%{product_name}%",))
    else:
        cursor.execute(f"SELECT {attribute} FROM inventory WHERE product_name LIKE ?", (f"%{product_name}%",))
    
    result = cursor.fetchone()
    conn.close()
    return result

# Funktion zum Abrufen aller Informationen eines Produkts
def get_all_information(product_name):
    """Fragt alle Informationen eines Produkts in der SQLite-Datenbank ab."""
    conn = sqlite3.connect('erp_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE product_name LIKE ?", (f"%{product_name}%",))
    result = cursor.fetchone()
    conn.close()

    if result:
        return f"""
        <b>Produktname:</b> {result[1]}<br>
        <b>Lagerbestand:</b> {result[2]} Einheiten<br>
        <b>Preis:</b> {result[3]} €<br>
        <b>Hersteller:</b> {result[4]}<br>
        <b>Lieferant:</b> {result[5]}<br>
        <b>Lagerort:</b> {result[6]}<br>
        <b>Gewicht:</b> {result[7]} kg<br>
        <b>Beschreibung:</b> {result[8]}
        """
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input'].lower()

    conn = sqlite3.connect('erp_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_name FROM inventory")
    products = cursor.fetchall()
    conn.close()

    attributes = {
        "lagerbestand": ("stock_quantity", "Einheiten"),
        "beschreibung": ("description", ""),
        "lieferant": ("supplier", ""),
        "gewicht": ("weight", "kg"),
        "preis": ("price", "€"),
        "lager": ("location", "")
    }

    product_found = False
    attribute_requested = None

    for product in products:
        product_name = product[0].lower()
        if product_name in user_input:
            if "alle informationen" in user_input:
                # Abrufen aller Informationen des Produkts
                all_info = get_all_information(product_name)
                if all_info:
                    answer = all_info
                else:
                    answer = f"Produkt {product_name.capitalize()} wurde nicht gefunden."
            else:
                for key, (db_column, unit) in attributes.items():
                    if key in user_input:
                        attribute_requested = (db_column, unit)
                        break

                if attribute_requested:
                    attribute_value = query_inventory(product_name, attribute_requested[0])
                    if attribute_value:
                        answer = f"Der {key.capitalize()} für {product_name.capitalize()} beträgt {attribute_value[0]} {attribute_requested[1]}."
                    else:
                        answer = f"Es konnten keine Informationen zu {key} für {product_name.capitalize()} gefunden werden."
                else:
                    # Falls nur der Produktname ohne spezifische Abfrage eingegeben wurde
                    options = ", ".join([f"<button onclick=\"sendMessage('{key.capitalize()} {product_name}')\">{key.capitalize()}</button>" for key in attributes.keys()])
                    answer = f"Welche Informationen möchten Sie über {product_name.capitalize()} wissen? Sie können nach {options} fragen."
            
            product_found = True
            break

    if not product_found:
        answer = "Entschuldige, derzeit kann ich dir leider nur Fragen zum Lagerbestand oder anderen spezifischen Informationen beantworten."

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
