import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

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
    </style>
    """, unsafe_allow_html=True)

    # Add SnapLogic logo
    logo = Image.open("snaplogic_logo.png")
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo, width=200)  # Adjust the width as needed
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("ROI Calculator")

    # Add description in a compact pretty box spanning both columns
    st.markdown("""
    <div class="description-box">
        <h4>Hi there!</h4>
        <p> Welcome to SnapLogic's ROI calculator. </p>
        <p>Please enter your current customer parameters and the expected improvements with SnapLogic below.</p>
        <p>If you're just getting started, feel free to use the example values to see how the tool works. </p>
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
                "Planned Number of Integrations (Per Year)": 10
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

        # Submit button
        submit_button = st.button("Submit")

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
                without_snaplogic_time_to_value = (
                    display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"] *
                    display_values["Without SnapLogic"]["FTE Capacity Used for Onboarding (%)"]/100 *
                    (ote_fte_developer *
                     display_values["Without SnapLogic"]["Months to Onboard"] / 12)
                )

                with_snaplogic_time_to_value = (
                    with_snaplogic_n_people_supporting_integrations *
                    with_snaplogic_fte_capacity_onboarding/100 *
                    (ote_fte_developer *
                     with_snaplogic_months_to_onboard / 12)
                )

                # Calculate development costs
                without_snaplogic_dev_cost = display_values["Without SnapLogic"]["Planned Number of Integrations (Per Year)"] * display_values["Without SnapLogic"]["Hours to Build An Integration"] * display_values["General"]["FTE Developer Rate"]
                with_snaplogic_dev_cost = display_values["With SnapLogic"]["Planned Number of Integrations (Per Year)"] * with_snaplogic_hours_build_integration * display_values["General"]["FTE Developer Rate"]

                # Calculate maintenance costs
                without_snaplogic_maintenance_cost = display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"] * display_values["Without SnapLogic"]["FTE Capacity Used for Maintenance (%)"]/100 * ote_fte_developer
                with_snaplogic_maintenance_cost = with_snaplogic_n_people_supporting_integrations * with_snaplogic_fte_capacity_maintenance/100 * ote_fte_developer

                # Calculate savings
                time_to_value_savings = without_snaplogic_time_to_value - with_snaplogic_time_to_value
                development_cost_savings = without_snaplogic_dev_cost - with_snaplogic_dev_cost
                maintenance_cost_savings = without_snaplogic_maintenance_cost - with_snaplogic_maintenance_cost
                total_savings = time_to_value_savings + development_cost_savings + maintenance_cost_savings

                # Display the total savings with custom styling and blue box
                st.markdown(f'<div class="total-savings">Total Annual Cost Savings with SnapLogic: ${int(round(total_savings)):,}</div>', unsafe_allow_html=True)

                # Create a dataframe for the savings table
                savings_data = {
                    "Category": ["Time to Value Savings", "Development Cost Savings", "Maintenance Cost Savings"],
                    "Amount": [
                        f"${int(round(time_to_value_savings)):,}",
                        f"${int(round(development_cost_savings)):,}",
                        f"${int(round(maintenance_cost_savings)):,}"
                    ]
                }
                savings_df = pd.DataFrame(savings_data)

                # Display the savings table with more space
                st.markdown('<h3 class="savings-breakdown-header">Savings Breakdown</h3>', unsafe_allow_html=True)
                st.markdown('<div class="savings-table">', unsafe_allow_html=True)
                st.table(savings_df.set_index("Category"))
                st.markdown('</div>', unsafe_allow_html=True)

                # Create interactive stacked bar plot
                fig = go.Figure(data=[
                    go.Bar(name='Time to Value Cost', x=['Without SnapLogic', 'With SnapLogic'], 
                           y=[without_snaplogic_time_to_value, with_snaplogic_time_to_value],
                           marker_color='#0077BE',
                           hovertemplate='Time to Value Cost: $%{y:,.0f}<extra></extra>'),  # SnapLogic blue
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
                st.markdown('<h3>Cost Comparison: Without vs With SnapLogic</h3>', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
             

            except Exception as e:
                st.error(f"An error occurred during calculation: {str(e)}")

if __name__ == "__main__":
    main()