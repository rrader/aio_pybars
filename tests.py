import unittest
from unittest.mock import Mock, call

from aio_pybars.loader import TemplateIncludeProxy


class TestIncludeProxy(unittest.TestCase):
    def setUp(self):
        self.app = object()

    def test_no_base(self):
        template_without_base = "hello\n{{var}}"
        loader = Mock()

        template = TemplateIncludeProxy(template_without_base, loader)
        self.assertEqual("hello\nworld", template(context={"var": "world"}))
        loader.assert_not_called()

    def test_base(self):
        template_with_base = "{{!< base_template}}hello\n{{var}}"
        base_template = "base: {{body}}"

        loader = Mock()
        loader.get_template = Mock(return_value=TemplateIncludeProxy(base_template, loader))

        template = TemplateIncludeProxy(template_with_base, loader)
        self.assertEqual("base: hello\nworld", template(context={"var": "world"}))
        loader.get_template.assert_has_calls([call("base_template")])

    def test_recursive_base(self):
        template_with_base = "{{!< base_template1}}may the {{var}}"
        base_template_1 = "{{!< base_template2}}{{body}} be"
        base_template_2 = "{{body}} with you"

        loader = Mock()
        loader.get_template = Mock()
        loader.get_template.side_effect = [TemplateIncludeProxy(base_template_1, loader),
                                           TemplateIncludeProxy(base_template_2, loader)]

        template = TemplateIncludeProxy(template_with_base, loader)
        self.assertEqual("may the force be with you", template(context={"var": "force"}))
        loader.get_template.assert_has_calls([call("base_template1"), call("base_template2")])


if __name__ == '__main__':
    unittest.main()
