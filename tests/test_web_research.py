import unittest

from runtime.web_research import WebResearch


class TestWebResearch(unittest.TestCase):
    def test_empty_topic_is_rejected(self):
        research = WebResearch()

        with self.assertRaises(ValueError):
            research.search("")

    def test_topic_is_encoded_into_search_url(self):
        research = WebResearch(
            search_url="https://example.com/search?q="
        )

        captured = {}

        class FakeResponse:
            def read(self):
                return b"test result"

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["timeout"] = timeout
            return FakeResponse()

        import runtime.web_research as module

        original = module.urlopen
        module.urlopen = fake_urlopen

        try:
            result = research.search("Python programming")
        finally:
            module.urlopen = original

        self.assertEqual(
            result.topic,
            "Python programming",
        )
        self.assertEqual(
            result.content,
            "test result",
        )
        self.assertIn(
            "Python%20programming",
            captured["url"],
        )


if __name__ == "__main__":
    unittest.main()
