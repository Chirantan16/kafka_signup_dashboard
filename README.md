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

How to run local zookeeper and kafka after downloading the kafka files and creating a topic:

```
cd kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
bin/kafka-topics.sh --create --topic form-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

To Run the Project in Ubuntu a virtual environment needs to be created.

```
python3 -m venv kafka-env
source kafka-env/bin/activate
pip install -r requirements.txt
```