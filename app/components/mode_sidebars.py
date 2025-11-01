import reflex as rx


def data_sidebar_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Data Sources", class_name="text-2xl font-bold text-gray-800 mb-8"),
        rx.el.p(
            "This is a placeholder for available data sources. You can connect to databases, upload files, or link to external APIs.",
            class_name="text-gray-600 mb-4",
        ),
        rx.el.ul(
            rx.el.li("- Public Records Database"),
            rx.el.li("- Financial Filings API"),
            rx.el.li("- Uploaded CSVs"),
            class_name="list-none text-gray-600 space-y-1 pl-2",
        ),
        class_name="p-8",
    )


def investigate_sidebar_content() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Bellingcat Tools", class_name="text-2xl font-bold text-gray-800 mb-8"
        ),
        rx.el.p(
            "This is a placeholder for investigative tools inspired by Bellingcat's open-source intelligence (OSINT) techniques.",
            class_name="text-gray-600 mb-4",
        ),
        rx.el.ul(
            rx.el.li("- Geolocation Analysis"),
            rx.el.li("- Social Media Monitoring"),
            rx.el.li("- Ship & Flight Tracking"),
            rx.el.li("- Reverse Image Search"),
            class_name="list-none text-gray-600 space-y-1 pl-2",
        ),
        class_name="p-8",
    )