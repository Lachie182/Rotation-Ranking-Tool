# Importing necessary libraries
import pandas as pd
import streamlit as st
import json
import io
from openpyxl import Workbook
import streamlit.components.v1 as components

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
    writer.close()
    output.seek(0)
    return output

# Load drag-and-drop component script
def drag_drop_js():
    return """
    <script>
    function initSortable() {
        const el = document.getElementById("sortable-list");
        Sortable.create(el, {
            animation: 150,
            onEnd: function (evt) {
                let order = [];
                for (let i = 0; i < el.children.length; i++) {
                    order.push(el.children[i].dataset.index);
                }
                const streamlitObj = {
                    type: "dragOrder",
                    order: order
                };
                window.parent.postMessage(JSON.stringify(streamlitObj), "*");
            }
        });
    }
    initSortable();
    </script>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    """

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

        # Create drag-and-drop list
        html_list = "<ul id='sortable-list' style='list-style-type:none; padding-left: 0;'>"
        for idx, item in enumerate(list_items):
            html_list += f"<li data-index='{idx}' style='padding: 10px; border: 1px solid black; margin: 5px; background-color: #f0f0f0;'>{item}</li>"
        html_list += "</ul>"

        # Display HTML and add JS script for drag-and-drop
        components.html(f"{html_list}{drag_drop_js()}", height=500)

        # Get the final ranking after drag-and-drop
        order_json = st.text_area("Paste new order JSON here (after drag-and-drop in browser)")

        # If user has entered new order, process it
        if order_json:
            order_data = json.loads(order_json)
            sorted_items = [list_items[int(idx)] for idx in order_data]
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
