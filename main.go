package main

import (
	"github.com/BurntSushi/toml"
	"github.com/bwmarrin/discordgo"
	flag "github.com/spf13/pflag"
	"os"
	"os/signal"
)

var dish Dish

func main() {
	file := flag.StringP("dish", "d", "", ".dish file")
	flag.Parse()
	data, err := os.ReadFile(*file)
	if err != nil {
		exitOnError(err)
	}
	err = toml.Unmarshal(data, &dish)
	exitOnError(err)

	session, err := discordgo.New("Bot " + dish.Bot.Token)
	exitOnError(err)
	session.Identify.Intents = discordgo.MakeIntent(discordgo.IntentsGuildMessages)
	session.AddHandler(handler)
	err = session.Open()
	exitOnError(err)
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, os.Interrupt, os.Kill)
	<-sc
	session.Close()
}
