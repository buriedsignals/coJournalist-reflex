import reflex as rx
from app.state import AppState
from app.components.mode_sidebars import (
    data_sidebar_content,
    investigate_sidebar_content,
)


def _scraper_setup_tab() -> rx.Component:
    """Scraper Setup tab button"""
    is_active = AppState.active_scrape_sidebar_tab == "Scraper Setup"
    return rx.el.button(
        "Scraper Setup",
        on_click=AppState.switch_to_scraper_setup,
        type="button",
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-indigo-600 border-b-2 border-indigo-600 cursor-pointer",
            "px-4 py-2 text-sm font-semibold text-gray-500 hover:text-gray-700 cursor-pointer transition-colors",
        ),
    )


def _active_jobs_tab() -> rx.Component:
    """Active Jobs tab button"""
    is_active = AppState.active_scrape_sidebar_tab == "Active Jobs"
    return rx.el.button(
        "Active Jobs",
        on_click=AppState.switch_to_active_jobs,
        type="button",
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-indigo-600 border-b-2 border-indigo-600 cursor-pointer",
            "px-4 py-2 text-sm font-semibold text-gray-500 hover:text-gray-700 cursor-pointer transition-colors",
        ),
    )


def _notifications_tab() -> rx.Component:
    """Notifications tab button"""
    is_active = AppState.active_scrape_sidebar_tab == "Notifications"
    return rx.el.button(
        "Notifications",
        on_click=AppState.switch_to_notifications,
        type="button",
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-indigo-600 border-b-2 border-indigo-600 cursor-pointer",
            "px-4 py-2 text-sm font-semibold text-gray-500 hover:text-gray-700 cursor-pointer transition-colors",
        ),
    )


def _scraper_setup() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Plan scraper", class_name="text-2xl font-bold text-gray-800 mb-8"),

        # URL field
        rx.el.div(
            rx.el.label("URL", class_name="block text-sm font-semibold text-gray-600 mb-2"),
            rx.el.input(
                placeholder="https://example.com",
                default_value=AppState.scrape_url,
                on_change=AppState.set_scrape_url,
                class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md focus:bg-white focus:ring-2 focus:ring-indigo-500",
            ),
            class_name="mb-6",
        ),

        # Criteria field
        rx.el.div(
            rx.el.label("CRITERIA", class_name="block text-sm font-semibold text-gray-600 mb-2"),
            rx.el.textarea(
                placeholder="What are you looking for? e.g., Monitor for specific keywords or changes",
                default_value=AppState.scrape_criteria,
                on_change=AppState.set_scrape_criteria,
                class_name="w-full px-4 py-2 h-24 bg-gray-100 border border-gray-200 rounded-md resize-none focus:bg-white focus:ring-2 focus:ring-indigo-500",
            ),
            class_name="mb-6",
        ),

        # Regularity selector
        rx.el.div(
            rx.el.label("REGULARITY", class_name="block text-sm font-semibold text-gray-600 mb-2"),
            rx.el.select(
                rx.el.option("Weekly", value="weekly"),
                rx.el.option("Monthly", value="monthly"),
                default_value=AppState.scrape_regularity,
                on_change=AppState.set_scrape_regularity,
                class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md appearance-none focus:bg-white focus:ring-2 focus:ring-indigo-500",
            ),
            class_name="mb-6",
        ),

        # Day selector (conditional based on regularity)
        rx.cond(
            AppState.scrape_regularity == "weekly",
            # Weekly: Days of week dropdown
            rx.el.div(
                rx.el.label("DAY OF WEEK", class_name="block text-sm font-semibold text-gray-600 mb-2"),
                rx.el.select(
                    rx.el.option("Monday", value="1"),
                    rx.el.option("Tuesday", value="2"),
                    rx.el.option("Wednesday", value="3"),
                    rx.el.option("Thursday", value="4"),
                    rx.el.option("Friday", value="5"),
                    rx.el.option("Saturday", value="6"),
                    rx.el.option("Sunday", value="7"),
                    value=AppState.scrape_day_number,
                    on_change=AppState.set_scrape_day_number,
                    class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md appearance-none focus:bg-white focus:ring-2 focus:ring-indigo-500",
                ),
                class_name="mb-6",
            ),
            # Monthly: Day of month dropdown
            rx.el.div(
                rx.el.label("DAY OF MONTH", class_name="block text-sm font-semibold text-gray-600 mb-2"),
                rx.el.select(
                    *[rx.el.option(str(i), value=str(i)) for i in range(1, 31)],
                    value=AppState.scrape_day_number,
                    on_change=AppState.set_scrape_day_number,
                    class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md appearance-none focus:bg-white focus:ring-2 focus:ring-indigo-500",
                ),
                class_name="mb-6",
            ),
        ),

        # Time field
        rx.el.div(
            rx.el.label("TIME (UTC)", class_name="block text-sm font-semibold text-gray-600 mb-2"),
            rx.el.input(
                type="time",
                placeholder="12:00",
                default_value=AppState.scrape_time,
                on_change=AppState.set_scrape_time,
                class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md focus:bg-white focus:ring-2 focus:ring-indigo-500",
            ),
            class_name="mb-6",
        ),

        # Monitoring toggle
        rx.el.div(
            rx.el.label("MONITORING", class_name="block text-sm font-semibold text-gray-600 mb-2"),
            rx.el.select(
                rx.el.option("Email", value="EMAIL"),
                rx.el.option("SMS", value="SMS"),
                rx.el.option("Webhook", value="WEBHOOK"),
                default_value=AppState.scrape_monitoring,
                on_change=AppState.set_scrape_monitoring,
                class_name="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-md appearance-none focus:bg-white focus:ring-2 focus:ring-indigo-500",
            ),
            class_name="mb-6",
        ),

        # Submit button
        rx.el.button(
            "Create Scraper",
            on_click=AppState.handle_scrape,
            class_name="w-full py-2.5 bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700 disabled:opacity-50 transition-colors",
            disabled=AppState.is_loading,
        ),

        class_name="p-8",
    )


def _scraper_card(scraper) -> rx.Component:
    """Individual scraper card component with delete functionality"""
    from app.states.supabase_state import SupabaseState

    return rx.el.div(
        # Scraper info
        rx.el.div(
            rx.el.p(
                scraper["name"],
                class_name="font-semibold text-gray-800 truncate",
            ),
            rx.cond(
                scraper["criteria"],
                rx.el.p(
                    f"Criteria: {scraper['criteria']}",
                    class_name="text-sm text-gray-500 truncate",
                ),
                rx.el.p(
                    "No criteria specified",
                    class_name="text-sm text-gray-400 italic truncate",
                ),
            ),
            rx.el.p(
                f"{scraper['regularity']} at {scraper['time_utc']}",
                class_name="text-xs text-gray-400 mt-1",
            ),
            class_name="flex-1 overflow-hidden",
        ),
        # Delete button
        rx.el.button(
            rx.icon("trash-2", class_name="h-4 w-4 text-red-500"),
            on_click=lambda: SupabaseState.delete_scraper(scraper["id"]),
            class_name="p-2 hover:bg-red-50 rounded-md cursor-pointer transition-colors",
        ),
        class_name="flex items-center gap-4 p-4 border border-gray-200 rounded-lg bg-white hover:shadow-sm transition-shadow",
    )


def _active_jobs() -> rx.Component:
    """Active Jobs tab with loading state and scraper list"""
    from app.states.supabase_state import SupabaseState

    return rx.el.div(
        # Header with refresh button
        rx.el.div(
            rx.el.h2("Active Jobs", class_name="text-2xl font-bold text-gray-800"),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-4 w-4"),
                on_click=SupabaseState.fetch_scrapers,
                class_name="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md cursor-pointer transition-colors",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        # Content with loading state
        rx.cond(
            AppState.scrapers_loading,
            # Loading state
            rx.el.div(
                rx.spinner(size="3"),
                rx.el.p("Loading scrapers...", class_name="text-gray-500 ml-3"),
                class_name="flex items-center justify-center py-12"
            ),
            # Content when not loading
            rx.cond(
                AppState.scheduled_scrapers,
                # List of scrapers
                rx.el.div(
                    rx.foreach(
                        AppState.scheduled_scrapers,
                        _scraper_card,
                    ),
                    class_name="space-y-4",
                ),
                # Empty state
                rx.el.div(
                    rx.el.p("No active jobs.", class_name="text-gray-500 text-center"),
                    rx.el.p("Create a scraper to get started.", class_name="text-sm text-gray-400 text-center mt-2"),
                    class_name="py-12",
                ),
            )
        ),
        class_name="p-8",
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
            _scraper_setup_tab(),
            _active_jobs_tab(),
            _notifications_tab(),
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