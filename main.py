import streamlit as st
import pandas as pd
from docx import Document
import csv
import re

# CTR data
ctr_data = {
    1: 33.25, 2: 14.17, 3: 9.17, 4: 5.44, 5: 3.36,
    6: 2.18, 7: 1.49, 8: 1.11, 9: 0.83, 10: 0.65,
    11: 0.59, 12: 0.58, 13: 0.69, 14: 0.73, 15: 0.72,
    16: 0.60, 17: 0.70, 18: 0.49, 19: 0.54, 20: 0.46
}

def calculate_traffic_and_conversions(search_volume, current_rank, target_rank, app_start_rate, app_submit_rate):
    current_ctr = ctr_data.get(current_rank, 0) / 100
    target_ctr = ctr_data.get(target_rank, 0) / 100
    
    current_traffic = search_volume * current_ctr
    target_traffic = search_volume * target_ctr
    incremental_traffic = target_traffic - current_traffic
    
    current_app_starts = current_traffic * app_start_rate
    current_app_submits = current_app_starts * app_submit_rate
    
    target_app_starts = target_traffic * app_start_rate
    target_app_submits = target_app_starts * app_submit_rate
    
    incremental_app_starts = target_app_starts - current_app_starts
    incremental_app_submits = target_app_submits - current_app_submits
    
    return {
        "current_traffic": round(current_traffic),
        "target_traffic": round(target_traffic),
        "incremental_traffic": round(incremental_traffic),
        "current_app_starts": round(current_app_starts),
        "current_app_submits": round(current_app_submits),
        "target_app_starts": round(target_app_starts),
        "target_app_submits": round(target_app_submits),
        "incremental_app_starts": round(incremental_app_starts),
        "incremental_app_submits": round(incremental_app_submits)
    }

def main():
    st.set_page_config(page_title="SEO Content Optimizer", layout="wide")
    st.title("SEO Content Optimizer")
    st.write("Created by Brandon Lazovic")
    
    st.markdown("""
    ### How to use this tool:
    1. Fill in the information for each section below.
    2. Use the tooltips (?) for guidance on SEO best practices.
    3. Click 'Generate Output' to preview the results.
    4. Export the data to Word or CSV format.
    """)

    if 'data' not in st.session_state:
        st.session_state.data = {}

    keyword_research()
    serp_analysis()
    on_page_elements()
    traffic_and_conversions()

    if st.button("Generate Output"):
        generate_output()

def keyword_research():
    st.header("Keyword Research")
    
    st.session_state.data['primary_keyword'] = st.text_input(
        "Primary Keyword",
        help="Enter 1 primary keyword for the page to target."
    )
    
    st.session_state.data['secondary_keywords'] = st.text_input(
        "Secondary Keywords",
        help="Enter 3-5 secondary keywords for the page to target, separated by commas."
    )
    
    st.session_state.data['search_volume'] = st.number_input(
        "Search Volume",
        min_value=0,
        help="Enter the monthly search volume number for the primary keyword."
    )
    
    st.session_state.data['current_rank'] = st.number_input(
        "Current Keyword Rank Position",
        min_value=1,
        max_value=20,
        help="Enter the current rank position for the primary keyword."
    )

def serp_analysis():
    st.header("SERP Analysis")
    
    st.session_state.data['search_intent'] = st.text_area(
        "Search Intent",
        help="Describe the search intent for the primary keyword."
    )
    
    st.session_state.data['search_features'] = st.text_area(
        "Search Features",
        help="List the search features present in the SERP for the primary keyword."
    )
    
    st.session_state.data['common_questions'] = st.text_area(
        "Common Questions",
        help="List common questions asked by users related to the primary keyword."
    )

def on_page_elements():
    st.header("On-Page Elements")
    
    st.session_state.data['h1_tag'] = st.text_input(
        "H1 Tag",
        help="Enter the H1 tag. Ensure the primary keyword is targeted and it's 65 characters or less.",
        max_chars=65
    )
    
    st.session_state.data['meta_title'] = st.text_input(
        "Meta Title",
        help="Enter the meta title. Ensure the primary keyword is targeted and it's 65 characters or less.",
        max_chars=65
    )
    
    st.session_state.data['meta_description'] = st.text_area(
        "Meta Description",
        help="Enter the meta description. Ensure the primary keyword is targeted and it's 155 characters or less.",
        max_chars=155
    )
    
    st.session_state.data['url_recommendation'] = st.text_input(
        "URL Recommendation",
        help="Enter the recommended URL. Ensure the primary keyword is in the slug, it's lowercase, stop-words are omitted, uses hyphens, and is concise."
    )
    
    st.session_state.data['keyword_in_first_100'] = st.checkbox(
        "Is the primary keyword included in the first 100 words of the article?",
        help="Check if the primary keyword appears in the first 100 words of the content."
    )
    
    st.session_state.data['faqs'] = st.text_area(
        "FAQs to include as subheads",
        help="Enter FAQs that should be included on-page as subheads. Separate each FAQ with a new line."
    )
    
    st.session_state.data['product_pages'] = st.text_area(
        "Product Pages to Link",
        help="Enter product pages that should be linked to, including anchor text with primary keyword target. Separate each entry with a new line."
    )
    
    st.session_state.data['articles'] = st.text_area(
        "Articles to Link",
        help="Enter articles that should be linked to, including anchor text with primary keyword target. Separate each entry with a new line."
    )
    
    st.session_state.data['breadcrumbs'] = st.text_input(
        "Breadcrumbs",
        help="Enter the breadcrumb structure. Ensure it meets proper format and aligns with the primary keyword target."
    )
    
    st.session_state.data['schema_markup'] = st.multiselect(
        "Schema Markup",
        options=["None", "Article", "Product", "FAQ", "How-to", "Local Business", "Event", "Recipe", "Review"],
        help="Select the schema markup types that should be included on the page."
    )
    
    st.session_state.data['heading_hierarchy'] = st.checkbox(
        "Does this page follow heading hierarchy best practices?",
        help="Check if the page follows proper heading hierarchy (e.g., single H1, H2s precede H3s, etc.)"
    )

def traffic_and_conversions():
    st.header("Traffic and Conversion Estimation")
    
    st.session_state.data['target_rank'] = st.number_input(
        "Target Keyword Rank Position",
        min_value=1,
        max_value=20,
        help="Enter the target rank position for the primary keyword."
    )
    
    st.session_state.data['app_start_rate'] = st.slider(
        "App Start Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        help="Enter the percentage of visitors who start the app."
    ) / 100

    st.session_state.data['app_submit_rate'] = st.slider(
        "App Submit Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.1,
        help="Enter the percentage of app starts that result in a submission."
    ) / 100

def generate_output():
    st.header("Output Preview")
    
    # Calculate traffic and conversions
    traffic_data = calculate_traffic_and_conversions(
        st.session_state.data['search_volume'],
        st.session_state.data['current_rank'],
        st.session_state.data['target_rank'],
        st.session_state.data['app_start_rate'],
        st.session_state.data['app_submit_rate']
    )
    
    st.session_state.data.update(traffic_data)
    
    df = pd.DataFrame(st.session_state.data.items(), columns=['Field', 'Value'])
    st.table(df)
    
    st.subheader("Traffic and Conversion Estimates")
    st.write(f"Current Monthly Traffic: {traffic_data['current_traffic']}")
    st.write(f"Target Monthly Traffic: {traffic_data['target_traffic']}")
    st.write(f"Incremental Monthly Traffic: {traffic_data['incremental_traffic']}")
    st.write(f"Current Monthly App Starts: {traffic_data['current_app_starts']}")
    st.write(f"Current Monthly App Submits: {traffic_data['current_app_submits']}")
    st.write(f"Target Monthly App Starts: {traffic_data['target_app_starts']}")
    st.write(f"Target Monthly App Submits: {traffic_data['target_app_submits']}")
    st.write(f"Incremental Monthly App Starts: {traffic_data['incremental_app_starts']}")
    st.write(f"Incremental Monthly App Submits: {traffic_data['incremental_app_submits']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export to Word"):
            export_to_word(st.session_state.data)
    with col2:
        if st.button("Export to CSV"):
            export_to_csv(st.session_state.data)

def export_to_word(data):
    doc = Document()
    doc.add_heading("SEO Content Optimization Report", 0)
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Field'
    hdr_cells[1].text = 'Value'
    
    for field, value in data.items():
        row_cells = table.add_row().cells
        row_cells[0].text = field
        row_cells[1].text = str(value)
    
    doc.save("seo_content_optimization_report.docx")
    st.success("Word document exported successfully!")

def export_to_csv(data):
    with open('seo_content_optimization_report.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Field", "Value"])
        for field, value in data.items():
            writer.writerow([field, value])
    st.success("CSV file exported successfully!")

if __name__ == "__main__":
    main()
