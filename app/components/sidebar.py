import reflex as rx
from app.state import AppState
from app.components.mode_sidebars import (
    data_sidebar_content,
    investigate_sidebar_content,
)


def _sidebar_tab(name: str) -> rx.Component:
    return rx.el.button(
        name,
        on_click=lambda: AppState.set_scrape_sidebar_tab(name),
        class_name=rx.cond(
            AppState.active_scrape_sidebar_tab == name,
            "px-4 py-2 text-sm font-semibold text-indigo-600 border-b-2 border-indigo-600",
            "px-4 py-2 text-sm font-semibold text-gray-500 hover:text-gray-700",
        ),
    )


def _scraper_setup() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Plan scraper", class_name="text-2xl font-bold text-gray-800 mb-8"),
        rx.el.div(
            rx.el.label("URL", class_name="text-sm font-semibold text-gray-600 mb-2"),
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
    )


def _active_jobs() -> rx.Component:
    from app.states.supabase_state import SupabaseState

    return rx.el.div(
        rx.el.div(
            rx.el.h2("Active Jobs", class_name="text-2xl font-bold text-gray-800"),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-4 w-4"),
                on_click=SupabaseState.fetch_scrapers,
                class_name="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.cond(
            AppState.scheduled_scrapers,
            rx.el.div(
                rx.foreach(
                    AppState.scheduled_scrapers,
                    lambda scraper: rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                scraper["name"],
                                class_name="font-semibold text-gray-800 truncate",
                            ),
                            rx.el.p(
                                f"Criteria: {scraper['criteria']}",
                                class_name="text-sm text-gray-500 truncate",
                            ),
                            class_name="flex-1 overflow-hidden",
                        ),
                        rx.el.button(
                            rx.icon("trash-2", class_name="h-4 w-4 text-red-500"),
                            on_click=lambda: SupabaseState.delete_scraper(
                                scraper["id"]
                            ),
                            class_name="p-2 hover:bg-red-50 rounded-md",
                        ),
                        class_name="flex items-center gap-4 p-4 border border-gray-200 rounded-lg bg-white",
                    ),
                ),
                class_name="space-y-4",
            ),
            rx.el.p("No active jobs.", class_name="text-gray-500"),
        ),
        class_name="p-8",
        on_mount=SupabaseState.fetch_scrapers,
    )


def _notifications() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Notifications", class_name="text-2xl font-bold text-gray-800 mb-8"),
        rx.el.p("No new notifications.", class_name="text-gray-500"),
        class_name="p-8",
    )


def scrape_sidebar_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            _sidebar_tab("Scraper Setup"),
            _sidebar_tab("Active Jobs"),
            _sidebar_tab("Notifications"),
            class_name="flex border-b border-gray-200",
        ),
        rx.match(
            AppState.active_scrape_sidebar_tab,
            ("Scraper Setup", _scraper_setup()),
            ("Active Jobs", _active_jobs()),
            ("Notifications", _notifications()),
            _scraper_setup(),
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.match(
            AppState.active_mode,
            ("SCRAPE", scrape_sidebar_content()),
            ("DATA", data_sidebar_content()),
            ("INVESTIGATE", investigate_sidebar_content()),
            rx.el.div(),
        ),
        class_name="w-96 bg-gray-50 h-screen border-r border-gray-200 transition-all duration-300 ease-in-out",
    )