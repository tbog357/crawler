package requester

import "net/http"

type httpClientWrapper struct {
	client *http.Client
	id     int
}



func InitHttpClientPool(numClient int) {
	// Init a http client pool for multiple requesting
	for httpClientId := 0; httpClientId <= numClient; httpClientId++ {
		httpClientPool[httpClientId] = httpClientWrapper{
			client: &http.Client{},
			id:     httpClientId,
		}

		httpClientStatus[httpClientId] = CLIENT_STATUS_FREE
	}
}
