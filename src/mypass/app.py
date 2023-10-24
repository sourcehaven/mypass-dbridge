import multiprocessing
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from . import config
from .config import AppConfig
from .routers import auth, teapot


class App(FastAPI):
    debug: bool
    _instance: 'App'

    def __init__(self):
        app_config = getattr(config, f'{os.environ.get("MYPASS_ENV", "")}Config')
        super().__init__(
            debug=app_config.DEBUG,
            title='MyPass',
            summary='MyPass restful bridge service.',
            description='Service acting as a bridge between database and frontend applications.'
        )

        routers = [auth.router, teapot.router]
        for router in routers:
            self.include_router(router)
        self._config = AppConfig.from_object(app_config)

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance

    def run(self):
        if self.debug:
            uvicorn.run(
                'mypass.app:app', host=self.config.get('HOST'), port=self.config.get('PORT'),
                reload=True, reload_dirs=[str(Path(__file__).parent)])
        else:
            uvicorn.run(
                'mypass.app:app', host=self.config.get('HOST'), port=self.config.get('PORT'),
                workers=multiprocessing.cpu_count() + 1)

    @property
    def config(self):
        return self._config


app = App()


def create_app():
    return App()
