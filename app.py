import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from PIL import Image as PILImage
import pdfkit
from jinja2 import Template
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from io import BytesIO
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def main():
    st.set_page_config(page_title="ROI Calculator", page_icon="📊", layout="wide")
    
    # Custom CSS to match SnapLogic brand colors and style the output
    st.markdown("""
    <style>
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .stButton>button {
        color: white !important;
        background-color: #0077BE;
        border-color: #0077BE;
    }
    .stButton>button:hover {
        background-color: #005c91;
        border-color: #005c91;
        color: white !important;
    }
    .stButton>button:focus:not(:active) {
        color: white !important;
        border-color: #005c91;
        box-shadow: none;
    }
    .stButton > button,
    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:active,
    .stButton > button:disabled {
        color: white !important;
        background-color: #0077BE !important;
        border-color: #0077BE !important;
    }
    .stButton > button:hover {
        background-color: #005c91 !important;
        border-color: #005c91 !important;
    }
    .stButton > button * {
        color: white !important;
    }

    /* Ensure text color for any child elements */
    .stButton > button span,
    .stButton > button p,
    .stButton > button div {
        color: white !important;
    }
    .total-savings {
        font-size: 24px;
        font-weight: bold;
        color: #0077BE;
        margin-bottom: 20px;
        padding: 15px;
        border: 2px solid #0077BE;
        border-radius: 5px;
        display: inline-block;
        background-color: var(--background-color);
    }
    .dataframe {
        width: 100%;
        text-align: left;
        border-collapse: collapse;
        color: var(--text-color);
    }
    .dataframe th {
        background-color: #0077BE;
        color: white;
        font-weight: bold;
        padding: 10px;
        text-align: left;  /* Add this line to left-align column names */
    }
    .dataframe td {
        padding: 10px;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-color);
    }
    .dataframe tr:nth-of-type(even) {
        background-color: var(--even-row-color);
    }
    .logo-container {
        text-align: center;
        padding: 10px;
    }
    .logo-container img {
        margin-bottom: 0;
    }
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
    }
    p {
        color: var(--text-color);
    }
    .streamlit-expanderHeader {
        margin-bottom: 0 !important;
        color: var(--text-color);
    }
    .stPlotlyChart {
        margin-top: -40px;
    }
    .savings-breakdown-header {
        margin-bottom: 20px !important;
        color: var(--text-color);
    }
    .savings-table {
        margin-top: 10px;
    }
    .description-box {
        background-color: var(--description-box-bg);
        border: 2px solid #0077BE;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .description-box h4 {
        color: #0077BE;
        margin-top: 0;
        margin-bottom: 10px;
    }
    .description-box p {
        margin-bottom: 10px;
        color: var(--text-color);
    }
    .output-container {
        background-color: var(--output-container-bg);
        border: 2px solid #0077BE;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: var(--text-color);
    }
    .output-container h3 {
        color: #0077BE;
        margin-top: 0;
        margin-bottom: 15px;
    }
    
    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #1E1E1E;
            --text-color: #E0E0E0;
            --border-color: #444444;
            --even-row-color: #2A2A2A;
            --description-box-bg: #2A2A2A;
            --output-container-bg: #2A2A2A;
        }
    }
    
    /* Light mode styles */
    @media (prefers-color-scheme: light) {
        :root {
            --background-color: #FFFFFF;
            --text-color: #333333;
            --border-color: #DDDDDD;
            --even-row-color: #F8F9FA;
            --description-box-bg: #F0F8FF;
            --output-container-bg: #F8F9FA;
        }
    }

    /* Updated styles for tooltips */
    :root {
        --tooltip-bg-color: #f8f9fa;
        --tooltip-text-color: #212529;
    }

    [data-theme="dark"] {
        --tooltip-bg-color: #f8f9fa;
        --tooltip-text-color: #000000;
    }

    .tooltip {
        position: relative;
        display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: var(--tooltip-bg-color);
        color: var(--tooltip-text-color);
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .stDownloadButton > button {
        color: white !important;
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
    }
    .stDownloadButton > button:hover {
        background-color: #EA3535 !important;
        border-color: #EA3535 !important;
    }
    .stDownloadButton > button:focus:not(:active) {
        color: white !important;
        border-color: #EA3535 !important;
        box-shadow: none;
    }
    .stDownloadButton > button * {
        color: white !important;
    }

    /* Ensure text color for any child elements */
    .stDownloadButton > button span,
    .stDownloadButton > button p,
    .stDownloadButton > button div {
        color: white !important;
    }

    /* Updated styles for the buttons */
    .stButton > button {
        height: 3rem;
        padding: 0 1rem;
        white-space: nowrap;
    }
    .stDownloadButton > button {
        color: white !important;
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
        height: 3rem;
        padding: 0 1rem;
        white-space: nowrap;
    }
    .stDownloadButton > button:hover {
        background-color: #EA3535 !important;
        border-color: #EA3535 !important;
    }
    .stDownloadButton > button:focus:not(:active) {
        color: white !important;
        border-color: #EA3535 !important;
        box-shadow: none;
    }
    .stDownloadButton > button * {
        color: white !important;
    }

    /* Custom CSS to reduce gap between buttons */
    .button-container {
        display: flex;
        gap: 0px;
    }
    .button-container > div {
        flex: 0 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add SnapLogic logo
    logo = PILImage.open("snaplogic_logo.png")
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo, width=200)  # Adjust the width as needed
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("ROI Calculator")

    # Add description in a compact pretty box spanning both columns
    st.markdown("""
    <div class="description-box">
        <h4>Hi there!</h4>
        <p> Welcome to SnapLogic's ROI calculator. </p>
        <p>Please enter your current customer parameters. If you're just getting started, feel free to use the example values to see how the tool works. </p>
        <p>If you have any questions, please reach out to the SE team 👩🏻‍💻 </p>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns
    left_column, right_column = st.columns(2)

    with left_column:
        # Toggle for example/custom values
        use_example = st.toggle("Use Example Values", value=True)

        # Dictionary of example values
        example_values = {
            "General": {
                "FTE Developer Rate": 45.0,
            },
            "Without SnapLogic": {
                "Months to Onboard": 24,
                "FTE Capacity Used for Onboarding (%)": 20,
                "Current Number of Integrations": 100,
                "Planned Number of Integrations (Per Year)": 10,
                "Hours to Build An Integration": 200,
                "Number of FTE Supporting Integrations": 10,
                "FTE Capacity Used for Maintenance (%)": 50
            },
            "With SnapLogic": {
                "Number of Integrations to be Moved": 100
        }
        }

        # Dictionary to store current values
        values = {category: {} for category in example_values}

        # Create input fields for all parameters in separate boxes
        for category, params in example_values.items():
            with st.expander(f"{category}", expanded=False):
                for key, example_value in params.items():
                    # Create a unique key for each input field
                    input_key = f"{category}_{key}"
                    
                    if key == "FTE Developer Rate":
                        values[category][key] = st.number_input(
                            f"{key} (£):",
                            min_value=0.0,
                            value=values[category].get(key, example_value),
                            step=0.01,
                            format="%.2f",
                            disabled=use_example,
                            key=input_key
                        )
                    elif key in ["FTE Capacity Used for Onboarding (%)", "FTE Capacity Used for Maintenance (%)"]:
                        values[category][key] = st.number_input(
                            f"{key}:",
                            min_value=0,
                            max_value=100,
                            value=int(values[category].get(key, example_value)),
                            step=1,
                            disabled=use_example,
                            key=input_key
                        )
                    elif isinstance(example_value, float):
                        values[category][key] = st.number_input(
                            f"{key}:",
                            min_value=0.0,
                            value=values[category].get(key, example_value),
                            step=0.01,
                            format="%.2f",
                            disabled=use_example,
                            key=input_key
                        )
                    else:
                        values[category][key] = st.number_input(
                            f"{key}:",
                            min_value=0,
                            value=values[category].get(key, example_value),
                            step=1,
                            disabled=use_example,
                            key=input_key
                        )

        # Create a container for the buttons
        button_container = st.container()

        # Use custom HTML for button layout
        button_container.markdown('<div class="button-container">', unsafe_allow_html=True)
        
        # Create two columns for the buttons with no gap
        col1, col2, _ = button_container.columns([1, 1.5, 2])

        # Submit button in the first column
        with col1:
            submit_button = st.button("Submit")

        # Placeholder for the download button in the second column
        with col2:
            download_button_placeholder = st.empty()

        button_container.markdown('</div>', unsafe_allow_html=True)

    with right_column:
        if submit_button:
            display_values = example_values if use_example else values

            try:
                # Calculate OTE FTE Developer
                ote_fte_developer = display_values["General"]["FTE Developer Rate"] * 40 * 52
                with_snaplogic_months_to_onboard = int(display_values["Without SnapLogic"]["Months to Onboard"] * 0.1)
                with_snaplogic_fte_capacity_onboarding = display_values["Without SnapLogic"]["FTE Capacity Used for Onboarding (%)"]
                with_snaplogic_fte_capacity_maintenance = display_values["Without SnapLogic"]["FTE Capacity Used for Maintenance (%)"] * 0.5
                with_snaplogic_hours_build_integration  = display_values["Without SnapLogic"]["Hours to Build An Integration"] * 0.1
                with_snaplogic_n_people_supporting_integrations = int(display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"] * 0.30)
                
                # Perform the calculations
                without_snaplogic_employee_onboarding = (
                    display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"] *
                    display_values["Without SnapLogic"]["FTE Capacity Used for Onboarding (%)"]/100 *
                    (ote_fte_developer *
                     display_values["Without SnapLogic"]["Months to Onboard"] / 12)
                )

                with_snaplogic_employee_onboarding = (
                    with_snaplogic_n_people_supporting_integrations *
                    with_snaplogic_fte_capacity_onboarding/100 *
                    (ote_fte_developer *
                     with_snaplogic_months_to_onboard / 12)
                )

                # Calculate development costs
                without_snaplogic_dev_cost = display_values["Without SnapLogic"]["Planned Number of Integrations (Per Year)"] * display_values["Without SnapLogic"]["Hours to Build An Integration"] * display_values["General"]["FTE Developer Rate"]
                with_snaplogic_dev_cost = display_values["Without SnapLogic"]["Planned Number of Integrations (Per Year)"] * with_snaplogic_hours_build_integration * display_values["General"]["FTE Developer Rate"]

                # Calculate maintenance costs
                without_snaplogic_maintenance_cost = display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"] * display_values["Without SnapLogic"]["FTE Capacity Used for Maintenance (%)"]/100 * ote_fte_developer
                with_snaplogic_maintenance_cost = with_snaplogic_n_people_supporting_integrations * with_snaplogic_fte_capacity_maintenance/100 * ote_fte_developer

                # Calculate savings
                employee_onboarding_savings = without_snaplogic_employee_onboarding - with_snaplogic_employee_onboarding
                development_cost_savings = without_snaplogic_dev_cost - with_snaplogic_dev_cost
                maintenance_cost_savings = without_snaplogic_maintenance_cost - with_snaplogic_maintenance_cost
                total_savings = employee_onboarding_savings + development_cost_savings + maintenance_cost_savings

                # Calculate savings per integration
                without_snaplogic_employee_onboarding_cost_per_integration = (without_snaplogic_employee_onboarding / display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"]) 
                with_snaplogic_employee_onboarding_cost_per_integration = (with_snaplogic_employee_onboarding / with_snaplogic_n_people_supporting_integrations)
                with_snaplogic_dev_cost_per_integration = (with_snaplogic_dev_cost / display_values["Without SnapLogic"]["Planned Number of Integrations (Per Year)"])
                without_snaplogic_dev_cost_per_integration = (without_snaplogic_dev_cost / display_values["Without SnapLogic"]["Planned Number of Integrations (Per Year)"])
                with_snaplogic_maintenance_cost_per_integration = (with_snaplogic_maintenance_cost / (display_values["Without SnapLogic"]["Planned Number of Integrations (Per Year)"] + display_values["With SnapLogic"]["Number of Integrations to be Moved"]))
                without_snaplogic_maintenance_cost_per_integration = (without_snaplogic_maintenance_cost / (display_values["Without SnapLogic"]["Planned Number of Integrations (Per Year)"] + display_values["Without SnapLogic"]["Current Number of Integrations"]))

                # Create a dataframe for the savings per integration table
                savings_per_integration_data = {
                    "Category": ["Employee Onboarding Cost", "Development Cost", "Maintenance Cost"],
                    "Without SnapLogic": [
                        f"${int(round(without_snaplogic_employee_onboarding_cost_per_integration)):,}",
                        f"${int(round(without_snaplogic_dev_cost_per_integration)):,}",
                        f"${int(round(without_snaplogic_maintenance_cost_per_integration)):,}"
                    ],
                    "With SnapLogic": [
                        f"${int(round(with_snaplogic_employee_onboarding_cost_per_integration)):,}",
                        f"${int(round(with_snaplogic_dev_cost_per_integration)):,}",
                        f"${int(round(with_snaplogic_maintenance_cost_per_integration)):,}"
                    ]
                }
                savings_per_integration_df = pd.DataFrame(savings_per_integration_data)

                # Replace the tabs with a single box showing 5-year and annual savings
                st.markdown("""
                <div class="total-savings">
                    <h2>Total 5 Year Cost Savings with SnapLogic</h2>
                    <div class="big-savings">${:,}</div>
                    <h3>Annual Cost Savings</h3>
                    <div class="annual-savings">${:,}</div>
                </div>
                """.format(int(round(total_savings * 5)), int(round(total_savings))), unsafe_allow_html=True)

                # Add this CSS to your existing styles
                st.markdown("""
                <style>
                .total-savings {
                    text-align: center;
                    padding: 20px;
                    border: 2px solid #0077BE;
                    border-radius: 10px;
                    background-color: var(--background-color);
                }
                .total-savings h2 {
                    color: #0077BE;
                    margin-bottom: 10px;
                }
                .big-savings {
                    font-size: 48px;
                    font-weight: bold;
                    color: #0077BE;
                    margin-bottom: 20px;
                }
                .total-savings h3 {
                    color: #0077BE;
                    margin-bottom: 5px;
                }
                .annual-savings {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0077BE;
                }
                </style>
                """, unsafe_allow_html=True)

                # Create a dataframe for the savings table
                savings_data = {
                    "Category": ["Employee Onboarding Savings", "Development Cost Savings", "Maintenance Cost Savings"],
                    "Amount": [
                        f"${int(round(employee_onboarding_savings)):,}",
                        f"${int(round(development_cost_savings)):,}",
                        f"${int(round(maintenance_cost_savings)):,}"
                    ]
                }
                savings_df = pd.DataFrame(savings_data)

                # Create hover descriptions
                hover_descriptions = {
                    "Employee Onboarding Savings": "This refers to the reduction in costs associated with onboarding users onto integration systems. With SnapLogic, the time and resources required to onboard employees are significantly reduced, leading to cost savings.",
                    "Development Cost Savings": "These are the savings realized in the process of creating new integrations. SnapLogic's platform allows for faster and more efficient development of integrations, reducing the time and effort required, which translates to lower development costs.",
                    "Maintenance Cost Savings": "This represents the reduced expenses for ongoing upkeep and management of existing integrations. SnapLogic's platform typically requires less maintenance effort compared to traditional integration methods, resulting in lower costs for maintaining integrations."
                }

                # Create custom CSS for hover effect
                hover_css = """
                <style>
                .hover-info {
                    display: none;
                    position: absolute;
                    background-color: #f9f9f9;
                    border: 1px solid #ccc;
                    padding: 10px;
                    z-index: 1000;
                    max-width: 300px;
                    color: #000000 !important; /* Force black text */
                }
                .dataframe td:first-child {
                    position: relative;
                    cursor: help;
                }
                .dataframe td:first-child:hover .hover-info {
                    display: block;
                }
                </style>
                """

                # Apply custom CSS
                st.markdown(hover_css, unsafe_allow_html=True)

                # Display the savings table with hover effect
                st.subheader("Savings Breakdown (Annual)")
                
                # Create a copy of the dataframe with hover info
                hover_df = savings_df.copy()
                hover_df['Category'] = hover_df['Category'].apply(lambda x: f"{x}<div class='hover-info'>{hover_descriptions[x]}</div>")
                
                # Display the table with left-aligned headers
                st.markdown(hover_df.to_html(escape=False, index=False, classes='dataframe'), unsafe_allow_html=True)

                # Create interactive stacked bar plot
                fig = go.Figure(data=[
                    go.Bar(name='Employee Onboarding Cost', x=['Without SnapLogic', 'With SnapLogic'], 
                           y=[without_snaplogic_employee_onboarding, with_snaplogic_employee_onboarding],
                           marker_color='#0077BE',
                           hovertemplate='Employee Onboarding Cost: $%{y:,.0f}<extra></extra>'),  # SnapLogic blue
                    go.Bar(name='Maintenance Cost', x=['Without SnapLogic', 'With SnapLogic'], 
                           y=[without_snaplogic_maintenance_cost, with_snaplogic_maintenance_cost],
                           marker_color='#00A8E8',
                           hovertemplate='Maintenance Cost: $%{y:,.0f}<extra></extra>'),  # Lighter blue
                    go.Bar(name='Development Cost', x=['Without SnapLogic', 'With SnapLogic'], 
                           y=[without_snaplogic_dev_cost, with_snaplogic_dev_cost],
                           marker_color='#F7931E',
                           hovertemplate='Development Cost: $%{y:,.0f}<extra></extra>')  # SnapLogic orange
                ])

                fig.update_layout(
                    barmode='stack',
                    yaxis=dict(tickformat='$,.0f'),
                    height=600,
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent surrounding
                    font=dict(color='#333333'),  # Dark gray text
                    hovermode='closest'
                )

                # Display the chart with an even smaller subheader and less space
                st.subheader("Cost Comparison (Annual)")
                st.plotly_chart(fig, use_container_width=True)

                # Create hover descriptions for Cost Per Integration
                cost_per_integration_descriptions = {
                    "Employee Onboarding Cost": "This represents the cost of onboarding employees to use integration systems, calculated per integration.",
                    "Development Cost": "This is the cost of creating a new integration.",
                    "Maintenance Cost": "This shows the ongoing cost to maintain each integration."
                }

                # Modify the display of the Cost Per Integration table
                st.subheader("Cost Per Integration (Annual)")
                
                # Create a copy of the dataframe with hover info
                hover_cost_per_integration_df = savings_per_integration_df.copy()
                hover_cost_per_integration_df['Category'] = hover_cost_per_integration_df['Category'].apply(lambda x: f"{x}<div class='hover-info'>{cost_per_integration_descriptions[x]}</div>")
                
                # Display the table with left-aligned headers
                st.markdown(hover_cost_per_integration_df.to_html(escape=False, index=False, classes='dataframe'), unsafe_allow_html=True)

                # Generate PDF data
                pdf_data = generate_pdf(total_savings, savings_df, savings_per_integration_df, hover_descriptions)

                # Display the download button in the placeholder
                with col2:
                    download_button_placeholder.download_button(
                        label="Download Report",
                        data=pdf_data,
                        file_name="roi_report.pdf",
                        mime="application/pdf"
                    )

                # Add some space between the button and the savings box
                st.markdown("<br>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred during calculation: {str(e)}")
                # Clear the download button if there's an error
                with col2:
                    download_button_placeholder.empty()

def generate_pdf(total_savings, savings_df, savings_per_integration_df, hover_descriptions):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*cm, bottomMargin=1*cm, leftMargin=1.5*cm, rightMargin=1.5*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor("#0077BE"),
        spaceAfter=0.5*cm,
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#0077BE"),
        spaceAfter=0.3*cm,
        spaceBefore=0.3*cm
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=9,
        textColor=colors.black,
        spaceAfter=0.2*cm
    )

    # Add logo
    pil_img = PILImage.open("snaplogic_logo.png")
    img_width, img_height = pil_img.size
    aspect = img_height / float(img_width)
    desired_width = 4 * cm
    desired_height = desired_width * aspect

    logo = Image("snaplogic_logo.png", width=desired_width, height=desired_height)
    elements.append(logo)
    elements.append(Spacer(1, 0.5*cm))

    # Add title
    elements.append(Paragraph("ROI Calculator Report", title_style))

    # Create a box for total savings
    savings_box = Table([
        [Paragraph(f"Total 5 Year Cost Savings with SnapLogic", subtitle_style)],
        [Paragraph(f"<font size=14>${int(round(total_savings * 5)):,}</font>", body_style)],
        [Paragraph(f"Annual Cost Savings", subtitle_style)],
        [Paragraph(f"<font size=12>${int(round(total_savings)):,}</font>", body_style)]
    ], colWidths=[doc.width])
    
    savings_box.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#0077BE")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F8FF")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#0077BE")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(savings_box)
    elements.append(Spacer(1, 0.5*cm))

    # Add savings breakdown table
    elements.append(Paragraph("Savings Breakdown (Annual)", subtitle_style))
    savings_data = [savings_df.columns.tolist()] + savings_df.values.tolist()
    savings_table = Table(savings_data, colWidths=[doc.width*0.6, doc.width*0.4])
    savings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0077BE")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F0F8FF")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#0077BE"))
    ]))
    elements.append(savings_table)
    elements.append(Spacer(1, 0.5*cm))

    # Add cost per integration table
    elements.append(Paragraph("Cost Per Integration (Annual)", subtitle_style))
    cost_data = [[Paragraph(cell, body_style) for cell in row] for row in [savings_per_integration_df.columns.tolist()] + savings_per_integration_df.values.tolist()]
    cost_table = Table(cost_data, colWidths=[doc.width*0.4, doc.width*0.3, doc.width*0.3])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0077BE")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F0F8FF")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#0077BE"))
    ]))
    elements.append(cost_table)
    elements.append(Spacer(1, 0.5*cm))

    # Add glossary
    elements.append(Paragraph("Glossary", subtitle_style))
    for term, description in hover_descriptions.items():
        elements.append(Paragraph(f"<b>{term}:</b> {description}", body_style))
        elements.append(Spacer(1, 0.1*cm))

    # Add footer
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.drawString(1.5*cm, 0.75*cm, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        canvas.drawRightString(doc.pagesize[0] - 1.5*cm, 0.75*cm, f"Page {canvas.getPageNumber()}")
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content

if __name__ == "__main__":
    main()