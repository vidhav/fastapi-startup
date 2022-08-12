# FastAPI Startup

An opinionated startup extension for FastAPI.

## Usage

```python
from fastapi_startup import FastAPIStartup

app = FastAPIStartup(
    site_name="My site",
    swagger_favicon_url="https://example.com/favicon.ico",
)
```

## Opinions

This is an opinionated way to start FastAPI:

- No ReDoc.
- Swagger is hosted at the `root_path`.
- Swagger UI oAuth2 redirect URL is `/oauth2-redirect`.
- Endpoint `/ping` responds with the plain text response "pong".
- Mounts static directory at `/static` (default).
- Title and site name in Swagger
- Assets (expects these files in the directory `./static/assets`):
  - Favicon - `favicon.ico`.
  - Swagger CSS - `swagger-ui.min.css`.
  - Swagger Bundle JS - `swagger-ui-bundle.min.js`.

## Config

Configure FastAPI as usual. Extra arguments (that can be accessed from `app.extra`):

| Name | Default | Description |
| --- | --- | --- |
| `site_name` | Swagger UI | Displayed in the Swagger title, with `app.title`. |
| `static_dir` | static | Where to mount the static directory. Disabled if value is falsy. |
| `swagger_css_url` | /assets/swagger-ui.min.css | URL to Swagger UI CSS file. |
| `swagger_favicon_url` | /assets/favicon.ico | URL to your Favicon. |
| `swagger_js_url` | /assets/swagger-ui-bundle.min.js | URL to Swagger JS bundle file. |

*If the `swagger_` arguments starts with a "/" and static is mounted, they will be loaded from "static", else it will be treated as a URL.*
