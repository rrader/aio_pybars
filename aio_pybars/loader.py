import os

import pybars
import re


class TemplateIncludeProxy:
    """
    Template proxy that handles recursively include directive
    """

    INCLUDE_COMMENT = re.compile(r'{{!<[ ]*([^}]+)}}')

    def __init__(self, template_source, loader):
        self.loader = loader
        self.template = loader.compiler.compile(template_source)
        self.base_template_name = self._load_base_template(template_source)

    def _load_base_template(self, template_source):
        first_line = template_source.split("\n", 1)[0]
        if self.INCLUDE_COMMENT.match(first_line):
            base_name = self.INCLUDE_COMMENT.findall(first_line)[0]
            return base_name

    def __call__(self, context=None, **kwargs):
        if not context:
            context = {}
        template = self.template
        if self.base_template_name:
            template = self.loader.get_template(self.base_template_name)
            body = self.template(context, **kwargs)
            context.update({"body": body})
        return template(context, **kwargs)


class FSTemplateLoader:
    """
    Loads template files from the file system.
    """
    def __init__(self, app, base_dir):
        self.app = app
        self.base_dir = base_dir
        self.compiler = pybars.Compiler()

    def get_template(self, name):
        """
        Loads template by name by appending the .hbs extension to it.
        Returns the proxy object that handles recursive includes for templates.
        """
        with open(os.path.join(self.base_dir, name + ".hbs"), 'r', encoding='utf8') as f:
            template_source = f.read()

        return TemplateIncludeProxy(template_source, self)

    def get_partials(self):
        return {}

    def get_helpers(self):
        return {}
