import unittest
from synapsense import ContextManager, PromptBuilder

class Testsynapsense(unittest.TestCase):
    def test_add_and_retrieve_context(self):
        cm = ContextManager()
        cm.add_context("test", ["example1", "example2"])
        self.assertEqual(cm.get_context("test"), ["example1", "example2"])

    def test_prompt_builder(self):
        cm = ContextManager()
        cm.add_context("test", ["example1", "example2"])
        pb = PromptBuilder(cm)

        # Assume that the user input is "input1"
        prompt = pb.build_prompt("test", "input1")

        # Here we should specify what the expected prompt output would be based on 
        # the relevant examples. Adjust this according to the logic in PromptBuilder.
        expected_prompt = (
            "Example: example1\n"
            "Example: example2\n"
            "User Input: input1\n"
            "Please respond based on the above context"
        )
        self.assertEqual(prompt, expected_prompt)

    def test_extract_keywords(self):
        cm = ContextManager()
        pb = PromptBuilder(cm)

        keywords = pb.extract_keywords("This is a sample input for testing.")
        expected_keywords = ['sample', 'input', 'testing']
        self.assertEqual(keywords, expected_keywords)

    def test_find_relevant_examples(self):
        cm = ContextManager()
        cm.add_context("test", ["example about testing", "irrelevant example", "another test example"])
        pb = PromptBuilder(cm)

        keywords = ['test']
        relevant_examples = pb.find_relevant_examples(cm.get_context("test"), keywords)
        expected_relevant_examples = ["example about testing", "another test example"]
        self.assertEqual(relevant_examples, expected_relevant_examples)

    def test_calculate_similarity(self):
        cm = ContextManager()
        pb = PromptBuilder(cm)

        similarity = pb.calculate_similarity("this is an example", ["example", "sample"])
        self.assertGreater(similarity, 0)  # Ensure that there is some similarity

if __name__ == '__main__':
    unittest.main()