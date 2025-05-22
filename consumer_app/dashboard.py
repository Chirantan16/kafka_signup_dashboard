from flask import Flask, jsonify
import threading
import json
from confluent_kafka import Consumer, KafkaError

app = Flask(__name__)
messages = []

def consume_messages():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    topic = 'form-data'
    consumer.subscribe([topic])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break
        data = json.loads(msg.value().decode('utf-8'))
        messages.append(data)

@app.route('/messages')
def get_messages():
    return jsonify(messages)

@app.route('/')
def home():
    print("Starting the dashboard...")
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submitted Credentials</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                padding: 40px;
            }

            h2 {
                text-align: center;
                margin-bottom: 30px;
            }

            table {
                border-collapse: collapse;
                width: 80%;
                margin: auto;
                background-color: #fff;
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                border-radius: 8px;
                overflow: hidden;
            }

            th, td {
                text-align: left;
                padding: 12px 15px;
                border-bottom: 1px solid #ddd;
            }

            th {
                background-color: #007bff;
                color: white;
                position: sticky;
                top: 0;
            }

            tr:hover {
                background-color: #f1f1f1;
            }

            input[type="text"] {
                width: 95%;
                padding: 6px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }

            .filter-row {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h2>Submitted Credentials</h2>
        <table id="data-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                </tr>
                <tr class="filter-row">
                    <th><input type="text" id="filter-name" placeholder="Filter by name"></th>
                    <th><input type="text" id="filter-email" placeholder="Filter by email"></th>
                </tr>
            </thead>
            <tbody id="table-body">
                <!-- Data will be inserted here -->
            </tbody>
        </table>

        <script>
            async function fetchData() {
                const res = await fetch('/messages');
                const data = await res.json();
                renderTable(data);
            }

            function renderTable(data) {
                const nameFilter = document.getElementById('filter-name').value.toLowerCase();
                const emailFilter = document.getElementById('filter-email').value.toLowerCase();

                const filtered = data.filter(item => {
                    return item.name.toLowerCase().includes(nameFilter) &&
                           item.email.toLowerCase().includes(emailFilter);
                });

                document.getElementById('table-body').innerHTML = filtered.map(d => `
                    <tr>
                        <td>${d.name}</td>
                        <td>${d.email}</td>
                    </tr>
                `).join('');
            }

            document.getElementById('filter-name').addEventListener('input', fetchData);
            document.getElementById('filter-email').addEventListener('input', fetchData);

            setInterval(fetchData, 2000);
            fetchData();
        </script>
    </body>
    </html>
    '''


if __name__ == '__main__':
    threading.Thread(target=consume_messages, daemon=True).start()
    app.run(debug=True, port=5001)

