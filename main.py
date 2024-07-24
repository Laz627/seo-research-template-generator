import streamlit as st
import pandas as pd
from docx import Document
import csv

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
    3. Click the export buttons to generate reports in Word or CSV format.
    """)

    if 'data' not in st.session_state:
        st.session_state.data = {}

    keyword_research()
    serp_analysis()
    on_page_elements()
    internal_links()
    traffic_and_conversions()

    if st.button("Export to Word"):
        export_to_word(st.session_state.data, st.session_state.keyword_data, calculate_all_traffic_and_conversions())

    if st.button("Export to CSV"):
        export_to_csv(st.session_state.data, st.session_state.keyword_data, calculate_all_traffic_and_conversions())

def keyword_research():
    st.header("Keyword Research")
    
    if 'keyword_data' not in st.session_state:
        st.session_state.keyword_data = [{"keyword": "", "search_volume": 0, "current_rank": 1}]
    
    def add_keyword():
        st.session_state.keyword_data.append({"keyword": "", "search_volume": 0, "current_rank": 1})
    
    def remove_keyword(index):
        st.session_state.keyword_data.pop(index)
    
    for i, keyword in enumerate(st.session_state.keyword_data):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            keyword["keyword"] = st.text_input(f"Keyword {i+1}", keyword["keyword"], key=f"keyword_{i}")
        
        with col2:
            keyword["search_volume"] = st.number_input(f"Search Volume {i+1}", min_value=0, value=keyword["search_volume"], key=f"volume_{i}")
        
        with col3:
            keyword["current_rank"] = st.number_input(f"Current Rank {i+1}", min_value=1, max_value=100, value=keyword["current_rank"], key=f"rank_{i}")
        
        with col4:
            if st.button("Remove", key=f"remove_{i}"):
                remove_keyword(i)
                st.experimental_rerun()
    
    if st.button("Add Keyword"):
        add_keyword()
        st.experimental_rerun()

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
    
    st.session_state.data['breadcrumbs'] = st.text_input(
        "Breadcrumbs",
        help="Enter the breadcrumb structure. Ensure it meets proper format and aligns with the primary keyword target."
    )
    
    schema_options = [
        "None", "WebPage", "Article", "Product", "FAQ", "HowTo", "LocalBusiness", 
        "Event", "Recipe", "Review", "BreadcrumbList", "FinancialProduct", 
        "Organization", "Person", "VideoObject", "ImageObject", "Service", 
        "SoftwareApplication", "Course", "JobPosting"
    ]
    
    st.session_state.data['schema_markup'] = st.multiselect(
        "Schema Markup",
        options=schema_options,
        help="Select the schema markup types that should be included on the page."
    )
    
    st.session_state.data['heading_hierarchy'] = st.checkbox(
        "Does this page follow heading hierarchy best practices?",
        help="Check if the page follows proper heading hierarchy (e.g., single H1, H2s precede H3s, etc.)"
    )

def internal_links():
    st.header("Internal Links")
    
    if 'internal_links' not in st.session_state:
        st.session_state.internal_links = []
    
    for i, link in enumerate(st.session_state.internal_links):
        col1, col2, col3, col4 = st.columns([3, 3, 1, 1])
        with col1:
            link['url'] = st.text_input("URL", link['url'], key=f"url_{i}")
        with col2:
            link['anchor_text'] = st.text_input("Anchor Text", link['anchor_text'], key=f"anchor_{i}")
        with col3:
            link['type'] = st.selectbox("Type", ["Product", "Article"], key=f"type_{i}")
        with col4:
            if st.button("Remove", key=f"remove_link_{i}"):
                st.session_state.internal_links.pop(i)
                st.experimental_rerun()
    
    if st.button("Add Internal Link"):
        st.session_state.internal_links.append({"url": "", "anchor_text": "", "type": "Product"})
        st.experimental_rerun()

def calculate_all_traffic_and_conversions():
    all_traffic_data = []
    for keyword in st.session_state.keyword_data:
        traffic_data = calculate_traffic_and_conversions(
            keyword['search_volume'],
            keyword['current_rank'],
            keyword['target_rank'],
            st.session_state.data['app_start_rate'],
            st.session_state.data['app_submit_rate']
        )
        all_traffic_data.append({
            'keyword': keyword['keyword'],
            **traffic_data
        })
    return all_traffic_data

def traffic_and_conversions():
    st.header("Traffic and Conversion Estimation")
    
    if st.session_state.keyword_data:
        for i, keyword in enumerate(st.session_state.keyword_data):
            keyword['target_rank'] = st.number_input(
                f"Target Rank for '{keyword['keyword']}'",
                min_value=1,
                max_value=100,
                value=max(1, keyword['current_rank'] - 1),
                key=f"target_rank_{i}"
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
    else:
        st.write("Please add at least one keyword in the Keyword Research section to enable traffic and conversion estimation.")

def export_to_word(data, keyword_data, traffic_data):
    doc = Document()
    doc.add_heading("SEO Content Optimization Report", 0)
    
    # Add keyword data table
    doc.add_heading("Keyword Data", level=1)
    keyword_table = doc.add_table(rows=1, cols=5)
    keyword_table.style = 'Table Grid'
    hdr_cells = keyword_table.rows[0].cells
    hdr_cells[0].text = 'Keyword'
    hdr_cells[1].text = 'Search Volume'
    hdr_cells[2].text = 'Current Rank'
    hdr_cells[3].text = 'Target Rank'
    hdr_cells[4].text = 'Incremental Traffic'
    
    for kw, td in zip(keyword_data, traffic_data):
        row_cells = keyword_table.add_row().cells
        row_cells[0].text = kw['keyword']
        row_cells[1].text = str(kw['search_volume'])
        row_cells[2].text = str(kw['current_rank'])
        row_cells[3].text = str(kw['target_rank'])
        row_cells[4].text = str(td['incremental_traffic'])
    
    # Add other data
    doc.add_heading("On-Page Elements", level=1)
    for field, value in data.items():
        if field not in ['app_start_rate', 'app_submit_rate']:
            doc.add_paragraph(f"{field}: {value}")
    
    # Add internal links
    doc.add_heading("Internal Links", level=1)
    links_table = doc.add_table(rows=1, cols=3)
    links_table.style = 'Table Grid'
    hdr_cells = links_table.rows[0].cells
    hdr_cells[0].text = 'URL'
    hdr_cells[1].text = 'Anchor Text'
    hdr_cells[2].text = 'Type'
    
    for link in st.session_state.internal_links:
        row_cells = links_table.add_row().cells
        row_cells[0].text = link['url']
        row_cells[1].text = link['anchor_text']
        row_cells[2].text = link['type']
    
    doc.save("seo_content_optimization_report.docx")
    st.success("Word document exported successfully!")

def export_to_csv(data, keyword_data, traffic_data):
    with open('seo_content_optimization_report.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword Data"])
        writer.writerow(["Keyword", "Search Volume", "Current Rank", "Target Rank", "Incremental Traffic"])
        for kw, td in zip(keyword_data, traffic_data):
            writer.writerow([kw['keyword'], kw['search_volume'], kw['current_rank'], kw['target_rank'], td['incremental_traffic']])
        
        writer.writerow([])
        writer.writerow(["On-Page Elements"])
        for field, value in data.items():
            if field not in ['app_start_rate', 'app_submit_rate']:
                writer.writerow([field, value])
        
        writer.writerow([])
        writer.writerow(["Internal Links"])
        writer.writerow(["URL", "Anchor Text", "Type"])
        for link in st.session_state.internal_links:
            writer.writerow([link['url'], link['anchor_text'], link['type']])
    
    st.success("CSV file exported successfully!")

if __name__ == "__main__":
    main()
