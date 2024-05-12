import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
)

st.image("Six Bricks Banner.png")

st.title("Six Bricks Activity Library")

st.write("""Welcome to the Six Bricks Library Activity! Use the filters on the left-hand side of this page to find Six Bricks activities that align with the developmental areas or subjects you're interested in.
        """)

st.write("""To learn more about Six Bricks, visit [Care for Education](https://www.carefored.co.za) -- home of the Six Bricks methodology.
        """)

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    
    with st.sidebar:
    
        df = df.copy()
        
        with st.container():
            to_filter_columns = st.multiselect("Select your filters:", df.columns,("Subject areas","Key skill areas"))
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

df = pd.read_csv("penguins.csv")
df_filtered = filter_dataframe(df)

st.dataframe(
    df_filtered,
    column_config={
        "Link to activity": st.column_config.LinkColumn("Link to activity")
    },
    hide_index=True,
)