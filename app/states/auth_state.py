import reflex as rx
import os
import logging
from supabase import Client, create_client
from typing import Optional


class AuthState(rx.State):
    """Manages Supabase authentication state"""

    user_id: Optional[str] = None
    email: Optional[str] = None
    is_authenticated: bool = False
    is_paid: bool = False

    def _get_supabase_client(self) -> Client:
        """Get Supabase client instance"""
        return create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_KEY"]
        )

    @rx.var
    def is_logged_in(self) -> bool:
        """Check if user is authenticated"""
        return self.is_authenticated and self.user_id is not None

    @rx.event
    async def check_auth(self):
        """Check authentication status and load user data"""
        # For now, just check if we have user_id in state
        if self.user_id and self.is_authenticated:
            await self._ensure_user_exists()
        logging.info(f"Auth check: authenticated={self.is_authenticated}, user_id={self.user_id}")

    @rx.event
    async def handle_auth_submit(self, form_data: dict):
        """Handle email/password sign in or sign up"""
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()

        if not email or not password:
            logging.error("Email or password missing")
            return

        client = self._get_supabase_client()

        try:
            # Try to sign in first
            try:
                response = client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                if response.user:
                    self.user_id = response.user.id
                    self.email = response.user.email
                    self.is_authenticated = True

                    # Ensure user record exists in database
                    await self._ensure_user_exists()

                    logging.info(f"User signed in: {self.user_id}")
                    return
            except Exception as sign_in_error:
                # Sign in failed, try to sign up
                logging.info(f"Sign in failed, trying sign up: {sign_in_error}")

                response = client.auth.sign_up({
                    "email": email,
                    "password": password
                })

                if response.user:
                    self.user_id = response.user.id
                    self.email = response.user.email
                    self.is_authenticated = True

                    # Create user record in database
                    await self._ensure_user_exists()

                    logging.info(f"User signed up: {self.user_id}")
                    return

        except Exception as e:
            logging.exception(f"Error in auth: {e}")

    async def _ensure_user_exists(self):
        """Create user record in database if it doesn't exist"""
        if not self.user_id or not self.email:
            return

        try:
            # Use admin client to create user record
            admin_client = create_client(
                os.environ["SUPABASE_URL"],
                os.environ["SUPABASE_SERVICE_ROLE_KEY"]
            )

            # Check if user exists
            result = (
                admin_client.table("users")
                .select("*")
                .eq("auth_user_id", self.user_id)
                .maybe_single()
                .execute()
            )

            if result and result.data:
                # User exists, load their data
                self.is_paid = result.data.get("is_paid", False)
                logging.info(f"User exists with id: {result.data.get('id')}")
            else:
                # Create new user record
                insert_result = admin_client.table("users").insert({
                    "auth_user_id": self.user_id,
                    "email": self.email,
                    "is_paid": False
                }).execute()

                if insert_result and insert_result.data:
                    logging.info(f"Created new user record for {self.user_id}")
                    self.is_paid = False
        except Exception as e:
            logging.exception(f"Error ensuring user exists: {e}")

    @rx.event
    async def sign_out(self):
        """Sign out user"""
        try:
            client = self._get_supabase_client()
            client.auth.sign_out()
            logging.info("User signed out")
        except Exception as e:
            logging.exception(f"Error signing out: {e}")
        finally:
            self.user_id = None
            self.email = None
            self.is_authenticated = False
            self.is_paid = False
            return rx.redirect("/")
