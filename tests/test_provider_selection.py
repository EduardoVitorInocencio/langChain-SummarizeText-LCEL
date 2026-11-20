import os
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

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
                        self.assertIs(
                            main.create_chat_model(), model_class.return_value
                        )
                        self.assertEqual(
                            model_class.call_args.kwargs["model"], "test-model"
                        )

    def test_defaults_to_ollama(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(main, "ChatOllama") as model_class:
                main.create_chat_model()
                self.assertEqual(model_class.call_args.kwargs["model"], "llama3.2")

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
            ("openai", "OPENAI_API_KEY", main.ChatOpenAI, "gpt-4o-mini"),
            (
                "google",
                "GOOGLE_API_KEY",
                main.ChatGoogleGenerativeAI,
                "gemini-3.8-flash",
            ),
            ("ollama", None, main.ChatOllama, "llama3.2"),
        ]
        for provider, api_key, model_class, expected_name in cases:
            with self.subTest(provider=provider):
                environment = {"LLM_PROVIDER": provider}
                if api_key:
                    environment[api_key] = "test-key"
                with patch.dict(os.environ, environment, clear=True):
                    model = main.create_chat_model()
                    self.assertIsInstance(model, model_class)
                    self.assertEqual(main.get_model_name(model), expected_name)

    def test_summary_prints_the_active_model(self):
        model = RunnableLambda(lambda _: AIMessage(content="Resumo teste"))
        model.model = "test-model"
        output = StringIO()
        with patch.object(main, "create_chat_model", return_value=model):
            with redirect_stdout(output):
                summary = main.summarize_information("Uma biografia")
        self.assertEqual(summary, "Resumo teste")
        self.assertIn("Modelo em uso: test-model", output.getvalue())


if __name__ == "__main__":
    unittest.main()
