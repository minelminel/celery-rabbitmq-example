import sys
import typing
import logging
import argparse

class Configuration(object):

    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

    def __init__( self, log_level, log_file, stdout=True, drop_tables=False,
            root_route="/scraper", host="localhost",
            port=8080, debug=False, use_reloader=False
        ):
        self.log_level = log_level
        self.log_file = log_file
        self.stdout = stdout
        self.drop_tables = drop_tables
        self.root_route = root_route
        self.host = host
        self.port = port
        self.debug = debug
        self.use_reloader = use_reloader


def get_configuration():
    parser = argparse.ArgumentParser(description="Configure properties for use in development.")

    parser.add_argument(
        "-t",
        "--drop_tables",
        required=False,
        default=False,
        help="Whether to reset or keep the current database"
    )

    server_parser = parser.add_argument_group("server", "Server")

    server_parser.add_argument(
        "-r",
        "--serviceroot",
        required=False,
        default="/scraper/api",
        help="The root URL path that the server should listen on"
    )
    server_parser.add_argument(
        "-o",
        "--host",
        required=False,
        default="localhost",
        help="The host that the server should start on"
    )
    server_parser.add_argument(
        "-p",
        "--port",
        required=False,
        default=8080,
        help="The port that the server should start on"
    )
    server_parser.add_argument(
        "-d",
        "--debug",
        required=False,
        action="store_true",
        help="Whether the server should start in debug mode."
    )
    server_parser.add_argument(
        "-u",
        "--use_reloader",
        required=False,
        action="store_true",
        help="Whether the server should automatically restart on saved changes."
    )

    log_parser = parser.add_argument_group("log", "Logging")

    log_parser.add_argument(
        "-l",
        "--loglevel",
        default='WARN',
        required=False,
        choices=Configuration.log_levels,
        help="The log level of the application"
    )
    log_parser.add_argument(
        "-f",
        "--logfile",
        default=None,
        required=False,
        help="The log file for the application"
    )
    log_parser.add_argument(
        "-s",
        "--stdout",
        default=True,
        required=False,
        help="Whether to print the log to the terminal"
    )

    args = parser.parse_args()

    drop_tables = args.drop_tables
    log_level = args.loglevel
    log_file = args.logfile
    stdout = args.stdout
    service_root = args.serviceroot
    host = args.host
    port = args.port
    debug = args.debug
    use_reloader = args.use_reloader

    return Configuration(
        log_level,
        log_file,
        stdout,
        drop_tables,
        service_root,
        host,
        port,
        debug,
        use_reloader,
    )
