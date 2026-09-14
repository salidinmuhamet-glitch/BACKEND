import socket
import http
from html import escape

PATHS = {
    "/": "<h1>Home page</h1>",
    "/page1": "<h1>Page 1</h1>",
    "/page2": "<h1>Page 2</h1>",
    "/page3": "<h1>Page 3</h1>",
    "/page4": "<h1>Page 4</h1>",
    "/page5": "<h1>Page 5</h1>",
    "/hello": "<h1>Hello {0} </h1>",
}

def respond(conn, status, protocol, body):
    body_len = len(body.encode())
    response = (f"{protocol} {status} {http.HTTPStatus(status).phrase}\r\n"
                f"Content-Type: text/html\r\n"
                f"Content-Length: {body_len}\r\n\r\n"
                f"{body}")
    conn.sendall(response.encode())


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
    server.listen(5)
    while True:
        conn, _ = server.accept()
        req = conn.recv(1024)
        arr_req = req.decode().splitlines()
        method, path, protocol = arr_req[0].split()

        if not req:
            conn.close()
            continue



        if method == 'GET':
            status = 200 if path in PATHS.keys() else 404
            segments = path.strip("/").split("/")
            body = PATHS.get(f"/{segments[0]}", "<h1>Page Not Found</h1>") if len(segments) <= 1 \
                else PATHS[f"{segments[0]}"].format(segments[0])
            respond(conn, status,protocol, body)
        elif method == 'POST':
            headers, _, request_body = req.decode().partition("\r\n\r\n")
            content_length = 0
            for header in headers.splitlines()[1:]:
                name, separator, value = header.partition(":")
                if separator and name.lower() == "content-length":
                    content_length = int(value.strip())
                    break

            body = request_body[:content_length]
            response_body = f"<h1>POST data: {escape(body)}</h1>"
            respond(conn, 200, protocol, response_body)
        else:
            status = 405
            body = "<h1>405 - Method Not Allowed</h1>"
            respond(conn, status,protocol, body)
        conn.close()
if __name__ == '__main__':
    main()