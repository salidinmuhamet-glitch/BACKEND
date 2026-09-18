import http


def respond(conn, protocol, status, body):
    payload = body.encode("utf-8")
    response = (
        f"{protocol} {status} {http.HTTPStatus(status).phrase}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(payload)}\r\n\r\n"
    )
    conn.sendall(response.encode("utf-8") + payload)
