from pathlib import Path

import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

from config import WEB_PATH

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    local_filename: Path = WEB_PATH
    remote_filename_url = "https://raw.githubusercontent.com/Altair788/HW19_1/main/remote_web.html"

    def get_context_data(self):
        """
        Читает содержимое локального HTML-файла и возвращает его.

        Открывает файл, указанный в атрибуте `local_filename`, и считывает его содержимое.
        Если файл успешно открыт, возвращает текстовое содержимое файла.

        Returns:
            str: Содержимое HTML-файла в виде строки.

        Raises:
            FileNotFoundError: Если файл не найден.
            IOError: Если произошла ошибка при чтении файла.
        """
        with open(self.local_filename, "r", encoding="utf-8") as f:
            context = f.read()
        return context

    def get_context_data_from_git(self):
        """
        Метод получает HTML-код страницы из GitHub в формате raw content и возвращает его.

        Выполняет HTTP GET-запрос к указанному URL, чтобы получить HTML-содержимое.
        Если запрос успешен, возвращает текст ответа. В противном случае возвращает
        сообщение об ошибке.

        Returns:
            str: HTML-код страницы, если запрос успешен; иначе сообщение об ошибке.
        """
        response = requests.get(self.remote_filename_url)
        return response.text if response.status_code == 200 else "<h1>Error loading page</h1>"

    def do_GET(self) -> None:
        """
        Метод для обработки входящих GET-запросов
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        #  локальная версия
        # self.wfile.write(bytes(self.get_context_data(), "utf-8"))
        self.wfile.write(bytes(self.get_context_data_from_git(), "utf-8"))


if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:

        webServer.serve_forever()
    except KeyboardInterrupt:

        pass

    webServer.server_close()
    print("Server stopped.")
