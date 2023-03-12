package main

import (
	"encoding/json"
	"fmt"
	"strconv"
	"worker/utils"

	"github.com/streadway/amqp"
)

type rabbitMQ struct {
	utils.RabbitMQ
}

// Job information field
type jobDetail struct {
	Platform string
	ShopID   string
	JobType  string
	URL      string
	Page     int
}

//https://shopee.vn/api/v2/item/get?itemid=6032957967&shopid=16461019
// Return url of public API of shopee
func getShopeeAPI(ShopID string, pageNum int) string {
	pageNumStr := strconv.Itoa(pageNum * 30)
	return "https://shopee.vn/api/v2/search_items/?by=pop&limit=30&match_id=" + ShopID + "&newest=" + pageNumStr + "&order=desc&page_type=shop&version=2"
}

// Send jobs to downloader
func (c *rabbitMQ) sendJobs(links []string, shopID string, currentPage int) {
	var job jobDetail

	for i := 0; i < len(links); i++ {
		// Generating job
		job.Platform = "shopee"
		job.JobType = "item"
		job.URL = links[i]
		job.ShopID = shopID
		job.Page = currentPage

		// Encode to json
		jobByte, err := json.Marshal(job)
		utils.FailOnError(err, "Failed at encoding job to json")

		// Send job to downloader
		err = c.Channel.Publish(
			"anker",
			"jobs",
			false,
			false,
			amqp.Publishing{
				ContentType: "text/plain",
				Body:        jobByte,
			},
		)
	}

	// Handle pagination
	// Send to downloader
	if len(links) != 0 {
		job.Platform = "shopee"
		job.JobType = "itemsList"
		job.URL = getShopeeAPI(shopID, currentPage+1)
		job.ShopID = shopID
		job.Page = currentPage + 1

		fmt.Println("Sent ", len(links), " links to downloader")
		fmt.Printf("Sending job to downloader %+v\n", job)

		jobByte, _ := json.Marshal(job)

		err := c.Channel.Publish(
			"anker",
			"jobs",
			false,
			false,
			amqp.Publishing{
				ContentType: "text/plain",
				Body:        jobByte,
			},
		)
		utils.FailOnError(err, "Failed to publish a message")
	} else {
		fmt.Println("No more links")
	}
}

// Send ack to the request's host
func (c *rabbitMQ) sendAck(d *amqp.Delivery) {
	// Send ack to the request's host
	response := "Success"

	err := c.Channel.Publish(
		"",                  // exchange
		"rpc_server_result", // routing key
		false,               // mandatory
		false,               // immediate
		amqp.Publishing{
			ContentType:   "text/plain",
			CorrelationId: d.CorrelationId,
			Body:          []byte(response),
		})
	utils.FailOnError(err, "Failed to publish a message")

	d.Ack(false)
}
