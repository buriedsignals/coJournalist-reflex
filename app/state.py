import reflex as rx
import reflex_clerk_api as clerk
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
    active_scrape_sidebar_tab: str = "Scraper Setup"
    chat_histories: dict[Mode, list[Message]] = {
        "SCRAPE": [],
        "DATA": [],
        "INVESTIGATE": [],
        "FACT-CHECK": [],
        "GRAPHICS": [],
    }
    current_question: str = ""
    is_loading: bool = False
    scrape_url: str = ""
    scrape_schedule: str = ""
    scrape_criteria: str = ""
    scrape_monitoring: str = "EMAIL"
    scraped_data: ScrapeResult | None = None
    show_about_modal: bool = False
    scheduled_scrapers: list[dict] = []
    hf_space_urls: dict[Mode, str] = {
        "GRAPHICS": "https://huggingface.co/spaces/coJournalist/cojournalist-graphics",
        "INVESTIGATE": "https://huggingface.co/spaces/coJournalist/cojournalist-investigate",
        "FACT-CHECK": "https://huggingface.co/spaces/coJournalist/coJournalist-Fact-Check",
        "DATA": "https://huggingface.co/spaces/coJournalist/cojournalist-data",
        "SCRAPE": "",
    }

    @rx.var
    async def is_paid_user(self) -> bool:
        clerk_user = await self.get_state(clerk.ClerkUser)
        if not clerk_user.email_address:
            return False
        return clerk_user.public_metadata.get("paid", False).to(bool)

    @rx.var
    def chat_disabled(self) -> bool:
        if self.active_mode == "SCRAPE":
            return self.is_loading or self.scraped_data is None
        return self.is_loading

    @rx.var
    def modes(self) -> list[str]:
        return ["SCRAPE", "DATA", "INVESTIGATE", "FACT-CHECK", "GRAPHICS"]

    @rx.var
    def chat_history(self) -> list[Message]:
        return self.chat_histories[self.active_mode]

    @rx.var
    def show_sidebar(self) -> bool:
        return self.active_mode in ["SCRAPE", "DATA", "INVESTIGATE"]

    @rx.event
    def set_active_mode(self, mode: str):
        self.active_mode = cast(Mode, mode)
        if not self.chat_histories[self.active_mode]:
            if self.active_mode != "SCRAPE":
                self.chat_histories[self.active_mode].append(
                    {
                        "role": "assistant",
                        "content": f"Welcome to {self.active_mode} mode. Ask a question to get started.",
                        "image": None,
                        "source": "System",
                    }
                )

    @rx.event
    def set_scrape_sidebar_tab(self, tab: str):
        self.active_scrape_sidebar_tab = tab

    @rx.event
    def toggle_about_modal(self):
        self.show_about_modal = not self.show_about_modal

    @rx.event(background=True)
    async def process_chat(self, form_data: dict):
        import json

        question = form_data.get("question", "").strip()
        if not question:
            async with self:
                self.is_loading = False
            return
        async with self:
            self.is_loading = True
            self.current_question = ""
            self.chat_histories[self.active_mode].append(
                {"role": "user", "content": question, "image": None, "source": None}
            )
        try:
            prompt_filename = self.active_mode.lower().replace("-", "_")
            prompt_path = f"app/prompts/{prompt_filename}_prompt.json"
            try:
                with open(prompt_path, "r") as f:
                    prompt_data = json.load(f)
                    system_prompt = prompt_data.get(
                        "prompt", "You are a helpful assistant."
                    )
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.exception(f"Error reading prompt file: {e}")
                system_prompt = "You are a helpful assistant."
            if self.active_mode in ["DATA", "INVESTIGATE", "FACT-CHECK", "GRAPHICS"]:
                await self._query_hf_space(question, system_prompt)
            else:
                await self._dummy_response(question, system_prompt)
        except Exception as e:
            logging.exception(f"Error processing chat: {e}")
            async with self:
                self.chat_histories[self.active_mode].append(
                    {
                        "role": "assistant",
                        "content": f"An error occurred: {str(e)}",
                        "image": None,
                        "source": "Error",
                    }
                )
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    async def handle_scrape(self):
        from app.states.supabase_state import SupabaseState

        return SupabaseState.handle_scrape

    async def _dummy_response(self, question: str, system_prompt: str):
        from langchain_huggingface import HuggingFaceEndpoint
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain

        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            max_new_tokens=128,
            temperature=0.7,
            huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_KEY"),
        )
        template = f"{system_prompt}\n\nUser question: '{{question}}'"
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        try:
            response = await llm_chain.ainvoke(question)
            response_content = response["text"]
        except Exception as e:
            logging.exception(f"Error calling Hugging Face: {e}")
            response_content = "Sorry, I couldn't process your request at the moment."
        async with self:
            self.chat_histories[self.active_mode].append(
                {
                    "role": "assistant",
                    "content": response_content,
                    "image": None,
                    "source": None,
                }
            )

    async def _query_hf_space(self, question: str, system_prompt: str):
        from gradio_client import Client
        import json

        space_url = self.hf_space_urls.get(self.active_mode)
        if not space_url or not space_url.startswith("https://huggingface.co/spaces/"):
            async with self:
                self.chat_histories[self.active_mode].append(
                    {
                        "role": "assistant",
                        "content": "This mode does not have a valid Hugging Face Space configured.",
                        "image": None,
                        "source": "System Error",
                    }
                )
            return
        space_id = space_url.replace("https://huggingface.co/spaces/", "")
        try:
            client = Client(space_id, hf_token=os.environ.get("HUGGINGFACE_API_KEY"))
            result = client.predict(
                question=question, system_prompt=system_prompt, api_name="/chat"
            )
            if isinstance(result, str):
                response_data = json.loads(result)
            else:
                response_data = result
            content = response_data.get("generated_text", "No response text found.")
            image = response_data.get("image_url")
            source = response_data.get("source_url")
            async with self:
                self.chat_histories[self.active_mode].append(
                    {
                        "role": "assistant",
                        "content": content,
                        "image": image,
                        "source": source,
                    }
                )
        except Exception as e:
            logging.exception(f"Error querying HF Space with gradio_client: {e}")
            async with self:
                self.chat_histories[self.active_mode].append(
                    {
                        "role": "assistant",
                        "content": f"The Hugging Face space for this mode is currently unavailable. This might be due to setup or maintenance. Please try again later.",
                        "image": None,
                        "source": "API Error",
                    }
                )