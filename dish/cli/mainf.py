import argparse
import os

import discord
import toml

import dish

parser: argparse.ArgumentParser = ...
args: argparse.Namespace = ...
config: dish.Config = ...


def preinit(client: discord.Client) -> None:
    ...


async def postinit(client: discord.Client) -> None:
    ...


async def handler(client: discord.Message) -> bool:
    return False


def main():
    parse()
    check()
    configure()
    run()


def parse():
    global parser, args

    parser = argparse.ArgumentParser(description="Discord command line interface")
    parser.add_argument(
        "-p",
        "--path",
        help="Path to directory containing configuration files, defaults to current directory",
        default=os.getcwd(),
    )

    args = parser.parse_args()


def check():
    if not os.path.isdir(args.path):
        print(f"Directory {args.path} does not exist")
        exit(1)


def configure():
    global config

    os.chdir(args.path)
    config = toml.load("config.dish", _dict=dish.Config)
    config["preinit"] = preinit
    config["postinit"] = postinit
    config["handler"] = handler


def run():
    dish.Bot(config).run()
