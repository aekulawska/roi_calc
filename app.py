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
        background-color: #ffffff;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #0077BE;
        border-color: #0077BE;
    }
    .stButton>button:hover {
        background-color: #005c91;
        border-color: #005c91;
        color: #ffffff;
    }
    .stButton>button:focus:not(:active) {
        color: #ffffff;
        border-color: #005c91;
        box-shadow: none;
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
    }
    .dataframe {
        width: 100%;
        text-align: left;
        border-collapse: collapse;
    }
    .dataframe th {
        background-color: #0077BE;
        color: white;
        font-weight: bold;
        padding: 10px;
    }
    .dataframe td {
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    .dataframe tr:nth-of-type(even) {
        background-color: #f8f9fa;
    }
    .logo-container {
        text-align: center;
        padding: 10px;
    }
    /* New styles to reduce space */
    .logo-container img {
        margin-bottom: 0;
    }
    h1 {
        margin-top: 0;
        padding-top: 0;
    }
    .streamlit-expanderHeader {
        margin-bottom: 0 !important;
    }
    .stPlotlyChart {
        margin-top: -40px;
    }
    h3 {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Updated styles for spacing */
    .savings-breakdown-header {
        margin-bottom: 20px !important;
    }
    .savings-table {
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add SnapLogic logo
    logo = Image.open("snaplogic_logo.png")
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(logo, width=200)  # Adjust the width as needed
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("ROI Calculator")

    # Create two columns
    left_column, right_column = st.columns(2)

    with left_column:
        # Toggle for default/custom values
        use_default = st.toggle("Use Default Values", value=True)

        # Dictionary of default values
        default_values = {
            "General": {
                "FTE Developer Rate": 45.0,
            },
            "Without SnapLogic": {
                "Months to Onboard": 24,
                "FTE Capacity Used for Onboarding": 20.0,
                "Number of Integrations Built Per Year": 10,
                "Hours to Build An Integration": 200,
                "Number of FTE Supporting Integrations": 10,
                "FTE Capacity Used for Maintenance": 50
            },
            "With SnapLogic": {
                "Months to Onboard": 2,
                "FFTE Capacity Used for Onboarding": 20.0,
                "Number of Integrations Built Per Year": 10,
                "Hours to Build An Integration": 20,
                "Number of FTE Supporting Integrations": 3,
                "FTE Capacity Used for Maintenance": 25
            },
        }

        # Dictionary to store current values
        values = {category: {} for category in default_values}

        # Create input fields for all parameters in separate boxes
        for category, params in default_values.items():
            with st.expander(f"{category}", expanded=True):
                for key, default_value in params.items():
                    # Create a unique key for each input field
                    input_key = f"{category}_{key}"
                    
                    if key == "FTE Developer Rate":
                        values[category][key] = st.number_input(
                            f"{key} (£):",
                            min_value=0.0,
                            value=values[category].get(key, default_value),
                            step=0.01,
                            format="%.2f",
                            disabled=use_default,
                            key=input_key
                        )
                    elif key == "FTE Capacity During Onboarding":
                        values[category][key] = st.number_input(
                            f"{key} (%):",
                            min_value=0.0,
                            max_value=100.0,
                            value=values[category].get(key, default_value),
                            step=0.1,
                            format="%.1f",
                            disabled=use_default,
                            key=input_key
                        ) / 100  # Convert percentage to decimal
                    elif isinstance(default_value, float):
                        values[category][key] = st.number_input(
                            f"{key}:",
                            min_value=0.0,
                            value=values[category].get(key, default_value),
                            step=0.01,
                            format="%.2f",
                            disabled=use_default,
                            key=input_key
                        )
                    else:
                        values[category][key] = st.number_input(
                            f"{key}:",
                            min_value=0,
                            value=values[category].get(key, default_value),
                            step=1,
                            disabled=use_default,
                            key=input_key
                        )

        # Submit button
        submit_button = st.button("Submit")

    with right_column:
        if submit_button:
            display_values = default_values if use_default else values

            try:
                # Calculate OTE FTE Developer
                ote_fte_developer = display_values["General"]["FTE Developer Rate"] * 40 * 52

                # Perform the calculations
                without_snaplogic_time_to_value = (
                    display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"] *
                    display_values["Without SnapLogic"]["FTE Capacity Used for Onboarding"]/100 *
                    (ote_fte_developer *
                     display_values["Without SnapLogic"]["Months to Onboard"] / 12)
                )

                with_snaplogic_time_to_value = (
                    display_values["With SnapLogic"]["Number of FTE Supporting Integrations"] *
                    display_values["With SnapLogic"]["FFTE Capacity Used for Onboarding"]/100 *
                    (ote_fte_developer *
                     display_values["With SnapLogic"]["Months to Onboard"] / 12)
                )

                # Calculate development costs
                without_snaplogic_dev_cost = display_values["Without SnapLogic"]["Number of Integrations Built Per Year"] * display_values["Without SnapLogic"]["Hours to Build An Integration"] * display_values["General"]["FTE Developer Rate"]
                with_snaplogic_dev_cost = display_values["With SnapLogic"]["Number of Integrations Built Per Year"] * display_values["With SnapLogic"]["Hours to Build An Integration"] * display_values["General"]["FTE Developer Rate"]

                # Calculate maintenance costs
                without_snaplogic_maintenance_cost = display_values["Without SnapLogic"]["Number of FTE Supporting Integrations"] * display_values["Without SnapLogic"]["FTE Capacity Used for Maintenance"]/100 * ote_fte_developer
                with_snaplogic_maintenance_cost = display_values["With SnapLogic"]["Number of FTE Supporting Integrations"] * display_values["With SnapLogic"]["FTE Capacity Used for Maintenance"]/100 * ote_fte_developer

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
                           hovertemplate='Time to Value Cost: $%{y:,.0f}<extra></extra>',
                           marker_color='#0077BE'),  # SnapLogic blue
                    go.Bar(name='Maintenance Cost', x=['Without SnapLogic', 'With SnapLogic'], 
                           y=[without_snaplogic_maintenance_cost, with_snaplogic_maintenance_cost],
                           hovertemplate='Maintenance Cost: $%{y:,.0f}<extra></extra>',
                           marker_color='#00A8E8'),  # Lighter blue
                    go.Bar(name='Development Cost', x=['Without SnapLogic', 'With SnapLogic'], 
                           y=[without_snaplogic_dev_cost, with_snaplogic_dev_cost],
                           hovertemplate='Development Cost: $%{y:,.0f}<extra></extra>',
                           marker_color='#F7931E')  # SnapLogic orange
                ])

                fig.update_layout(
                    barmode='stack',
                    yaxis=dict(tickformat='$,.0f', showticklabels=False),  # Hide y-axis labels
                    height=600,
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent surrounding
                    font=dict(color='#333333')  # Dark gray text
                )

                # Display the chart with an even smaller subheader and less space
                st.markdown('<h3>Cost Comparison: Without vs With SnapLogic</h3>', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
             

            except Exception as e:
                st.error(f"An error occurred during calculation: {str(e)}")

if __name__ == "__main__":
    main()
