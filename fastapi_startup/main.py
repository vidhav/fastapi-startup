from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles


async def ping():
    return "pong"


async def swagger_ui_html(request: Request):
    app: FastAPI = request.app
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    oauth2_redirect_url = root_path + app.swagger_ui_oauth2_redirect_url

    site_name = app.extra.get("site_name", "Swagger UI")
    static_dir = app.extra.get("static_dir", "static")

    swagger_css_url = app.extra.get("swagger_css_url", "/assets/swagger-ui.min.css")
    if static_dir and swagger_css_url.startswith("/"):
        swagger_css_url = request.url_for("static", path=swagger_css_url)

    swagger_favicon_url = app.extra.get("swagger_favicon_url", "/assets/favicon.ico")
    if static_dir and swagger_favicon_url.startswith("/"):
        swagger_favicon_url = request.url_for("static", path=swagger_favicon_url)

    swagger_js_url = app.extra.get("swagger_js_url", "/assets/swagger-ui-bundle.min.js")
    if static_dir and swagger_js_url.startswith("/"):
        swagger_js_url = request.url_for("static", path=swagger_js_url)

    return get_swagger_ui_html(
        init_oauth=app.swagger_ui_init_oauth,
        oauth2_redirect_url=oauth2_redirect_url,
        openapi_url=openapi_url,
        swagger_css_url=swagger_css_url,
        swagger_favicon_url=swagger_favicon_url,
        swagger_js_url=swagger_js_url,
        swagger_ui_parameters=app.swagger_ui_parameters,
        title=f"{app.title} - {site_name}",
    )


async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


class FastAPIStartup(FastAPI):
    def setup(self) -> None:
        self.docs_url = None
        self.redoc_url = None
        self.swagger_ui_oauth2_redirect_url = "/oauth2-redirect"

        static_dir = self.extra.get("static_dir", "static")

        super().setup()

        if static_dir:
            self.mount(
                path="/static",
                app=StaticFiles(directory=static_dir),
                name="static",
            )

        self.add_api_route(
            endpoint=ping,
            include_in_schema=False,
            path="/ping",
            response_class=PlainTextResponse,
        )

        self.add_api_route(
            endpoint=swagger_ui_html,
            include_in_schema=False,
            path="/",
            response_class=HTMLResponse,
        )

        self.add_api_route(
            endpoint=swagger_ui_redirect,
            include_in_schema=False,
            path=self.swagger_ui_oauth2_redirect_url,
            response_class=HTMLResponse,
        )
