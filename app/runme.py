from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler

import psycopg2
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from proj01.spiders.sreality import SrealitySpider
from server import WebServer
import logging

conn = psycopg2.connect(
    host="db",
    database="srealitydb",
    user="postgres",
    password="root")

hostName = "0.0.0.0"
serverPort = 8080


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(SrealitySpider)
    process.start()
    run_server()


def run_server():
    webServer = HTTPServer((hostName, serverPort), WebServer)
    SimpleHTTPRequestHandler.extensions_map = {k: v + ';charset=UTF-8' for k, v in
                                               SimpleHTTPRequestHandler.extensions_map.items()}
    logging.warning("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    main()
