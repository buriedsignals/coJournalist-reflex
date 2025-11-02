import reflex as rx
import os
from app.components.sidebar import sidebar
from app.components.chat import chat_interface
from app.state import AppState
from app.states.auth_state import AuthState


def protected_page() -> rx.Component:
    return rx.el.div(
        rx.cond(AppState.show_sidebar, sidebar(), None),
        rx.el.main(chat_interface(), class_name="flex-1 h-screen overflow-hidden"),
        class_name="flex w-full min-h-screen bg-white font-['Inter']",
    )


def auth_page() -> rx.Component:
    """Email/password authentication page"""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1("co", class_name="text-5xl font-bold text-indigo-600"),
                rx.el.h1("Journalist", class_name="text-5xl font-bold text-gray-800"),
                class_name="flex items-baseline gap-2 mb-4",
            ),
            rx.el.p(
                "Your AI-Powered Journalism Assistant",
                class_name="text-lg text-gray-600 mb-8",
            ),

            # Sign in/up form
            rx.form(
                rx.el.div(
                    rx.el.label("Email", class_name="block text-sm font-semibold text-gray-700 mb-2"),
                    rx.el.input(
                        type="email",
                        name="email",
                        placeholder="you@example.com",
                        required=True,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Password", class_name="block text-sm font-semibold text-gray-700 mb-2"),
                    rx.el.input(
                        type="password",
                        name="password",
                        placeholder="••••••••",
                        required=True,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Sign In / Sign Up",
                    type="submit",
                    class_name="w-full px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition",
                ),
                on_submit=AuthState.handle_auth_submit,
                class_name="w-full max-w-md p-8 bg-white rounded-lg shadow-lg",
            ),
            class_name="flex flex-col items-center",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 text-center",
    )


def index() -> rx.Component:
    return rx.cond(
        AuthState.is_logged_in,
        # Authenticated view
        rx.el.div(
            rx.el.header(
                rx.el.button(
                    "Sign Out",
                    on_click=AuthState.sign_out,
                    class_name="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md",
                    style={"pointer-events": "auto"},
                ),
                class_name="absolute top-0 right-0 p-6 z-10",
                style={"pointer-events": "none"},
            ),
            protected_page(),
        ),
        # Unauthenticated view
        auth_page(),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)

# Add main page
app.add_page(index, route="/", on_load=AuthState.check_auth)