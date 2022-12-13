package main

import (
	"log"
	"os"
)

func exitOnError(err error) {
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}
}

func logOnError(err error) bool {
	if err != nil {
		log.Println(err)
		return true
	}
	return false
}
