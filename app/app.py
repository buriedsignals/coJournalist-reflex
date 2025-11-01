import reflex as rx
import reflex_clerk_api as clerk
import os
from app.components.sidebar import sidebar
from app.components.chat import chat_interface
from app.state import AppState


def protected_page() -> rx.Component:
    return rx.el.div(
        rx.cond(AppState.show_sidebar, sidebar(), None),
        rx.el.main(chat_interface(), class_name="flex-1 h-screen overflow-hidden"),
        class_name="flex w-full min-h-screen bg-white font-['Inter']",
    )


def index() -> rx.Component:
    return rx.el.div(
        clerk.clerk_loading(
            rx.el.div(
                rx.spinner(class_name="w-8 h-8 text-indigo-600"),
                class_name="flex items-center justify-center min-h-screen",
            )
        ),
        clerk.clerk_loaded(
            rx.el.div(
                clerk.signed_out(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h1(
                                "co", class_name="text-5xl font-bold text-indigo-600"
                            ),
                            rx.el.h1(
                                "Journalist",
                                class_name="text-5xl font-bold text-gray-800",
                            ),
                            class_name="flex items-baseline gap-2",
                        ),
                        rx.el.p(
                            "Your AI-Powered Journalism Assistant",
                            class_name="text-lg text-gray-600 mt-4 mb-8",
                        ),
                        clerk.sign_in_button(
                            class_name="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition"
                        ),
                        class_name="flex flex-col items-center justify-center h-screen bg-gray-50 text-center",
                    )
                ),
                clerk.signed_in(
                    rx.el.div(
                        rx.el.header(
                            rx.el.div(class_name="flex-1"),
                            rx.el.div(
                                clerk.user_button(
                                    after_sign_out_url="/", class_name="p-2"
                                ),
                                class_name="flex items-center gap-4 text-sm font-semibold",
                            ),
                            class_name="absolute top-0 right-0 p-6 flex items-center justify-end w-full z-10",
                        ),
                        protected_page(),
                    )
                ),
            )
        ),
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
from app.states.supabase_state import SupabaseState

app = clerk.wrap_app(
    app,
    publishable_key=os.environ.get("CLERK_PUBLISHABLE_KEY", ""),
    secret_key=os.environ.get("CLERK_SECRET_KEY", ""),
    register_user_state=True,
    after_sign_in_url="/",
    after_sign_up_url="/",
)
clerk.add_sign_in_page(app)
clerk.add_sign_up_page(app)
app.add_page(index, on_load=SupabaseState.create_user_on_login)