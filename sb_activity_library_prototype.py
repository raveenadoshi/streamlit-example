import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
)


st.set_page_config(page_title="Six Bricks Activity Library", page_icon="Six Bricks Square.png", layout="centered", initial_sidebar_state="expanded", menu_items=None)
# DATAFRAME START
# Define columns to exclude from being filtered on
excluded_columns = ["Link to activity", "Activity name"]

# Function to add a nested filtering UI on top of the dataframe
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    
    with st.sidebar:

        # HEADER START

        # Display header and information
        st.image('Six Bricks Banner.png')
        st.header("Six Bricks Activity Library")

        st.write("Welcome to the Six Bricks Activity Library! Use the filters on below to find Six Bricks activities that align with the developmental areas or subjects you're interested in.")
        # HEADER END
    
        df = df.copy()
        
        with st.container():
            to_filter_columns = st.multiselect("Select your filters:", [col for col in df.columns if col not in excluded_columns], default=("Subject areas", "Key skill areas"))
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

df = pd.read_csv("activity_table.csv")
df_filtered = filter_dataframe(df)

st.dataframe(
    df_filtered,
    column_config={
        "Link to activity": st.column_config.LinkColumn("Link to activity",display_text="Click here")
    },
    hide_index=True,
)

# DATAFRAME END

"---"

st.subheader("About Six Bricks")
st.write("Six Bricks is a play-based learning methodology developed by [Care for Education](https://www.carefored.co.za) and powered by the [LEGO Foundation](https://learningthroughplay.com/). The Six Bricks concept involves implementation of manipulatives (6 colorful LEGO DUPLO bricks) to develop key executive functions and build numerous development areas for children. To learn more about Six Bricks, visit https://www.carefored.co.za.")

"---"

st.caption("This open-source web application has been developed by [Leap Education](mailto:learn.play.leap@gmail.com) & [Six Bricks Australia](https://www.sixbricksaustralia.au/). Check out our Github repository [here](https://github.com/raveenadoshi/streamlit-example/tree/master).")
st.caption("LEGO® and DUPLO® are registered trademarks of the LEGO® Group. © 2024 The LEGO® Group.")