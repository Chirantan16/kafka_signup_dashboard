This project is a basic demonstration of a Kafka Data Transfer process.

The Project Directory Tree:

```
kafka-form-dashboard/
├── README.md
├── requirements.txt
├── kafka-env/           # (created after running venv only for Ubuntu)
├── consumer_app/
│   └── dashboard.py
└── producer_app/
    ├── templates
    |   └──form.html
    └── app.py
```

Starting local Zookeeper and Kafka after downloading the Kafka files.

```
cd kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

Starting Kafka via Kraft

```
./bin/kafka-storage.sh random-uuid	
./bin/kafka-storage.sh format -t <UUID> -c config/kraft/server.properties
./bin/kafka-server-start.sh config/kraft/server.properties
```

Creating a Kafka Topic.

```
cd kafka
bin/kafka-topics.sh --create --topic form-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Stopping the Zookeeper and Kafka or Kraft Kafka.

```
bin/zookeeper-server-stop.sh config/zookeeper.properties
bin/kafka-server-stop.sh config/server.properties
./bin/kafka-server-stop.sh config/kraft/server.properties
```

To Run the Project in Ubuntu a virtual environment needs to be created.

```
python3 -m venv kafka-env
source kafka-env/bin/activate
pip install -r requirements.txt
cd producer_app
    python app.py
cd consumer_app
    python dashboard.py
```