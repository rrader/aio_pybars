from .loader import FSTemplateLoader
from .render import render, AIOBarsResponse


async def setup(app, templates_dir, Loader=FSTemplateLoader):
    app['loader'] = Loader(app, templates_dir)
