import os
import unittest
from unittest.mock import patch

import main


class ProviderSelectionTests(unittest.TestCase):
    def test_selects_each_provider_and_model(self):
        cases = [
            ("openai", "OPENAI_API_KEY", "OPENAI_MODEL", "ChatOpenAI"),
            ("google", "GOOGLE_API_KEY", "GOOGLE_MODEL", "ChatGoogleGenerativeAI"),
            ("ollama", None, "OLLAMA_MODEL", "ChatOllama"),
        ]
        for provider, api_key, model_var, constructor in cases:
            with self.subTest(provider=provider):
                environment = {"LLM_PROVIDER": provider, model_var: "test-model"}
                if api_key:
                    environment[api_key] = "test-key"
                with patch.dict(os.environ, environment, clear=True):
                    with patch.object(main, constructor) as model_class:
                        self.assertIs(main.create_chat_model(), model_class.return_value)
                        self.assertEqual(model_class.call_args.kwargs["model"], "test-model")

    def test_defaults_to_openai(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True):
            with patch.object(main, "ChatOpenAI") as model_class:
                main.create_chat_model()
                self.assertEqual(model_class.call_args.kwargs["model"], "gpt-4o-mini")

    def test_missing_api_key_is_reported(self):
        for provider in ("openai", "google"):
            with self.subTest(provider=provider):
                with patch.dict(os.environ, {"LLM_PROVIDER": provider}, clear=True):
                    with self.assertRaisesRegex(ValueError, "API_KEY is required"):
                        main.create_chat_model()

    def test_unknown_provider_is_reported(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "unknown"}, clear=True):
            with self.assertRaisesRegex(ValueError, "Unsupported LLM_PROVIDER"):
                main.create_chat_model()

    def test_real_models_can_be_constructed_without_api_calls(self):
        cases = [
            ("openai", "OPENAI_API_KEY", main.ChatOpenAI),
            ("google", "GOOGLE_API_KEY", main.ChatGoogleGenerativeAI),
            ("ollama", None, main.ChatOllama),
        ]
        for provider, api_key, model_class in cases:
            with self.subTest(provider=provider):
                environment = {"LLM_PROVIDER": provider}
                if api_key:
                    environment[api_key] = "test-key"
                with patch.dict(os.environ, environment, clear=True):
                    self.assertIsInstance(main.create_chat_model(), model_class)


if __name__ == "__main__":
    unittest.main()
