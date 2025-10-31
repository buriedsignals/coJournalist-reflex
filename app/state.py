import reflex as rx
from typing import Literal, TypedDict, cast
import os
import logging

Mode = Literal["SCRAPE", "DATA", "INVESTIGATE", "FACT-CHECK", "GRAPHICS"]


class Message(TypedDict):
    role: str
    content: str
    image: str | None
    source: str | None


class ScrapeResult(TypedDict):
    success: bool
    title: str
    preview: str
    url: str
    error: str | None


class AppState(rx.State):
    active_mode: Mode = "SCRAPE"
    chat_history: list[Message] = []
    current_question: str = ""
    is_loading: bool = False
    scrape_url: str = ""
    scrape_schedule: str = ""
    scrape_criteria: str = ""
    scrape_monitoring: str = "EMAIL"
    scraped_data: ScrapeResult | None = None
    hf_space_urls: dict[Mode, str] = {
        "GRAPHICS": "https://huggingface.co/spaces/coJournalist/cojournalist-graphics",
        "INVESTIGATE": "https://huggingface.co/spaces/coJournalist/cojournalist-investigate",
        "FACT-CHECK": "https://huggingface.co/spaces/coJournalist/coJournalist-Fact-Check",
        "DATA": "https://huggingface.co/spaces/coJournalist/cojournalist-data",
        "SCRAPE": "",
    }

    @rx.var
    def chat_disabled(self) -> bool:
        if self.active_mode == "SCRAPE":
            return self.is_loading or self.scraped_data is None
        return self.is_loading

    @rx.var
    def modes(self) -> list[str]:
        return ["SCRAPE", "DATA", "INVESTIGATE", "FACT-CHECK", "GRAPHICS"]

    @rx.var
    def show_scrape_sidebar(self) -> bool:
        return self.active_mode == "SCRAPE"

    @rx.event
    def set_active_mode(self, mode: str):
        self.active_mode = cast(Mode, mode)

    @rx.event
    async def process_chat(self, form_data: dict):
        question = form_data.get("question", "").strip()
        if not question:
            return
        self.is_loading = True
        self.current_question = ""
        self.chat_history.append(
            {"role": "user", "content": question, "image": None, "source": None}
        )
        yield
        try:
            if self.active_mode == "SCRAPE":
                await self._dummy_response(question)
            else:
                self.chat_history.append(
                    {
                        "role": "assistant",
                        "content": f"The {self.active_mode} mode opens in a new tab. Click 'Open Space' to start.",
                        "image": None,
                        "source": "System",
                    }
                )
        except Exception as e:
            logging.exception(f"Error processing chat: {e}")
            self.chat_history.append(
                {
                    "role": "assistant",
                    "content": f"An error occurred: {str(e)}",
                    "image": None,
                    "source": "Error",
                }
            )
        finally:
            self.is_loading = False
            yield

    @rx.event(background=True)
    async def handle_scrape(self):
        import requests
        import json

        async with self:
            if not self.scrape_url:
                return
            self.is_loading = True
            self.scraped_data = None
            self.chat_history = []
        payload = {
            "url": self.scrape_url,
            "schedule": self.scrape_schedule,
            "criteria": self.scrape_criteria,
            "monitoring": self.scrape_monitoring,
        }
        webhook_url = "https://n8n-cojournalist.onrender.com/webhook/lipsum"
        try:
            response = requests.post(webhook_url, json=payload, timeout=15)
            response.raise_for_status()
            response_data = response.json()
            scraped_data = {
                "success": True,
                "title": response_data.get("title", "Scrape Result"),
                "preview": response_data.get(
                    "preview", "The webhook returned a response."
                ),
                "url": self.scrape_url,
                "error": None,
            }
            async with self:
                self.scraped_data = cast(ScrapeResult, scraped_data)
                self.chat_history.append(
                    {
                        "role": "assistant",
                        "content": self.scraped_data["title"],
                        "image": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                        "source": self.scraped_data["url"],
                    }
                )
                self.chat_history.append(
                    {
                        "role": "assistant",
                        "content": "Scrape successful. Please review the result. You can now use the chat to proceed.",
                        "image": None,
                        "source": None,
                    }
                )
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error calling N8N webhook: {e}")
            async with self:
                self.chat_history.append(
                    {
                        "role": "assistant",
                        "content": f"Failed to trigger scrape workflow. Error: {str(e)}",
                        "image": None,
                        "source": "System Error",
                    }
                )
        finally:
            async with self:
                self.is_loading = False

    async def _dummy_response(self, question: str):
        from langchain_huggingface import HuggingFaceEndpoint
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain

        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            max_length=128,
            temperature=0.7,
            huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_KEY"),
        )
        template = f"You are an AI assistant in '{self.active_mode}' mode. Answer the user's question: '{{question}}'"
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        try:
            response = await llm_chain.ainvoke(question)
            response_content = response["text"]
        except Exception as e:
            logging.exception(f"Error calling Hugging Face: {e}")
            response_content = "Sorry, I couldn't process your request at the moment."
        async with self:
            image = None
            source = None
            if self.active_mode == "GRAPHICS":
                image = "/placeholder.svg"
                source = "AI Art Generator"
            self.chat_history.append(
                {
                    "role": "assistant",
                    "content": response_content,
                    "image": image,
                    "source": source,
                }
            )