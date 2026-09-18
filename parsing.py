import socket
from urllib.parse import unquote_to_bytes


def decode_path(path):
    if not path:
        return ""
    return unquote_to_bytes(path).decode("utf-8")


def read_request(conn):
    data = b""

    while True:
        chunk = conn.recv(4096)
        if not chunk:
            return None

        data += chunk
        if b"\r\n\r\n" in data:
            break

    header_part, body_part = data.split(b"\r\n\r\n", 1)
    lines = header_part.decode("latin-1").splitlines()

    if not lines:
        raise ValueError("Empty request")

    method, target, protocol = lines[0].split()
    headers = {}

    for line in lines[1:]:
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()

    length = int(headers.get("content-length", "0"))
    while len(body_part) < length:
        chunk = conn.recv(4096)
        if not chunk:
            raise ValueError("Incomplete body")
        body_part += chunk

    body = body_part[:length]
    return method, target, protocol, headers, body
