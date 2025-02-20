import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd


def get_user_widget_statistics() -> None:
    """
    Функция для отображения статистики по пользователю в виде виджета.

    Возвращает:
        None
    """
    st.subheader("Статистика пользователя")

    if "markup_search_stats" not in st.session_state:
        st.session_state.markup_search_stats = 0

    if "markup_matching_stats" not in st.session_state:
        st.session_state.markup_matching_stats = 0

    search_markup_count = st.session_state.markup_search_stats
    matching_markup_count = st.session_state.markup_matching_stats

    st.write(f"* Разметок по поиску: {search_markup_count}")
    st.write(f"* Разметок по матчингу: {matching_markup_count}")

    st.write(f"* Всего разметок: {search_markup_count + matching_markup_count}")

def display_image_with_scroll_search(image_url: str) -> None:
    """
    Отображает изображение с прокруткой в Streamlit.

    Функция отображает изображение в ограниченной области с возможностью прокрутки,
    что позволяет удобно просматривать изображения большого размера.

    Параметры:
        image_url (str): URL изображения для отображения.

    Возвращает:
        None
    """
    st.markdown(
        f"""
        <div style="overflow:auto; max-height:400px; border:1px solid #ccc;">
            <img src="{image_url}" style="width: 100%; height: auto;" />
        </div>
        """,
        unsafe_allow_html=True
    )

def display_image_with_scroll_matching(image_url: str) -> None:
    """
    Отображает изображение с прокруткой в Streamlit для разметки матчинга.

    Функция отображает изображение в ограниченной области с возможностью прокрутки,
    что позволяет удобно просматривать изображения большого размера при разметке матчинга.

    Параметры:
        image_url (str): URL изображения для отображения.

    Возвращает:
        None
    """
    st.markdown(
        f"""
        <div style="overflow:auto; max-height:300px; border:1px solid #ccc;">
            <img src="{image_url}" style="width: 100%; height: auto;" />
        </div>
        """,
        unsafe_allow_html=True
    )

def search_markup_task() -> None:
    """
    Обработка задания по разметке поиска.

    Задания поиска загружаются из файла и выполняются до перезагрузки страницы. После чего они выполняются снова.

    Возвращает:
        None
    """
    all_items = pd.read_csv('files/Разметка поиска.csv')
    items = [row for row in all_items.iterrows()]

    if len(all_items) - st.session_state.markup_search_stats == 0:
        st.warning('Все данные для разметки поиска завершены. Чтобы повторить цикл, перезагрузите страницу.')
        return

    item = items[st.session_state.markup_search_stats][1]

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("### Варианты ответа:")
        option = st.radio(
            "Как точно этот товар соответствует запросу?",
            ["Точно", "Частично", "Невозможно оценить", "Бесполезно"],
            key="option",
        )

        state_option = st.checkbox("Товар б/у", key="used")
        counterfeit_option = st.checkbox("Контрафакт", key="counterfeit")
        mistake_option = st.checkbox("Ошибка в карточке", key="mistake")

        st.write(f"Осталось неразмеченных данных: {len(all_items) - st.session_state.markup_search_stats}")

        if (
            "check_and_save" in st.session_state
            and st.session_state.check_and_save == True
        ):
            st.session_state.running = True
        else:
            st.session_state.running = False

        if st.button(
            "Сохранить", disabled=st.session_state.running, key="check_and_save"
        ):
            st.session_state.markup_search_stats += 1
            st.experimental_rerun()

    with col2:
        st.markdown(f"**Запрос:** {item.query}")
        st.markdown(f"**Название:** {item.title}")
        st.text_area("**Описание**", item.description, height=100)
        display_image_with_scroll_search(item.url_photo)
        link_html_code = """<div style="text-align: center"><a href="%s">Ссылка на товар</a></div>"""
        st.markdown(link_html_code % item.url, unsafe_allow_html=True)

def matching_markup_task() -> None:
    """
    Обработка задания по разметке матчинга.

    Задания матчинга загружаются из файла и выполняются до перезагрузки страницы. После чего они выполняются снова.

    Возвращает:
        None
    """
    all_items = pd.read_csv('files/Разметка матчинга.csv')
    items = [row for row in all_items.iterrows()]

    if len(all_items) - st.session_state.markup_matching_stats == 0:
        st.warning('Все данные для разметки матчинга завершены. Чтобы повторить цикл, перезагрузите страницу.')
        return

    item = items[st.session_state.markup_matching_stats][1]

    col1, col2, col3 = st.columns([3, 3, 3])

    with col1:
        option = st.radio(
            "Как точно эти два товара совпадают?",
            ["Совпадает", "Не совпадает", "Частично"],
            key="match_option",
        )

        used_option = st.checkbox("Товар б/у", key="used")
        counterfeit_option = st.checkbox("Контрафакт", key="counterfeit")
        mistake_option = st.checkbox("Ошибка в карточке", key="mistake")
        insufficient_option = st.checkbox("Недостаточно данных", key="insufficient")

        st.write(f"Осталось неразмеченных данных: {len(all_items) - st.session_state.markup_matching_stats}")

        if (
            "check_and_save" in st.session_state
            and st.session_state.check_and_save == True
        ):
            st.session_state.running = True
        else:
            st.session_state.running = False

        if st.button(
            "Сохранить", disabled=st.session_state.running, key="check_and_save"
        ):

            st.experimental_rerun()

    with col2:
        #st.markdown("### Товар 1:")
        st.text_area("Наименование товара 1", item.title1, height=100)
        st.text_area("Описание товара 1", item.description1, height=150)
        display_image_with_scroll_matching(item.url_photo1)

        link_html_code = """<div style="text-align: center"><a href="%s">Ссылка на товар 1</a></div>"""
        st.markdown(link_html_code % item.url1, unsafe_allow_html=True)

    with col3:
        st.text_area("Наименование товара 2", item.title2, height=100)
        st.text_area("Описание товара 2", item.description2, height=150)
        display_image_with_scroll_matching(item.url_photo2)

        link_html_code = """<div style="text-align: center"><a href="%s">Ссылка на товар 2</a></div>"""
        st.markdown(link_html_code % item.url2, unsafe_allow_html=True)

def main():
    """
    Главная функция для управления интерфейсами пользователя.

    Функция запускает демонстрационную версию поля пользователя-разметчика двух типов данных.
    Возвращает:
        None
    """
    with st.sidebar:
        st.markdown(f'Демонстрационный вариант сервиса разметки данных')
        get_user_widget_statistics()
        task_selected = option_menu(
            "Разметка",
            ["Разметка поиска", "Разметка матчинга"],
            icons=["search", "link", "logout"],
        )

    if task_selected == "Разметка поиска":
        search_markup_task()
    else:
        matching_markup_task()


if __name__ == "__main__":
    main()
