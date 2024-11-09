# Importing necessary libraries
import pandas as pd
import streamlit as st
from streamlit_sortables import sort_items  # This library adds drag-and-drop functionality in Streamlit
import json
import io
from colour import Color
from openpyxl import Workbook

# Load data from Excel file
def load_data(file_path):
    df = pd.read_excel(file_path, sheet_name="Sheet1", skiprows=2)  # Assuming data starts from row 4
    df = df[3:]  # Data starts from row 4
    return df

# Function to export data to Excel
def export_to_excel(df, file_name):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, sheet_name='Ranked_Rotations', index=False)
    writer.save()
    output.seek(0)
    return output

# Main Streamlit app
def main():
    st.title("Rotation Ranking Tool")
    st.write("Drag and drop to rank the rotations as per your preference.")

    # Upload Excel File
    uploaded_file = st.file_uploader("Upload Rotation Excel File", type=["xlsx"])
    if uploaded_file:
        df = load_data(uploaded_file)
        
        # Display original data in the Streamlit app
        st.write("Original Data:")
        st.dataframe(df)

        # Extract relevant columns for drag and drop functionality
        list_items = df.apply(lambda row: f"Line {row['Line']}: " + ' | '.join(map(str, row[1:])), axis=1).tolist()

        # Drag-and-Drop sort using Streamlit Sortables
        sorted_items = sort_items(list_items)

        # Convert sorted list back to DataFrame for easier processing
        sorted_lines = [item.split(': ')[0] for item in sorted_items]  # Extract line numbers from sorted items
        sorted_df = df[df['Line'].isin(sorted_lines)].copy()  # Keep sorted order

        # Display sorted DataFrame
        st.write("Sorted Data:")
        st.dataframe(sorted_df)

        # Option to save rankings
        if st.button("Save Rankings as Excel"):
            excel_file = export_to_excel(sorted_df, "Ranked_Rotations.xlsx")
            st.download_button(label="Download Ranked Excel File", data=excel_file, file_name="Ranked_Rotations.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Option to save rankings to JSON
        if st.button("Save Rankings as JSON"):
            json_data = sorted_df.to_json(indent=4, orient='records')
            st.download_button(label="Download Ranked JSON File", data=json_data, file_name="Ranked_Rotations.json", mime="application/json")

if __name__ == "__main__":
    main()
