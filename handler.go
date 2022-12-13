package main

import (
	"bytes"
	"fmt"
	"github.com/bwmarrin/discordgo"
	"github.com/mattn/go-shellwords"
)

func handle(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Author.ID == s.State.User.ID {
		return
	}

	args, err := shellwords.Parse(m.Content)
	if err != nil {
		return
	}
	command, ok := dish.Commands[args[0]]
	if !ok {
		return
	}
	if command.Args {
		args = append(command.Command, args[1:]...)
	} else {
		args = command.Command
	}
	result, err := command.Run(args)
	if err != nil {
		return
	}
	lines := bytes.Split(result, []byte{'\n'})
	buf := &bytes.Buffer{}
	msg, err := s.ChannelMessage(m.ChannelID, m.ID)
	if err != nil {
		return
	}
	for _, line := range lines {
		if buf.Len()+len(line)+13 > 2000 {
			text := fmt.Sprintf("```ansi\n%s```", buf.String())
			msg, err = s.ChannelMessageSendReply(m.ChannelID, text, msg.Reference())
			if err != nil {
				fmt.Println(err)
				return
			}
			buf.Truncate(0)
		}
		buf.Write(line)
		buf.WriteByte('\n')
	}
	if buf.Len() > 0 {
		text := fmt.Sprintf("```ansi\n%s```", buf.String())
		msg, err = s.ChannelMessageSendReply(m.ChannelID, text, msg.Reference())
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}
