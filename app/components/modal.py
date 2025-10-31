import reflex as rx
from app.state import AppState


def about_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "About coJournalist",
                    class_name="text-2xl font-bold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "coJournalist is an AI-powered assistant designed to streamline your journalistic workflow. It offers specialized modes for scraping web content, analyzing data, conducting investigations, fact-checking information, and generating graphics.",
                        class_name="text-gray-600 mb-4",
                    ),
                    rx.el.p(
                        "This tool integrates with external services like Hugging Face Spaces and N8N to provide powerful, context-aware capabilities. Select a mode to get started and let coJournalist help you uncover your next big story.",
                        class_name="text-gray-600 mb-4",
                    ),
                    rx.el.h3(
                        "Modes:", class_name="font-semibold text-gray-700 mt-6 mb-2"
                    ),
                    rx.el.ul(
                        rx.el.li(
                            rx.el.strong("SCRAPE:"),
                            " Plan and execute web scraping tasks.",
                        ),
                        rx.el.li(
                            rx.el.strong("DATA:"),
                            " Analyze datasets and extract insights.",
                        ),
                        rx.el.li(
                            rx.el.strong("INVESTIGATE:"),
                            " Deep dive into topics with research assistance.",
                        ),
                        rx.el.li(
                            rx.el.strong("FACT-CHECK:"),
                            " Verify claims and check sources.",
                        ),
                        rx.el.li(
                            rx.el.strong("GRAPHICS:"),
                            " Generate visual content for your stories.",
                        ),
                        class_name="list-disc list-inside text-gray-600 space-y-1",
                    ),
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Close",
                            on_click=AppState.toggle_about_modal,
                            class_name="mt-6 px-4 py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 transition",
                        )
                    ),
                    class_name="flex justify-end pt-4",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-8 w-full max-w-lg z-50",
            ),
        ),
        open=AppState.show_about_modal,
    )