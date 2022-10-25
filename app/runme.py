from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler

import psycopg2
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from proj01.spiders.sreality import SrealitySpider
import logging

conn = psycopg2.connect(
    host="db",
    database="srealitydb",
    user="postgres",
    password="root")

hostName = "0.0.0.0"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):

        cursor = conn.cursor()
        postgreSQL_select_Query = "SELECT title, image FROM properties"

        cursor.execute(postgreSQL_select_Query)
        sproperties = cursor.fetchall()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><meta content='text/html;charset=utf-8' http-equiv='Content-Type'><meta content='utf-8' http-equiv='encoding'><title>Demo server</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))

        for row in sproperties:
            self.wfile.write(bytes(row[0] + " <img src='" + row[1] + "'><br>", "utf-8"))

        self.wfile.write(bytes("</body>", "utf-8"))


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(SrealitySpider)
    process.start()
    
    run_server()
    


def run_server():
    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    SimpleHTTPRequestHandler.extensions_map = {k: v + ';charset=UTF-8' for k, v in
                                               SimpleHTTPRequestHandler.extensions_map.items()}
    logging.warning("Server started http://%s:%s" % (hostName, serverPort))
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
   
    webServer.server_close()
    logging.warning("Server stopped.")


if __name__ == "__main__":
    main()
