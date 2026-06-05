NGINX_ROUTES = {
    "/": "frontend",
    "/api": "qverse-api",
    "/admin": "react-admin",
}


def get_nginx_routes() -> dict[str, str]:
    return NGINX_ROUTES.copy()
