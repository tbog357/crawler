package requester

import (
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
)

type RequestWrapper struct {
	url    string
	method string
	body   io.Reader
}

type ResponseWrapper struct {
	Request      RequestWrapper
	Body         string
	httpClientId int
}

type ResponseHandler interface {
	WriteResponse(*ResponseWrapper)
}

func sendRequest(httpClient httpClientWrapper, request RequestWrapper, response *ResponseWrapper) (bool, []byte) {
	isSuccess := true
	// Create request
	req, err := http.NewRequest(request.method, request.url, request.body)
	if err != nil {
		log.Fatalf("Error")
		isSuccess = false
	}

	// Send request
	resp, err := httpClient.client.Do(req)
	if err != nil {
		log.Fatalf("Error")
		isSuccess = false
	}

	// Close the connection
	defer resp.Body.Close()

	// Convert response from byte to string
	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error")
		isSuccess = false
	}

	return isSuccess, respBody
}

func handleRequest(wg *sync.WaitGroup, httpClient httpClientWrapper, request RequestWrapper) {
	// Create placeholer to hold response returned
	response := &ResponseWrapper{
		Request:      request,
		httpClientId: httpClient.id,
	}

	isSuccess, respBody := sendRequest(httpClient, request, response)
	// Assign to response placeholer
	if isSuccess {
		response.Body = string(respBody)
	}

	// Send to output channel
	responseChannel <- response

	// Set http connection to be free again for reuse
	httpClientStatus[httpClient.id] = CLIENT_STATUS_FREE
	wg.Done()
}

func handleResponse(handler ResponseHandler) {
	for {
		response, ok := <-responseChannel
		if ok {
			// Write to file
			handler.WriteResponse(response)
		} else {
			log.Println("Error")
		}
	}
}
