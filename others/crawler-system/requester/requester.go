package requester

import (
	"log"
	"sync"
)

const (
	CLIENT_STATUS_FREE = 0
	CLIENT_STATUS_BUSY = 1
)

var (
	httpClientPool   = make(map[int]httpClientWrapper)
	httpClientStatus = make(map[int]int)
	responseChannel  = make(chan *ResponseWrapper)
)

func SendMultipleRequest(urls []string, method string, responseHandler ResponseHandler) {
	var wg sync.WaitGroup
	go handleResponse(responseHandler)
	// Handle concurrent request based on number of urls provided
	var url string
	for len(urls) > 0 {
		for clientId, clientStatus := range httpClientStatus {
			if clientStatus == CLIENT_STATUS_FREE {
				// Get the free client
				httpClient := httpClientPool[clientId]

				// Pop an url for the free client
				if len(urls) == 0 {
					break
				} else {
					url = urls[0]
					urls = urls[1:]
				}
				log.Println("Requesting url: ", url)
				request := RequestWrapper{
					url:    url,
					method: method,
					body:   nil,
				}
				wg.Add(1)
				go handleRequest(&wg, httpClient, request)

				// Set the client status as busy
				httpClientStatus[clientId] = CLIENT_STATUS_BUSY
			}
		}
	}
	// Wait for all request to finish
	// Close the response channel (output channel)
	wg.Wait()
}
