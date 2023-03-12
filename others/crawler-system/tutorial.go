package main

import (
	"crawler-system/requester"
	"log"
	"net/http"
	"os"
)

type MyResponseHandler struct {
	outputFile *os.File
}

func (handler *MyResponseHandler) InitFile() {
	var err error
	handler.outputFile, err = os.OpenFile("output", os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0600)
	if err != nil {
		log.Println("Error")
	}
}

func (handler MyResponseHandler) WriteResponse(resp *requester.ResponseWrapper) {
	_, err := handler.outputFile.WriteString(resp.Body)
	if err != nil {
		panic(err)
	}
}

func main() {
	urls := []string{
		"https://vnexpress.net/microservice/sheet/type/covid19_2021_by_location",
		"https://vnexpress.net/microservice/sheet/type/covid19_2021_by_day",
		"https://vnexpress.net/microservice/sheet/type/covid19_daily_deaths",
		"https://vnexpress.net/microservice/sheet/type/vaccine_data_vietnam",
	}
	responseHandler := MyResponseHandler{}
	responseHandler.InitFile()
	requester.InitHttpClientPool(4)
	requester.SendMultipleRequest(urls, http.MethodGet, responseHandler)
}
