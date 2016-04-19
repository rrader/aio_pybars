aio_pybars
========

Quick Start
------------------

0. Install::

    pip install aio_pybars

OR via setup.py::

    python setup.py install

1. Configure your app::

    from aio_pybars import FSTemplateLoader
    loop.run_until_complete(aio_pybars.setup(app,
                                             templates_dir=config['TEMPLATES_DIR'],
                                             Loader=FSTemplateLoader))

2. Use templates in the view::

    async def index(request):
        context = {"var": "value"}
        return AIOBarsResponse(request, 'template_name', context)

It will render the `template_name.hbs` template with variables in the `context` to the aiohttp response.

Helpers and partials
------------------------------------

Partial is the nested template that should be included in the specific place.
If the following code occurs in the template::

    {{> "sidebar"}}

pybars3 will search the _partial_ named `sidebar` in the dictionary. How to add your own partial see below.

Helper is the callable that can be called from the template. Syntactically it looks same as the variable, but can
get the arguments::

    <link rel="shortcut icon" href="{{asset "favicon.ico"}}">

would call the `asset` callable with "favicon.ico" argument and put the results in the rendered template.

*To use your own partials and helpers* implement your subclass of templates loader::

    class AppFSTemplateLoader(FSTemplateLoader):
        def __init__(self, app, base_dir):
            super().__init__(app, base_dir)

        def get_partials(self):
            """
            Load all files in the partials/ subdirectory of templates dir.
            Method should return the dictionary {'partial_name': <compiled template>, ...}
            """
            partials = super().get_partials()
            base_partials = os.path.join(self.app.config['TEMPLATES_DIR'], 'partials')
            for name in os.listdir(base_partials):
                filename = os.path.splitext(name)[0]
                template_source = open(os.path.join(base_partials, name), 'r', encoding='utf8').read()
                template = self.compiler.compile(template_source)
                partials[filename] = template
            return partials

        def get_helpers(self):
            """
            Define your own set of helpers.
            Method should return the dictionary {'helper_name': <callable>, ...}
            """
            helpers = super().get_helpers()
            helpers.update({"asset": _asset})
            return helpers


    def _asset(options, val, *args, **kwargs):
        return "/static/{}".format(val)

and pass it as Loader argument to the setup::

    loop.run_until_complete(aio_pybars.setup(app,
                                             templates_dir=config['TEMPLATES_DIR'],
                                             Loader=AppFSTemplateLoader))

Recursive rendering of templates
--------------------------

The aio_pybars enables templates to be recursive. If the first line of the template contains::

    {{!< base_template}}

all the rendered template will be passed as variable `body` to the base template.

For example:

base.hbs::

    <!DOCTYPE html>
    <html>
    <head>
        <title>Template</title>
    </head>
    <body>
        {{body}}
    </body>

test.hbs::

    {{!< base}}
    Hello, {{name}}.

Then result of the `render(loader, 'test', {'name': 'Roma'})` will be::

    <!DOCTYPE html>
    <html>
    <head>
        <title>Template</title>
    </head>
    <body>
        Hello, Roma
    </body>
