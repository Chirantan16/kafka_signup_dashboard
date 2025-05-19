from flask import Flask, render_template, request
from kafka import KafkaProducer
import json

app = Flask(__name__)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form['name'],
        'email': request.form['email']
    }
    producer.send('test-topic', value=data)

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submission Successful</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f4f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            h2 {{
                color: #28a745;
            }}
            p {{
                margin-top: 10px;
                color: #555;
            }}
            a {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                transition: background-color 0.3s;
            }}
            a:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>✅ Form Submitted Successfully!</h2>
            <p>Thank you, <strong>{name}</strong>. Your data has been sent to Kafka.</p>
            <a href="/">⬅️ Go Back to Sign Up Page</a>
        </div>
    </body>
    </html>
    '''.format(name=data['name'])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
