import pandas as pd
import streamlit as st
from PyMultiDictionary import MultiDictionary


@st.cache_resource(show_spinner="Wörter werden geladen...")
def load_data():
    """
    Load the substantives data from a CSV file.
    """
    words = pd.read_csv("nouns.csv", dtype=str)
    substantives = words.loc[words["pos"] == "Substantiv", "lemma"]
    return substantives


def get_random_words(words: pd.Series, n: int) -> list:
    """
    Returns a list of n random words from the substantives Series.
    """
    return words.sample(n).tolist()


def get_word_definition(word, dictionary):
    """
    Returns the definition of the given word using the MultiDictionary API.
    """
    dictionary = MultiDictionary()
    definition = dictionary.meaning("de", word)[1]  # type: ignore
    if len(definition) == 0:
        return "Keine Definition gefunden."
    else:
        return definition.split(". ")[1]  # type: ignore


def main():
    st.set_page_config(page_title="Freestyle-Wortgenerator", page_icon=":book:")
    st.title("Wortgenerator")
    st.write("Generiere eine zufällige Wortliste z.B. zum Üben von Freestyle-Raps!")

    # Load the substantives data
    if "substantives" not in st.session_state:
        st.session_state["substantives"] = load_data()

    # Load dictionary
    if "dictionary" not in st.session_state:
        st.session_state["dictionary"] = MultiDictionary()

    # Get the number of words to quiz on from the user
    with st.form("word_form"):
        num_words = st.number_input(
            "Wieviele Wörter sollen generiert werden?",
            min_value=1,
            max_value=25,
            value=5,
        )
        submit_button = st.form_submit_button(label="Generiere Wörter")

    if not submit_button:
        st.info("Bitte klicke auf 'Generiere Wörter', um die Wörter zu generieren.")
        st.stop()

    # Get random words for the quiz
    random_words = get_random_words(st.session_state["substantives"], num_words)

    # Display the words to the user
    st.write("Das sind deine Wörter:")
    st.info("Bewege deinen Mauszeiger über die Wörter, um die Bedeutung zu sehen.")
    for word in random_words:
        meaning = get_word_definition(word, st.session_state["dictionary"])
        st.markdown(
            f"""
            <span title="{meaning}">{word}</span>
            """,
            unsafe_allow_html=True,
        )

    # Testarea


if __name__ == "__main__":
    main()
