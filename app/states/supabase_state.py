import reflex as rx
from app.state import AppState, ScrapeResult
from typing import cast
import os
import logging
import supabase
import requests
import json


class SupabaseState(rx.State):

    def _get_client(self) -> supabase.Client:
        """Get Supabase client with anon key for user-facing operations"""
        # Create client on each call to avoid serialization issues
        return supabase.create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_KEY"]
        )

    def _get_admin_client(self) -> supabase.Client:
        """Get Supabase client with service role key for admin operations"""
        # Create client on each call to avoid serialization issues
        return supabase.create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_SERVICE_ROLE_KEY"]
        )

    async def _get_current_user_db_id(self) -> str | None:
        """Get current authenticated user's database ID"""
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.user_id:
            logging.info("No authenticated user")
            return None

        # Query users table by auth_user_id
        # Use admin client to bypass RLS policies (server-side lookup)
        client = self._get_admin_client()
        try:
            result = (
                client.table("users")
                .select("*")
                .eq("auth_user_id", auth_state.user_id)
                .maybe_single()
                .execute()
            )

            if result and result.data:
                logging.info(f"Found user database ID: {result.data.get('id')}")
                return result.data.get("id")

            logging.warning(f"No user record found for auth_user_id: {auth_state.user_id}")
            return None
        except Exception as e:
            logging.exception(f"Error getting user database ID: {e}")
            return None

    @rx.event(background=True)
    async def handle_scrape(self):
        async with self:
            app_state = await self.get_state(AppState)
            if not app_state.scrape_url:
                return
            app_state.is_loading = True
            app_state.scraped_data = None
            app_state.chat_histories[app_state.active_mode] = []

            # Get current user's database ID
            user_id = await self._get_current_user_db_id()
        if user_id:
            try:
                # Use admin client to bypass RLS for server-side insert
                client = self._get_admin_client()

                # Format time as HH:MM:SS
                time_utc = app_state.scrape_time if app_state.scrape_time else "12:00"
                if len(time_utc.split(":")) == 2:
                    time_utc = f"{time_utc}:00"

                # Ensure criteria has a value
                criteria = app_state.scrape_criteria if app_state.scrape_criteria else "Monitor for changes"

                # Convert day_number to int
                day_number = int(app_state.scrape_day_number) if app_state.scrape_day_number else 1

                client.table("scheduled_scrapers").insert(
                    {
                        "user_id": user_id,
                        "name": app_state.scrape_url,
                        "criteria": criteria,
                        "regularity": app_state.scrape_regularity,
                        "day_number": day_number,
                        "time_utc": time_utc,
                        "scraper_service": "default",
                        "prompt_summary": f"Scrape {app_state.scrape_url}",
                        "monitoring": bool(app_state.scrape_monitoring),
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
        app_state.scrapers_loading = True

        try:
            # Get current user's database ID
            user_id = await self._get_current_user_db_id()

            if not user_id:
                app_state.scheduled_scrapers = []
                return

            # Use admin client to bypass RLS for server-side fetch
            client = self._get_admin_client()
            scrapers_data = (
                client.table("scheduled_scrapers")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            app_state.scheduled_scrapers = scrapers_data.data if scrapers_data.data else []
        except Exception as e:
            logging.exception(f"Error fetching scrapers from Supabase: {e}")
            app_state.scheduled_scrapers = []
        finally:
            app_state.scrapers_loading = False

    @rx.event(background=True)
    async def delete_scraper(self, scraper_id: str):
        """Delete a scraper and refresh the list"""
        logging.info(f"Deleting scraper with id: {scraper_id}")
        try:
            # Use admin client to bypass RLS for server-side delete
            client = self._get_admin_client()
            client.table("scheduled_scrapers").delete().eq("id", scraper_id).execute()
            logging.info(f"Successfully deleted scraper: {scraper_id}")
        except Exception as e:
            logging.exception(f"Error deleting scraper from Supabase: {e}")

        # Refresh the scrapers list
        yield SupabaseState.fetch_scrapers