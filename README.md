This project is a basic demonstration of a Kafka Data Transfer process.

The Project Directory Tree:

```
kafka-form-dashboard/
├── README.md
├── requirements.txt
├── kafka-env/           # (created after running venv)
├── consumer_app/
│   └── dashboard.py
└── producer_app/
    ├── templates
    |   └──form.html
    └── app.py
```

To Run the Project in Ubuntu a virtual environment needs to be created.

```
python3 -m venv kafka-env
source kafka-env/bin/activate
pip install -r requirements.txt
```