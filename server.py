import socket

from http_utils import respond
from parsing import read_request
from router import dispatch


def serve(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)

    while True:
        conn, _ = server.accept()
        conn.settimeout(5)

        try:
            request = read_request(conn)
            if not request:
                conn.close()
                continue

            method, target, protocol, headers, body = request

            if protocol not in {"HTTP/1.0", "HTTP/1.1"}:
                respond(conn, protocol, 400, "<h1>Bad Request</h1>")
                conn.close()
                continue

            if method not in {"GET", "POST"}:
                respond(conn, protocol, 405, "<h1>Method Not Allowed</h1>")
                conn.close()
                continue

            dispatch(conn, method, target, protocol, body)

        except (TimeoutError, ValueError):
            respond(conn, "HTTP/1.1", 400, "<h1>Bad Request</h1>")

        finally:
            conn.close()
