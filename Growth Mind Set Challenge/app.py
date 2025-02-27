import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Convertor", layout="wide")
st.title("File Convertor & cleaner")
st.write("Upload csv or excel file to delete or convert the file formates.")

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files : 
    for file in files :
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Remove")
            st.dataframe(df.head())

            if st.checkbox(f"File Missing values - {file.name}"):
                df = fillna(df.select_dtypes(include=["number"]).mean(), inplace = True)
                st.success("Missing values filled with mean")
                st.dataframe(df.head())

            selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
            df = df[selected_columns]
            st.dataframe(df.head())


            if st.checkbox(f"Show Charts - {file.name}") and not df.select_dtypes(include="number").empty:
                st.bar_chart(df.select_dtypes(include="number")).iloc[:, :2]

            format_choise = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)
            
            if st.button(f"Download {file.name} as {format_choise}"):
                output = BytesIO()
                if format_choise == "csv":
                    df.to_csv(output, index=False)
                    mine = "text/csv"
                    new_name = file.name.replace(ext, "csv")
                
                else:
                    df.to_csv(output, index=False, engine = 'openpyxl')
                    mine = "application/vnd.openxml formats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")
                    
                output.seek(0)
                st.download_button("Download File", file_name = new_name, data=output, mime=mine)

                st.success("Processing Complete!")