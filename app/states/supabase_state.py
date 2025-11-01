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
        clerk_state = await self.get_state(clerk.ClerkState)
        if not clerk_state.is_hydrated or not clerk_state.user_id:
            return
        clerk_user_state = await self.get_state(clerk.ClerkUser)
        client = self._get_client()
        try:
            user_data = (
                client.table("users")
                .select("id")
                .eq("clerk_id", clerk_state.user_id)
                .execute()
            )
            if not user_data.data:
                client.table("users").insert(
                    {
                        "clerk_id": clerk_state.user_id,
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
            clerk_state = await self.get_state(clerk.ClerkState)
            client = self._get_client()
            user_id = None
            try:
                user_data = (
                    client.table("users")
                    .select("id")
                    .eq("clerk_id", clerk_state.user_id)
                    .maybe_single()
                    .execute()
                )
                user_id = user_data.data.get("id") if user_data.data else None
            except Exception as e:
                logging.exception(f"Error fetching user from Supabase: {e}")
        if user_id:
            try:
                client.table("scheduled_scrapers").insert(
                    {
                        "user_id": user_id,
                        "name": app_state.scrape_url,
                        "criteria": app_state.scrape_criteria,
                        "regularity": "weekly",
                        "day_number": 1,
                        "monitoring": app_state.scrape_monitoring == "EMAIL",
                    }
                ).execute()
            except Exception as e:
                logging.exception(f"Error inserting scheduled scraper: {e}")
        try:
            scraped_data = {
                "success": True,
                "title": f"Scrape Planned for {app_state.scrape_url}",
                "preview": "This scrape has been saved to your active jobs. The N8N workflow was not triggered.",
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
                        "content": "Scrape job saved. You can view it in the 'Active Jobs' tab. You can now use the chat to proceed.",
                        "image": None,
                        "source": None,
                    }
                )
        except Exception as e:
            logging.exception(f"Error creating mock scrape data: {e}")
            async with app_state:
                app_state.chat_histories["SCRAPE"].append(
                    {
                        "role": "assistant",
                        "content": f"Failed to create scrape job. Error: {str(e)}",
                        "image": None,
                        "source": "System Error",
                    }
                )
        finally:
            async with app_state:
                app_state.is_loading = False

    @rx.event
    async def fetch_scrapers(self):
        app_state = await self.get_state(AppState)
        clerk_state = await self.get_state(clerk.ClerkState)
        if not clerk_state.is_hydrated or not clerk_state.user_id:
            app_state.scheduled_scrapers = []
            return
        client = self._get_client()
        try:
            user_data = (
                client.table("users")
                .select("id")
                .eq("clerk_id", clerk_state.user_id)
                .maybe_single()
                .execute()
            )
            user_id = user_data.data.get("id") if user_data.data else None
            if not user_id:
                app_state.scheduled_scrapers = []
                return
            scrapers_data = (
                client.table("scheduled_scrapers")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            app_state.scheduled_scrapers = scrapers_data.data
        except Exception as e:
            logging.exception(f"Error fetching scrapers from Supabase: {e}")
            app_state.scheduled_scrapers = []

    @rx.event(background=True)
    async def delete_scraper(self, scraper_id: int):
        async with self:
            client = self._get_client()
            try:
                client.table("scheduled_scrapers").delete().eq(
                    "id", scraper_id
                ).execute()
            except Exception as e:
                logging.exception(f"Error deleting scraper from Supabase: {e}")
        yield SupabaseState.fetch_scrapers