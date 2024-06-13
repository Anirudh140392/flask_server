from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pymysql
from prompt1 import PROMPT
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
CORS(app, origins=["https://genai.trailytics.com"])

GOOGLE_API_KEY = "AIzaSyC8VSPGQu2pyXz0vMHVoFTCMmFMBJ7nXPk"
genai.configure(api_key=GOOGLE_API_KEY)

def read_sql_query():
    DB_HOST = "tr-wp-database.cfqdq6ohjn0p.us-east-1.rds.amazonaws.com"
    DB_USER = "riya"
    DB_PASSWORD = "Trailytics@789"
    DB_DATABASE = "wipro_n"
    DB_PORT = 3306

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_DATABASE,
        port=DB_PORT,
        connect_timeout=1000,
        autocommit=True
    )

    table_name = "tb_wh_geosales"
    sql = f"SELECT web_pid, orderAmt, pincode, date_column FROM {table_name} WHERE web_pid IN ('B00791D3QG', 'B07VKM2HR5') AND pincode IN ('600064', '700159', '201009') ORDER BY web_pid, date_column;"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    # Close the connection after fetching results
    connection.close()

    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=col_names)

    return col_names, rows

def read_sql_query2():
    DB_HOST = "tr-wp-database.cfqdq6ohjn0p.us-east-1.rds.amazonaws.com"
    DB_USER = "riya"
    DB_PASSWORD = "Trailytics@789"
    DB_DATABASE = "wipro_n"
    DB_PORT = 3306

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_DATABASE,
        port=DB_PORT,
        connect_timeout=1000,
        autocommit=True
    )

    table_name = "product_overall_data_final_copy"
    sql = f"SELECT web_pid, pincode, sales, qty, osa, buybox, created_on FROM {table_name} WHERE web_pid = 'B00791D3QG' AND pf_id = 1 GROUP BY pincode, created_on;"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    # Close the connection after fetching results
    connection.close()

    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=col_names)

    return col_names, rows

def getInsights():
    col_names, rows = read_sql_query2()
    df = pd.DataFrame(rows, columns=col_names)
    
    df['created_on'] = pd.to_datetime(df['created_on'])

    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    df['buybox'] = pd.to_numeric(df['buybox'], errors='coerce')
    
    # Debugging: Print the DataFrame columns and first few rows
    print("DataFrame columns and types:\n", df.dtypes)
    print("First few rows of the DataFrame:\n", df.head())

    # Ensure the 'osa' column is processed correctly for availability calculation
    def availability_percentage(x):
        return (x == 'INSTOCK').mean() * 100
    
    # Group by 'created_on' and calculate the required statistics
    grouped_df = df.groupby('created_on').agg(
        Qty=('qty', 'mean'),
        Sales=('sales', 'mean'),
        Availability=('osa', availability_percentage),
        BuyBox=('buybox', 'mean')
    ).reset_index()

    # Convert 'BuyBox' to percentage
    grouped_df['BuyBox'] = grouped_df['BuyBox'] * 100

    # Rename 'created_on' to 'Day'
    grouped_df.rename(columns={'created_on': 'Day'}, inplace=True)
    
    # Debugging: Print the resulting grouped DataFrame
    print("Grouped DataFrame:\n", grouped_df)
    
    return grouped_df


# Example machine learning function
def perform_ml():
    global all_chart_data
    col_names, rows = read_sql_query()
    df = pd.DataFrame(rows, columns=col_names)
    
    df['date_column'] = pd.to_datetime(df['date_column'])
    
    sns.set(style="whitegrid")
    
    all_chart_data = []
    
    for web_pid in df['web_pid'].unique():
        plt.figure(figsize=(10, 6))
        chart_data = df[df['web_pid'] == web_pid]
        sns.lineplot(data=chart_data, x='date_column', y='orderAmt', hue='pincode', marker='o')

        all_chart_data.append(chart_data)
        # plt.title(f'Sales for {web_pid}')
        # plt.xlabel('Date')
        # plt.ylabel('Sales')
        # plt.legend(title='Pincode')
        # plt.xticks(rotation=45)
        # plt.tight_layout()

        # # Save the plot as an image file
        # plt.savefig(f'{web_pid}_sales.png')

        # # Show the plot
        # plt.show()
    
    return all_chart_data

# a = perform_ml()
# print("***", a)
# exit()
@app.route('/api/predict', methods=['POST'])
def predict():
    global all_chart_data
    try:
        all_chart_data = perform_ml()

        data_dicts = [df.to_dict(orient='records') for df in all_chart_data]
        response = jsonify({"data": data_dicts})
        all_chart_data = []  
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/insights', methods=['POST'])
def insights():
    try:
        df = getInsights()
        result = df.to_dict(orient='records')
        fields = [{'name': col} for col in df.columns]
        return jsonify({'rows': result, 'fields': fields}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
