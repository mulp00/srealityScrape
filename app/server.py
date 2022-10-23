from http.server import BaseHTTPRequestHandler

import psycopg2
import logging

conn = psycopg2.connect(
    host="localhost",
    database="srealitydb",
    user="postgres",
    password="root")

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        cursor = conn.cursor()
        postgreSQL_select_Query = "select title, image from properties"

        cursor.execute(postgreSQL_select_Query)
        sproperties = cursor.fetchall()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Demo server</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))

        for row in sproperties:
            self.wfile.write(bytes("title: " + row[0] + " <img src='" + row[1] + "'>", "utf-8"))

        self.wfile.write(bytes("</body>", "utf-8"))
