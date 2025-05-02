#backend

from flask import Flask,render_template, url_for, request
import joblib
import pandas as pd
import sqlite3

std_scaler = joblib.load(r"models\std.lb")
model = joblib.load(r"models\kmeans.lb")
df = pd.read_csv(r'models\label_data.csv')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/inputdata')
def inputdata():
    return render_template('input.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        # data = request.form
        # print(data)
        # return data
        N = int(request.form['N'])
        P = int(request.form['P'])
        h = int(request.form['h'])
        k = int(request.form['k'])
        ph = int(request.form['ph'])
        r = int(request.form['r'])
        t = int(request.form['t'])

        unseen_data = [[N, P, h, k, ph, r, t]]
        tranformed_data = std_scaler.transform(unseen_data)
        cluster_no =  model.predict(tranformed_data)[0]

        # code to insert data into the database.
        conn = sqlite3.connect('farmer.db')
        data_to_be__inserted = (N, P, h, k, ph, r, t, cluster_no)
        insertion_query = "insert into farmerdata (N, P, h, k, ph, r, t, prediction) values(?, ?, ?, ?, ?, ?, ?, ?)"
        cursor_obj = conn.cursor()
        cursor_obj.execute(insertion_query, data_to_be__inserted)
        conn.commit()
        print("inserted successfully.")
        # print(cluster_no)
        filteredcluster_data = df[df['cluster_no'] == cluster_no]
        crops = list(filteredcluster_data['label'].unique())
        # return f"over.{cluster_no}"
        # return crops
        return render_template('output.html',suggested_crops=crops)

if __name__ == "__main__":
    app.run(debug=True)