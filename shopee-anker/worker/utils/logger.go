package utils

import "fmt"

// FailOnError
func FailOnError(err error, msg string) {
	if err != nil {
		fmt.Printf("%s: %s", msg, err)
	}
}
