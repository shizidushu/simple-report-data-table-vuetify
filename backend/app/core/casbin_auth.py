
from typing import Callable, List, Dict
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response


class CasbinRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # start process/handle request; after call_next(request) in middleware

            request.state.path = self.path
            request.state.tags = self.tags

            # print("in casbin route")

            # start execute corresponding path function to process request
            response: Response = await original_route_handler(request)
            # after execute path function; before do something to response in middleware

            return response

        return custom_route_handler


# concatenate tags in reverse order
def join_tags(tags: List[str]) -> str:
    return '_'.join(tags[::-1])

# extract all path operation's path, method, tags that need casbin auth from openapi schema
def extract_path_info_of_tag(app: FastAPI, tag_name: str) -> List[Dict]:
    openapi_schema = app.openapi()
    openapi_paths = openapi_schema['paths']
    extracted_paths = [{'path': k, 'method': method, 'tags': join_tags(config['tags'])} for k, v in openapi_paths.items(
    ) for method, config in v.items() if config['tags'].count(tag_name) > 0]
    return extracted_paths
