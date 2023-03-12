package main

import (
	"fmt"
	"strconv"
	"worker/utils"

	"github.com/streadway/amqp"
	"github.com/valyala/fastjson"
)

func main() {
	var clientRabbitMQ rabbitMQ
	var jsonParser fastjson.Parser

	// Setup connection
	clientRabbitMQ.SetupConnection()

	// Listenning to request
	clientRabbitMQ.Channel.QueueDeclare(
		"rpc_queue", // name
		false,       // durable
		false,       // delete when unused
		false,       // exclusive
		false,       // no-wait
		nil,         // arguments
	)

	err := clientRabbitMQ.Channel.Qos(
		1,     // prefetch count
		0,     // prefetch size
		false, // global
	)
	utils.FailOnError(err, "Failed to set QoS")

	msgs, err := clientRabbitMQ.Channel.Consume(
		"rpc_queue", // queue
		"",          // consumer
		false,       // auto-ack
		false,       // exclusive
		false,       // no-local
		false,       // no-wait
		nil,         // args
	)
	utils.FailOnError(err, "Failed to register a consumer")

	blockMainRoutine := make(chan bool)

	// Can add more routine here
	go func(sender rabbitMQ) {
		for d := range msgs {
			// Recevice request from downloader
			var links []string
			var url string
			var job jobDetail

			// Decode json to get job detail
			jobSelector, err := jsonParser.Parse(string(d.Body))
			utils.FailOnError(err, "Failed to decode json data")

			// Get job information
			job.Platform = string(jobSelector.GetStringBytes("Job", "Platform"))
			job.JobType = string(jobSelector.GetStringBytes("Job", "JobType"))
			job.URL = string(jobSelector.GetStringBytes("Job", "URL"))
			job.ShopID = string(jobSelector.GetStringBytes("Job", "ShopID"))
			job.Page = jobSelector.GetInt("Job", "Page")

			fmt.Printf("Recevied job %+v\n", job)

			// Decode json to get data
			rpcData := jobSelector.GetStringBytes("Data")
			utils.FailOnError(err, "Cannot decode json to get data")

			v, err := jsonParser.Parse(string(rpcData))

			// Generate item link from json data
			for i := 0; i < 30; i++ {
				itemid := v.GetInt("items", strconv.Itoa(i), "itemid")
				// https://shopee.vn/api/v2/item/get?itemid=6032957967&shopid=16461019
				url = "https://shopee.vn/api/v2/item/get?itemid=" + strconv.Itoa(itemid) + "&shopid=" + job.ShopID
				// url = "https://shopee.vn/*-i.16461019." + strconv.Itoa(itemid)
				if itemid != 0 {
					links = append(links, url)
				}
			}

			// Send back jobs to downloaders if have any
			clientRabbitMQ.sendJobs(links, job.ShopID, job.Page)

			// Send ack

			response := ""

			err = clientRabbitMQ.Channel.Publish(
				"",        // exchange
				d.ReplyTo, // routing key
				false,     // mandatory
				false,     // immediate
				amqp.Publishing{
					ContentType:   "text/plain",
					CorrelationId: d.CorrelationId,
					Body:          []byte(response),
				})
			utils.FailOnError(err, "Failed to publish a message")
			fmt.Println("Send ack to requester ", d.CorrelationId, " with response")
			d.Ack(false)
		}
	}(clientRabbitMQ)

	// Keep main go routine running
	<-blockMainRoutine
}
