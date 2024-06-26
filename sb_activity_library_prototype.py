import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
)


st.set_page_config(page_title="Six Bricks Activity Library", page_icon="Six Bricks Stack.png", layout="centered", initial_sidebar_state="expanded", menu_items=None)

st.subheader("Six Bricks Activity Library")

with st.sidebar:
    # HEADER START
    # Display header and information
    st.image('Six Bricks Stack.png', width=200)
    st.header("Welcome to the Six Bricks Activity Library!")
    st.info("🚧 This is a prototype for a library that will house hundreds of Six Bricks activites, with the ability to quickly filter by skill area, subject area, and more. Check back towards the end of 2024 for our launch! 🚧")
    #st.subheader("Quick actions")
    #st.button("🔍 Find an activity")
    #st.button("💡 Submit an activity to the library")

    "---"

    st.subheader("About Six Bricks")
    st.write("Six Bricks is a hand-on, play-based learning methodology developed by [Care for Education](https://www.carefored.co.za) and powered by the [LEGO Foundation](https://learningthroughplay.com/). The Six Bricks concept uses a set of 6 colorful 2x4 LEGO® DUPLO® bricks to help children practice their memory, movement, creativity, problem-solving, language, and more. To learn more about Six Bricks, visit https://www.carefored.co.za.")
    st.caption("LEGO® and DUPLO® are registered trademarks of the LEGO® Group. © 2024 The LEGO® Group.")

tab1, tab2 = st.tabs(["📚 Six Bricks Activity Library", "🌱 Community Submissions"])

# DATAFRAME START
# Define columns to exclude from being filtered on
excluded_columns = ["Link to activity", "Activity name"]

with tab1:

    def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a UI on top of a dataframe to let viewers filter columns

        Args:
            df (pd.DataFrame): Original dataframe

        Returns:
            pd.DataFrame: Filtered dataframe
        """
        
        df = df.copy()
        
        with st.container():
            to_filter_columns = st.multiselect("Select the filters that you would like to use:", [col for col in df.columns if col not in excluded_columns], default=("Subject areas", "Key skill areas"))
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                # Treat columns with < 10 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Select {column}:",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]

                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                else:
                    user_text_input = right.text_input(
                        f"Type below to search by {column}:",
                    )
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]
        return df
    
    # Read activity list
    df = pd.read_csv("activity_table.csv")
    df_filtered = filter_dataframe(df)

    if st.button("🔍 Find activities",type='primary'):
        st.divider()
        st.subheader("Search results:")
        st.dataframe(
            df_filtered,
            column_config={
                "Link to activity": st.column_config.LinkColumn("Link to activity", display_text="Click here")
            },
            hide_index=True,
        )

with tab2:
    st.write("Created a Six Bricks Activity that you want to share with the global community? Follow the steps below to get your activity added to this library.")
    st.write("1. Review the library to ensure that the activity doesn't already exist.")
    st.write("2. Make a copy of the [linked template](https://www.canva.com/design/DAGGYv8tDXc/e4m3ExfR87otSz9GwN2OcQ/edit?utm_content=DAGGYv8tDXc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton), and fill it in with the details about your activity. You might notice that this template looks a little different from some of the activities in the library; this is intentional. Please use this format to help us standardize all new submissions to the library.")
    st.write("3. Submit your activity for review using the [linked form](https://forms.gle/fqpreubi3ZmnoWw86).")
    st.write("4. Stay tuned; we'll review your submission and get it added to the library. We may reach out if we have questions.")

st.caption("This open-source web application has been developed by [Leap Education](mailto:learn.play.leap@gmail.com) & [Six Bricks Australia](https://www.sixbricksaustralia.au/). Check out our Github repository [here](https://github.com/raveenadoshi/streamlit-example/tree/master).")
