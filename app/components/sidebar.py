import reflex as rx
from app.state import AppState


def scrape_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.h2(
                "Plan scraper", class_name="text-2xl font-bold text-gray-800 mb-8"
            ),
            rx.el.div(
                rx.el.label(
                    "URL", class_name="text-sm font-semibold text-gray-600 mb-2"
                ),
                rx.el.input(
                    placeholder="https://example.com",
                    default_value=AppState.scrape_url,
                    on_change=AppState.set_scrape_url,
                    class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md focus:bg-white focus:ring-2 focus:ring-indigo-500",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Scrape URL",
                on_click=AppState.handle_scrape,
                class_name="w-full py-2.5 bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700 disabled:opacity-50",
                disabled=AppState.is_loading,
            ),
            rx.el.div(class_name="my-8 border-t border-gray-200"),
            rx.el.div(
                rx.el.label(
                    "SCHEDULE", class_name="text-sm font-semibold text-gray-600 mb-2"
                ),
                rx.el.input(
                    placeholder="e.g., Every 24 hours",
                    default_value=AppState.scrape_schedule,
                    on_change=AppState.set_scrape_schedule,
                    class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md focus:bg-white focus:ring-2 focus:ring-indigo-500",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "CRITERIA", class_name="text-sm font-semibold text-gray-600 mb-2"
                ),
                rx.el.textarea(
                    placeholder="Is the mayor meeting with any of these individuals? Johnny, Max, Lucas.",
                    default_value=AppState.scrape_criteria,
                    on_change=AppState.set_scrape_criteria,
                    class_name="w-full px-4 py-2 h-32 bg-gray-100 border border-gray-200 rounded-md resize-none focus:bg-white focus:ring-2 focus:ring-indigo-500",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "MONITORING", class_name="text-sm font-semibold text-gray-600 mb-2"
                ),
                rx.el.select(
                    rx.el.option("EMAIL", value="EMAIL"),
                    rx.el.option("SMS", value="SMS"),
                    rx.el.option("WEBHOOK", value="WEBHOOK"),
                    default_value=AppState.scrape_monitoring,
                    on_change=AppState.set_scrape_monitoring,
                    class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md appearance-none focus:bg-white focus:ring-2 focus:ring-indigo-500",
                ),
                class_name="mb-6",
            ),
            class_name="p-8",
        ),
        class_name="w-96 bg-gray-50 h-screen border-r border-gray-200 transition-all duration-300 ease-in-out",
    )