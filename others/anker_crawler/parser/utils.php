<?php
declare(strict_types=1);

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
use Elasticsearch\ClientBuilder;

// RabbitMQ 
// Name of queues
const QUEUE_DOWNLOAD_JOBS = "download_jobs";
const QUEUE_DOWNLOAD_RESULTS = "download_results";
const RPC_JOBS = "rpc_queue";

// Routing keys
const KEY_JOBS = "jobs";
const KEY_RESULTS = "results";

// Exchange (using direct type)
const EXCHANGE_NAME = "anker";

// RPC 


// Create pipelines
$rabbitmq_client = new RabbitMQ();

// Create queues
$rabbitmq_client->create_queue(QUEUE_DOWNLOAD_JOBS);
$rabbitmq_client->create_queue(QUEUE_DOWNLOAD_RESULTS);

// Create exchange
$rabbitmq_client->create_exchange(EXCHANGE_NAME);

// Binding queue with routing keys
$rabbitmq_client->binding_queue(QUEUE_DOWNLOAD_JOBS, EXCHANGE_NAME, KEY_JOBS);
$rabbitmq_client->binding_queue(QUEUE_DOWNLOAD_RESULTS, EXCHANGE_NAME, KEY_RESULTS);

// General class for init RabbitMQ connection 
class RabbitMQ {
    // Assume using 'direct' exchange type only
    // and using 1 channel only
    private $conn;
    private $chan;

    // Parse host information and init AMPQ connection 
    public function __construct()
    {
        // Host Information
        $host = "127.0.0.1";
        $port = "5672";
        $user = "guest";
        $password = "guest";

        // Create connection to RabbitMQ
        $this->conn = new AMQPStreamConnection($host, $port, $user, $password); 
        $this->chan = $this->conn->channel();    
    }

    public function __destruct() {
        // Close the connection to RabbitMQ
        $this->chan->close();
        $this->conn->close();
    }

    // Create a Queue
    public function create_queue($queue_name) {
        $this->chan->queue_declare($queue_name, false, false, false, false);
    }

    // Create an exchange
    public function create_exchange($exchange_name) {
        $this->chan->exchange_declare($exchange_name, 'direct', false, false, false);
    }

    // Binding key
    public function binding_queue($queue_name, $exchange_name, $binding_key) {
        $this->chan->queue_bind($queue_name, $exchange_name, $binding_key);
    }

    // Send message to exchange
    public function produce($message, $exchange_name, $routing_key) {
        $msg_object = new AMQPMessage($message);
        $this->chan->basic_publish($msg_object, $exchange_name, $routing_key);
    }

    // Start listening to a specific queue
    public function start_consuming($queue_name, $routing_key, $trigger_function) {
        // Setup config for consuming 
        $this->chan->basic_consume($queue_name, $routing_key, false, true, false, false, $trigger_function);
        
        // Start consuming 
        while ($this->chan->is_consuming()) {
            $this->chan->wait();
        }
    }
}


// Helper class for inserting product information to databases
class DataInserterMySQL {
    // Connection to mysql
    private $conn;
    private $log_path = "/home/tbog/Intrepid/anker_crawler/db_log.txt";

    public function __construct() {
        // Host Information
        $server_name = "127.0.0.1";
        $port = 3306;
        $username = "root";
        $password = "";
        $dbname = "anker";

        // Create connection
        $this->conn = new mysqli($server_name, $username, $password, $dbname, $port);

        // Check connection
        if ($this->conn->connect_error) {
            die("Connection failed: ". $this->conn->connect_error);
        }
    }

    // Close connection when done
    public function __destruct() {
        $this->conn->close();
    }

    // Create table in anker database
    public function create_table() {
        $sql_query = "
            CREATE TABLE product_details (
                id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
                name VARCHAR(100),
                url VARCHAR(100),
                price_min FLOAT UNSIGNED ,
                price_max FLOAT UNSIGNED ,
                price_min_before_discount FLOAT UNSIGNED ,
                price_max_before_discount FLOAT UNSIGNED ,
                stock INT UNSIGNED,
                currency CHAR(3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
        ";
    
        if ($this->conn->query($sql_query) === true) {
            echo "Create table success";
        } else {
            echo "Create table failed";
        }
    }


    // if input is -1 return null else just return the value
    public function check_null($value) {
        if ($value == -1) {
            return "NULL";
        } else {
            return $value;
        }
    }

    // Insert data to table
    public function insert_product($data_item) {
        
        $name = $data_item["name"];
        $url = $data_item["url"];
        $price_min = $this->check_null($data_item["price_min"]);
        $price_max = $this->check_null($data_item["price_max"]);
        $price_min_before_discount = $this->check_null($data_item["price_min_before_discount"]);
        $price_max_before_discount = $this->check_null($data_item["price_max_before_discount"]);
        $stock = $data_item["stock"];
        $currency = $data_item["currency"];
        // 
        $values = "'{$name}', '{$url}', {$price_min}, {$price_max}, {$price_min_before_discount}, {$price_max_before_discount}, {$stock}, '{$currency}'";
        $sql_query = "
            INSERT INTO product_details (name, url, price_min, price_max, price_min_before_discount, price_max_before_discount, stock, currency)
            VALUES ({$values})"; 
        if ($this->conn->query($sql_query) === true) {
            file_put_contents($this->log_path, "SUCCESS: {$values}\n", FILE_APPEND);
        } else {
            file_put_contents($this->log_path, "FAIL INSERT: {$values}\n", FILE_APPEND);
        }
    }
}