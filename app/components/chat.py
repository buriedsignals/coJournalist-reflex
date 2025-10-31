import reflex as rx
from app.state import AppState, Message
from app.components.modal import about_modal


def mode_button(mode: str) -> rx.Component:
    return rx.el.button(
        mode,
        on_click=lambda: AppState.set_active_mode(mode),
        class_name=rx.cond(
            AppState.active_mode == mode,
            "px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-md shadow-md",
            "px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
        ),
    )


def chat_message(message: Message) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.cond(
                message["image"],
                rx.el.div(
                    rx.image(
                        src=message["image"],
                        class_name="w-24 h-16 object-cover rounded-md",
                    ),
                    rx.el.div(
                        rx.el.p(
                            message.get("source", "SOURCE"),
                            class_name="text-xs font-bold uppercase text-gray-500",
                        ),
                        rx.el.p(
                            message["content"],
                            class_name="text-md text-gray-800 font-semibold",
                        ),
                        class_name="ml-4",
                    ),
                    class_name="flex items-center p-4 bg-gray-100 rounded-lg w-full max-w-lg",
                ),
                rx.el.p(message["content"], class_name="text-md text-gray-800"),
            ),
            class_name=rx.cond(is_user, "p-4 rounded-lg bg-gray-100", "p-4"),
        ),
        class_name=rx.cond(is_user, "flex justify-end", "flex justify-start"),
    )


def chat_interface() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("co", class_name="text-4xl font-bold text-indigo-600"),
                    rx.el.h1(
                        "Journalist", class_name="text-4xl font-bold text-gray-800"
                    ),
                    class_name="flex items-baseline gap-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(rx.foreach(AppState.modes, mode_button), class_name="flex gap-2"),
            rx.el.div(
                rx.el.a(
                    rx.icon("share", class_name="w-4 h-4 mr-2"),
                    "Open Space",
                    href=AppState.hf_space_urls[AppState.active_mode],
                    target="_blank",
                    class_name="flex items-center px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
                ),
                class_name=rx.cond(
                    AppState.active_mode != "SCRAPE", "absolute right-6 top-6", "hidden"
                ),
            ),
            class_name="relative flex flex-col items-center justify-center text-center gap-8 py-12",
        ),
        rx.el.div(
            rx.foreach(AppState.chat_history, chat_message),
            class_name="flex-grow p-4 space-y-4 overflow-y-auto",
        ),
        rx.el.footer(
            rx.el.form(
                rx.el.input(
                    placeholder="Ask coJournalist...",
                    name="question",
                    class_name="w-full px-4 py-3 bg-gray-100 border-transparent rounded-lg focus:bg-white focus:ring-2 focus:ring-indigo-500",
                    disabled=AppState.chat_disabled,
                    default_value=AppState.current_question,
                    key=AppState.current_question,
                ),
                rx.el.button(
                    rx.icon("send", class_name="text-white"),
                    type="submit",
                    class_name="p-3 bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300",
                    disabled=AppState.chat_disabled,
                ),
                on_submit=AppState.process_chat,
                reset_on_submit=True,
                class_name="flex items-center gap-2 p-4",
            ),
            about_modal(),
            rx.el.p(
                "ABOUT",
                class_name="text-center text-xs text-gray-400 pb-4 cursor-pointer",
                on_click=AppState.toggle_about_modal,
            ),
        ),
        class_name="flex flex-col h-full w-full",
    )