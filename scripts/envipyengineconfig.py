"""

"""
from __future__ import print_function
import argparse

from envipyengine import config

system_option = argparse.ArgumentParser(add_help=False)
system_option.add_argument('-s', '--system', action='store_true',
                           help='set to modify the system config, defaults to the user config')

main_parser = argparse.ArgumentParser(
    description='Gets and sets config options for the envipyengine.'
)

sub_commands = main_parser.add_subparsers(help='sub-commands')

# GET COMMAND
def get(get_args):
    value = config.get(get_args.property_name)
    print(value)

get_command = sub_commands.add_parser('get',
                                       help='gets the envipyengine config option')
get_command.set_defaults(func=get)
get_command.add_argument('property_name', help='the name of the property to get')

# SET COMMAND
def set(set_args):
    config.set(set_args.property_name, args.value, system=args.system)

set_command = sub_commands.add_parser('set', 
                                      help='sets the envipyengine config option',
                                      parents=[system_option])
set_command.set_defaults(func=set)
set_command.add_argument('property_name', help='the name of the property to set')
set_command.add_argument('value', help='the value for the property')

# REMOVE COMMAND
def remove(remove_args):
    config.remove(remove_args.property_name, system=remove_args.system)

remove_command = sub_commands.add_parser('remove',
                                         help='removes the envipyengine config option',
                                         parents=[system_option])
remove_command.set_defaults(func=remove)
remove_command.add_argument('property_name', help='the name of the property to remove')

# PARSE
args = main_parser.parse_args()
args.func(args)
