# pylint: disable=C0103,C0111

import json
import unittest
import mock
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from bumblebee.output import I3BarOutput
from tests.util import MockWidget
from tests.util import MockTheme

class TestI3BarOutput(unittest.TestCase):
    def setUp(self):
        self.theme = MockTheme()
        self.output = I3BarOutput(self.theme)
        self.expectedStart = json.dumps({"version": 1, "click_events": True}) + "[\n"
        self.expectedStop = "]\n"
        self.someWidget = MockWidget("foo bar baz")

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_start(self, stdout):
        self.output.start()
        self.assertEquals(self.expectedStart, stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_stop(self, stdout):
        self.output.stop()
        self.assertEquals(self.expectedStop, stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_draw_single_widget(self, stdout):
        self.output.draw(self.someWidget)
        self.output.flush()
        result = json.loads(stdout.getvalue())[0]
        self.assertEquals(result["full_text"], self.someWidget.full_text())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_draw_multiple_widgets(self, stdout):
        for widget in [self.someWidget, self.someWidget]:
            self.output.draw(widget)
        self.output.flush()
        result = json.loads(stdout.getvalue())
        for res in result:
            self.assertEquals(res["full_text"], widget.full_text())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_begin(self, stdout):
        self.output.begin()
        self.assertEquals("", stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_end(self, stdout):
        self.output.end()
        self.assertEquals(",\n", stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_prefix(self, stdout):
        self.theme.set_prefix(" - ")
        self.output.draw(self.someWidget)
        self.output.flush()
        result = json.loads(stdout.getvalue())[0]
        self.assertEquals(result["full_text"], "{}{}".format(
            self.theme.prefix(self.someWidget), self.someWidget.full_text())
        )

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_suffix(self, stdout):
        self.theme.set_suffix(" - ")
        self.output.draw(self.someWidget)
        self.output.flush()
        result = json.loads(stdout.getvalue())[0]
        self.assertEquals(result["full_text"], "{}{}".format(
            self.someWidget.full_text(), self.theme.suffix(self.someWidget))
        )

    @mock.patch("sys.stdout", new_callable=StringIO)
    def test_bothfix(self, stdout):
        self.theme.set_suffix(" - ")
        self.theme.set_prefix(" * ")
        self.output.draw(self.someWidget)
        self.output.flush()
        result = json.loads(stdout.getvalue())[0]
        self.assertEquals(result["full_text"], "{}{}{}".format(
            self.theme.prefix(self.someWidget), self.someWidget.full_text(), self.theme.suffix(self.someWidget))
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
