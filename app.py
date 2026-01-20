import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="TOPSIS Web Service")

st.title("TOPSIS Web Service")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

weights_input = st.text_input("Enter Weights (comma separated)", "1,1,1,1,1")
impacts_input = st.text_input("Enter Impacts (+ or - , comma separated)", "+,+,+,+,+")

def topsis_calc(df, weights, impacts):
    data = df.iloc[:, 1:]

    for c in data.columns:
        if not np.issubdtype(data[c].dtype, np.number):
            st.error("Non-numeric values found in criteria columns")
            return None

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        st.error("Number of weights or impacts does not match criteria")
        return None

    norm = data.copy()
    for c in norm.columns:
        norm[c] = norm[c] / np.sqrt((norm[c] ** 2).sum())

    for i in range(len(weights)):
        norm.iloc[:, i] *= weights[i]

    best, worst = [], []
    for i in range(len(impacts)):
        col = norm.iloc[:, i]
        if impacts[i] == "+":
            best.append(col.max())
            worst.append(col.min())
        else:
            best.append(col.min())
            worst.append(col.max())

    d_best = np.sqrt(((norm - best) ** 2).sum(axis=1))
    d_worst = np.sqrt(((norm - worst) ** 2).sum(axis=1))

    score = d_worst / (d_best + d_worst)
    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    return df

if st.button("Run TOPSIS"):

    if uploaded_file is None:
        st.error("Please upload a CSV file")
    else:
        try:
            df = pd.read_csv(uploaded_file)
            weights = list(map(float, weights_input.split(",")))
            impacts = impacts_input.split(",")

            result = topsis_calc(df, weights, impacts)

            if result is not None:
                st.success("TOPSIS calculation completed")
                st.dataframe(result)

                buffer = BytesIO()
                result.to_csv(buffer, index=False)
                buffer.seek(0)

                st.download_button(
                    label="Download Result CSV",
                    data=buffer,
                    file_name="topsis_result.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(str(e))
