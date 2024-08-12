from http.server import HTTPServer

from src.app import hostName, serverPort, MyServer


def main() -> None:
    """
    Запускает HTTP-сервер и ожидает запросов.

    Создает экземпляр HTTPServer с указанными хостом и портом.
    Запускает сервер в бесконечном цикле, обрабатывая входящие запросы.
    При нажатии Ctrl+C (KeyboardInterrupt) сервер останавливается.
    """
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:

        webServer.serve_forever()
    except KeyboardInterrupt:

        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == '__main__':
    main()
