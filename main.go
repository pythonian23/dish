package main

import (
	"fmt"
	"github.com/BurntSushi/toml"
	"github.com/bwmarrin/discordgo"
	flag "github.com/spf13/pflag"
	"os"
	"os/signal"
)

func exit(err error) {
	fmt.Println(err)
	os.Exit(1)
}

var dish Dish

func main() {
	file := flag.StringP("dish", "d", "", ".dish file")
	flag.Parse()

	data, err := os.ReadFile(*file)
	if err != nil {
		exit(err)
	}

	err = toml.Unmarshal(data, &dish)
	if err != nil {
		exit(err)
	}

	session, err := discordgo.New("Bot " + dish.Bot.Token)
	if err != nil {
		exit(err)
	}
	session.Identify.Intents = discordgo.MakeIntent(discordgo.IntentsGuildMessages)
	session.AddHandler(handle)
	err = session.Open()
	if err != nil {
		exit(err)
	}
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, os.Interrupt, os.Kill)
	<-sc
	session.Close()
}
