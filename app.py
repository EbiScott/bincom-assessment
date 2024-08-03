from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/question1', methods=['GET', 'POST'])
def question1():
    conn = sqlite3.connect('election.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        polling_unit_id = request.form['polling_unit_id']
        cursor.execute("SELECT * FROM polling_unit WHERE polling_unit_id=?", (polling_unit_id,))
        data = cursor.fetchall()
        return render_template('question1.html', data=data)
    return render_template('question1.html')


@app.route('/question2', methods=['GET', 'POST'])
def question2():
    conn = sqlite3.connect('election.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        lga_id = request.form['lga_id']
        cursor.execute("""
            SELECT party_abbreviation, SUM(party_score)
            FROM announced_pu_results
            WHERE polling_unit_uniqueid IN (
                SELECT uniqueid FROM polling_unit WHERE lga_id=?
            )
            GROUP BY party_abbreviation
        """, (lga_id,))
        data = cursor.fetchall()
        return render_template('question2.html', data=data)
    return render_template('question2.html')

@app.route('/question3', methods=['GET', 'POST'])
def question3():
    conn = sqlite3.connect('election.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT party_abbreviation, SUM(party_score)
        FROM announced_pu_results
        GROUP BY party_abbreviation
    """)
    data = cursor.fetchall()
    return render_template('question3.html', data=data)
