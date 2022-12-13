package main

import (
	flag "github.com/spf13/pflag"
	"os/exec"
)

type Dish struct {
	Bot      Bot
	Commands map[string]*Command
}

type Bot struct {
	Token  string
	Status string
}

type Command struct {
	Command     []string
	Args        bool
	Description string
	flagSet     *flag.FlagSet
}

func (c *Command) Run(args []string) ([]byte, error) {
	cmd := exec.Command(args[0], args[1:]...)
	return cmd.CombinedOutput()
}
