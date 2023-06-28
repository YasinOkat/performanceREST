from flask import Flask, jsonify, request
from datetime import datetime
import psycopg2

app = Flask(__name__)
db_connection_string = "dbname=veritabani user=postgres password=1234 host=localhost"


def get_database_connection():
    conn = psycopg2.connect(db_connection_string)
    cursor = conn.cursor()
    return conn, cursor


@app.route("/", methods=['GET'])
def home():
    return "Merhaba."


@app.route('/getPersoneller', methods=['GET'])
def get_personeller():
    conn, cursor = get_database_connection()

    gorev = request.args.get('gorev')

    query = "SELECT isim, soyisim FROM personeller WHERE gorev = %s"
    cursor.execute(query, (gorev,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    personeller = [{'isim': row[0], 'soyisim': row[1]} for row in result]
    return jsonify(personeller)


@app.route('/insertLog', methods=['POST'])
def insert_log():
    conn, cursor = get_database_connection()

    data = request.get_json()
    rampa_no = data.get('rampa_no')
    vardiya_amiri = data.get('vardiya_amiri')
    rampa_sorumlusu = data.get('rampa_sorumlusu')
    yuklemeci = data.get('yuklemeci')
    yuklemeci2 = data.get('yuklemeci2')
    days = data.get('days')
    arac_plaka = data.get('arac_plaka')
    dorse_plaka = data.get('dorse_plaka')
    urun_sayisi = data.get('urun_sayisi')
    forklift_operatoru = data.get('forklift_operatoru')

    query = "INSERT INTO perflog (rampa_no, vardiya_amiri, " \
            "rampa_sorumlusu, yuklemeci, yuklemeci2, days, arac_plaka, " \
            "dorse_plaka, urun_sayisi, forklift_operatoru) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(query, (rampa_no, vardiya_amiri, rampa_sorumlusu, yuklemeci,
                           yuklemeci2, days, arac_plaka, dorse_plaka, urun_sayisi, forklift_operatoru))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'success'})


@app.route('/insertArac', methods=['POST'])
def insert_arac():
    conn, cursor = get_database_connection()

    data = request.get_json()
    days = data.get('days_no')
    gecikme_adet = data.get('gecikme_adet')
    gecikme_dk = data.get('gecikme_dk')
    current_time = datetime.now()

    action = data.get('action')
    if action == 'rampa_yanasma':
        query = "UPDATE perflog SET rampa_yanasma = %s WHERE days = %s AND rampa_yanasma IS NULL"
        cursor.execute(query, (current_time, days))
    elif action == 'toplama_baslama':
        query = "UPDATE perflog SET toplama_baslama = %s WHERE days = %s AND toplama_baslama IS NULL"
        cursor.execute(query, (current_time, days))
    elif action == 'arac_ici_baslama':
        query = "UPDATE perflog SET yukleme_baslama = %s WHERE days = %s AND yukleme_baslama IS NULL"
        cursor.execute(query, (current_time, days))
    elif action == 'toplama_bitis':
        query = "UPDATE perflog SET toplama_bitis = %s WHERE days = %s AND toplama_bitis IS NULL"
        cursor.execute(query, (current_time, days))
    elif action == 'yukleme_bitis':
        query = "UPDATE perflog SET yukleme_bitis = %s WHERE days = %s AND yukleme_bitis IS NULL"
        cursor.execute(query, (current_time, days))
    elif action == 'rampa_cikis':
        query = "UPDATE perflog SET rampa_cikis = %s WHERE days = %s AND rampa_cikis IS NULL"
        cursor.execute(query, (current_time, days))
    elif action == 'İlave':
        query2 = "UPDATE perflog SET ilave_adet = %s, ilave_dk = %s WHERE days = %s AND ilave_adet IS NULL AND ilave_dk IS NULL"
        cursor.execute(query2, (gecikme_adet, gecikme_dk, days))
    elif action == 'Düşüm':
        query2 = "UPDATE perflog SET dusum_adet = %s, dusum_dk = %s WHERE days = %s AND dusum_adet IS NULL AND dusum_dk IS NULL"
        cursor.execute(query2, (gecikme_adet, gecikme_dk, days))
    elif action == 'Bloke':
        query2 = "UPDATE perflog SET bloke_adet = %s, bloke_dk = %s WHERE days = %s AND bloke_adet IS NULL AND bloke_dk IS NULL"
        cursor.execute(query2, (gecikme_adet, gecikme_dk, days))
    elif action == 'Diğer':
        query2 = "UPDATE perflog SET diger_adet = %s, diger_dk = %s WHERE days = %s AND diger_adet IS NULL AND diger_dk IS NULL"
        cursor.execute(query2, (gecikme_adet, gecikme_dk, days))
    else:
        return jsonify({'message': 'Invalid action'})


    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'success'})


@app.route('/getDaysNo', methods=['GET'])
def get_days_no():
    conn, cursor = get_database_connection()

    query = "SELECT days FROM perflog WHERE rampa_cikis IS NULL"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    days = [{'days': row[0]} for row in result]
    return jsonify(days)


@app.route('/getLatestDaysNo', methods=['GET'])
def get_latest_days_no():
    conn, cursor = get_database_connection()

    query = "SELECT days FROM perflog WHERE rampa_cikis IS NULL ORDER BY days DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    days = [{'days': row[0]} for row in result]
    return jsonify(days)


@app.route('/getRampaOptions', methods=['GET'])
def get_rampa_options():
    conn, cursor = get_database_connection()

    query = "SELECT rampa FROM rampalar"
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    rampa_options = [{'rampa': row[0]} for row in result]
    return jsonify(rampa_options)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.193')
