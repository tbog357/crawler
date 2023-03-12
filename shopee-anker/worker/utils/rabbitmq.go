package utils

import "github.com/streadway/amqp"

// RabbitMQ ..
type RabbitMQ struct {
	Connection *amqp.Connection
	Channel    *amqp.Channel
}

// SetupConnection ..
func (c *RabbitMQ) SetupConnection() {
	var err error
	// Create connection
	c.Connection, err = amqp.Dial("amqp://guest:guest@localhost:5672/")
	FailOnError(err, "Failed to connect to RabbitMQ")

	// Create channel
	c.Channel, err = c.Connection.Channel()
	FailOnError(err, "Failed to create a channel")
}
