import reflex as rx
import reflex_clerk_api as clerk
from app.state import AppState, ScrapeResult
from typing import cast
import os
import logging
import supabase
import requests
import json


class SupabaseState(rx.State):
    _client: supabase.Client | None = None

    def _get_client(self) -> supabase.Client:
        if self._client is None:
            self._client = supabase.create_client(
                os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"]
            )
        return self._client

    @rx.event
    async def create_user_on_login(self):
        clerk_user_state = await self.get_state(clerk.ClerkUser)
        if not clerk_user_state.is_loaded or not clerk_user_state.user_id:
            return
        client = self._get_client()
        try:
            user_data = (
                client.table("users")
                .select("id")
                .eq("clerk_id", clerk_user_state.user_id)
                .execute()
            )
            if not user_data.data:
                client.table("users").insert(
                    {
                        "clerk_id": clerk_user_state.user_id,
                        "email": clerk_user_state.email_address,
                    }
                ).execute()
        except Exception as e:
            logging.exception(f"Error creating user in Supabase: {e}")

    @rx.event(background=True)
    async def handle_scrape(self):
        async with self:
            app_state = await self.get_state(AppState)
            if not app_state.scrape_url:
                return
            app_state.is_loading = True
            app_state.scraped_data = None
            app_state.chat_histories[app_state.active_mode] = []
            clerk_user_state = await self.get_state(clerk.ClerkUser)
            client = self._get_client()
            user_id = None
            try:
                user_data = (
                    client.table("users")
                    .select("id")
                    .eq("clerk_id", clerk_user_state.user_id)
                    .single()
                    .execute()
                )
                user_id = user_data.data.get("id")
            except Exception as e:
                logging.exception(f"Error fetching user from Supabase: {e}")
        if user_id and app_state.scrape_schedule:
            try:
                client.table("scheduled_scrapers").insert(
                    {
                        "user_id": user_id,
                        "url": app_state.scrape_url,
                        "schedule": app_state.scrape_schedule,
                        "criteria": app_state.scrape_criteria,
                        "monitoring": app_state.scrape_monitoring,
                    }
                ).execute()
            except Exception as e:
                logging.exception(f"Error inserting scheduled scraper: {e}")
        payload = {
            "url": app_state.scrape_url,
            "schedule": app_state.scrape_schedule,
            "criteria": app_state.scrape_criteria,
            "monitoring": app_state.scrape_monitoring,
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
                "url": app_state.scrape_url,
                "error": None,
            }
            async with app_state:
                app_state.scraped_data = cast(ScrapeResult, scraped_data)
                app_state.chat_histories["SCRAPE"].append(
                    {
                        "role": "assistant",
                        "content": app_state.scraped_data["title"],
                        "image": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                        "source": app_state.scraped_data["url"],
                    }
                )
                app_state.chat_histories["SCRAPE"].append(
                    {
                        "role": "assistant",
                        "content": "Scrape successful. Please review the result. You can now use the chat to proceed.",
                        "image": None,
                        "source": None,
                    }
                )
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error calling N8N webhook: {e}")
            async with app_state:
                app_state.chat_histories["SCRAPE"].append(
                    {
                        "role": "assistant",
                        "content": f"Failed to trigger scrape workflow. Error: {str(e)}",
                        "image": None,
                        "source": "System Error",
                    }
                )
        finally:
            async with app_state:
                app_state.is_loading = False