from http.server import BaseHTTPRequestHandler

import psycopg2
import logging

conn = psycopg2.connect(
    host="db",
    database="srealitydb",
    user="postgres",
    password="root")

hostName = "0.0.0.0"
serverPort = 8080

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        cursor = conn.cursor()
        postgreSQL_select_Query = "SELECT title, image FROM properties"

        cursor.execute(postgreSQL_select_Query)
        sproperties = cursor.fetchall()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(
            "<html><head><meta content='text/html;charset=utf-8' http-equiv='Content-Type'><meta content='utf-8' http-equiv='encoding'><title>Sreality scrape web</title></head>",
            "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))

        for row in sproperties:
            self.wfile.write(bytes(row[0] + " <img src='" + row[1] + "'><br>", "utf-8"))

        self.wfile.write(bytes("</body>", "utf-8"))
