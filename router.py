from urllib.parse import urlsplit

from config import ROUTES
from http_utils import respond
from parsing import decode_path

MESSAGES = []


def home():
    return "<h1>Homepage</h1>"


def about():
    return "<h1>About</h1>"


def contacts():
    return "<h1>Contacts</h1>"


def help_page():
    return "<h1>Help</h1>"


def hello(name=""):
    return f"<h1>Hello, {name}</h1>"


def render_messages():
    if not MESSAGES:
        return ""
    return "\n".join(MESSAGES)


def route(path, method):
    if method == "GET" and path.startswith("/hello/"):
        return "/hello"
    if path in ROUTES and method in ROUTES[path]:
        return path
    return None


def dispatch(conn, method, path, protocol, body):
    clean_path = urlsplit(path).path
    decoded = decode_path(clean_path)

    if method not in {"GET", "POST"}:
        respond(conn, protocol, 405, "<h1>Method Not Allowed</h1>")
        return

    if route(decoded, method) is None:
        respond(conn, protocol, 404, "<h1>Page Not Found</h1>")
        return

    if method == "GET":
        if decoded == "/":
            respond(conn, protocol, 200, home())
        elif decoded == "/about":
            respond(conn, protocol, 200, about())
        elif decoded == "/contacts":
            respond(conn, protocol, 200, contacts())
        elif decoded == "/help":
            respond(conn, protocol, 200, help_page())
        elif decoded == "/hello":
            respond(conn, protocol, 200, hello())
        elif decoded.startswith("/hello/"):
            name = decoded[len("/hello/") :]
            respond(conn, protocol, 200, hello(name))
        elif decoded == "/messages":
            respond(conn, protocol, 200, render_messages())
        else:
            respond(conn, protocol, 404, "<h1>Page Not Found</h1>")

    elif method == "POST":
        if decoded == "/messages":
            message = body.decode("utf-8", errors="replace")
            MESSAGES.append(message)
            respond(conn, protocol, 201, "<h1>Created</h1>")
        else:
            respond(conn, protocol, 405, "<h1>Method Not Allowed</h1>")
