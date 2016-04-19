from .loader import FSTemplateLoader
from .render import render, AIOBarsResponse


async def setup(app, Loader=FSTemplateLoader):
    app['loader'] = Loader(app, app['config']['TEMPLATES_DIR'])
