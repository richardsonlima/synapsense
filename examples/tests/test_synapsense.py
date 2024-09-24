import unittest
from src import ContextManager, PromptBuilder

class Testsynapsense(unittest.TestCase):
    def test_add_and_retrieve_context(self):
        cm = ContextManager()
        cm.add_context("test", ["example1", "example2"])
        self.assertEqual(cm.get_context("test"), ["example1", "example2"])

    def test_prompt_builder(self):
        cm = ContextManager()
        cm.add_context("test", ["example1", "example2"])
        pb = PromptBuilder(cm)
        prompt = pb.build_prompt("test", "input1")
        expected_prompt = "Example: example1\nExample: example2\nUser Input: input1\nModel Output:"
        self.assertEqual(prompt, expected_prompt)

if __name__ == '__main__':
    unittest.main()
