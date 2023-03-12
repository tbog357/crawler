package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"worker/utils"
)

func main() {
	// Create connection with RabbitMQ server
	var clientRabbitMQ rabbitMQ
	clientRabbitMQ.SetupConnection()

	// Configuration for receving jobs
	jobsMsg, err := clientRabbitMQ.Channel.Consume(
		"download_jobs",
		"jobs",
		true,
		false,
		false,
		false,
		nil,
	)
	utils.FailOnError(err, "Failed to register a consumer")

	// Start go routines downloader
	maxGoRoutines := 10
	blockMainRoutine := make(chan bool)

	// Gain id for each goroutine for monitoring
	for id := 0; id < maxGoRoutines; id++ {
		// Start go routine for this literal function
		go func(goRoutineId int, sender rabbitMQ) {
			// Forever loop
			for {
				// Waiting to receive downloading job
				// fmt.Printf("Go routine %d waiting for job\n", goRoutineId)
				msg := <-jobsMsg
				var job jobDetail

				// Decode json
				json.Unmarshal(msg.Body, &job)

				fmt.Printf("Go routine %d received job %+v\n", goRoutineId, job)

				// For now, don't care about platform
				// just handle ShopID and JobType
				switch job.JobType {
				case "itemsList":
					data := fetchAPI(job.URL)
					// Send to RPC server to get list of products
					sender.sendListItems(data, job, goRoutineId)
				case "item":
					data := fetchAPI(job.URL)
					// Send items information to result consumer
					sender.sendItems(data)
				}

			}
		}(id, clientRabbitMQ)
	}

	// Main routine block here
	<-blockMainRoutine
}

// Fetch the public api
func fetchAPI(url string) []byte {
	fmt.Println(url)
	// Generate HTTP Request
	req, err := http.NewRequest(http.MethodGet, url, nil)
	utils.FailOnError(err, "Failed to create a request")

	// Spoofing
	req.Header.Add("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")

	// Send the HTTP Request
	httpClient := &http.Client{}
	resp, err := httpClient.Do(req)
	utils.FailOnError(err, "Failed to send HTTP request")

	// Convert to byte slice
	data, err := ioutil.ReadAll(resp.Body)
	utils.FailOnError(err, "Failed to parse HTTP response")

	return data
}
