package main

import (
	"encoding/json"
	"fmt"

	"worker/utils"

	"github.com/streadway/amqp"
)

type rabbitMQ struct {
	utils.RabbitMQ
}

// Handle job type == itemsList
type rpcJob struct {
	Job  jobDetail
	Data string
}

type jobDetail struct {
	Platform string
	ShopID   string
	JobType  string
	URL      string
	Page     int
}

func genRPCJob(data []byte, job jobDetail) []byte {
	var rpcServerJob rpcJob
	rpcServerJob.Data = string(data)
	rpcServerJob.Job = job

	rpcServerJobBytes, err := json.Marshal(rpcServerJob)
	utils.FailOnError(err, "Cannot encode rpcServerJob")
	return rpcServerJobBytes
}

func (c *rabbitMQ) sendListItems(data []byte, job jobDetail, goRoutineId int) {

	// Create a queue for receving result from RPC server
	q, err := c.Channel.QueueDeclare(
		"",    // name
		false, // durable
		false, // delete when unused
		true,  // exclusive
		false, // noWait
		nil,   // arguments
	)

	// Listen to the result queue
	msgs, err := c.Channel.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	utils.FailOnError(err, "Failed to publish a message")

	// Generate ID
	corrID := utils.RandomString(32)

	// Send request to rpc server
	err = c.Channel.Publish(
		"",          // exchange
		"rpc_queue", // routing key
		false,       // mandatory
		false,       // immediate
		amqp.Publishing{
			ContentType:   "text/plain",
			CorrelationId: corrID,
			ReplyTo:       q.Name,
			Body:          genRPCJob(data, job),
		})
	utils.FailOnError(err, "Failed to publish a message")

	// Waiting for result
	for d := range msgs {
		fmt.Printf("Go routine %d received result with %s\n", goRoutineId, d.CorrelationId)
		if corrID == d.CorrelationId {
			fmt.Printf("Go routine %d success sending request to RPC server\n", goRoutineId)
			break
		}
	}
	return
}

func (c *rabbitMQ) sendItems(data []byte) {
	c.Channel.Publish(
		"anker",
		"results",
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        data,
		})
}
