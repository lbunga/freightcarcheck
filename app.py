"""FreightcarchecK - Heavy Haul Manifest Viewer
Main Streamlit application for viewing freight train manifests.
"""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
import sys

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.data_loader import load_sample_trains, trains_json_to_dataframe
from utils.calculations import (
    calculate_total_tonnage,
    calculate_hazmat_tonnage,
    get_weight_distribution,
    calculate_braking_ratio,
    get_hazmat_summary,
)
from utils.filters import apply_filters
from utils.visualizations import (
    create_train_layout,
    create_hazmat_distribution,
    create_tonnage_breakdown,
    create_car_type_distribution,
    format_cargo_table,
)


# Page configuration
st.set_page_config(
    page_title="FreightcarchecK",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🚂 FreightcarchecK")
st.markdown("## Heavy Haul Manifest Viewer - Emergency Response Support")
st.markdown("""
**For Train Crews, First Responders, and Safety Teams**

Instantly access train composition, locate hazardous materials, calculate tonnage, and identify critical safety metrics during emergencies.
""")

# Sidebar
st.sidebar.header("Train Selection")

# Load sample trains
@st.cache_data
def load_trains():
    trains = load_sample_trains('data')
    if not trains:
        # Generate sample data if not exists
        try:
            import data_generator
            trains = data_generator.generate_sample_trains(3)
            # Save for next load
            Path('data').mkdir(exist_ok=True)
            with open('data/sample_trains.json', 'w') as f:
                json.dump(trains, f, indent=2)
        except Exception as e:
            st.error(f"Error generating sample data: {e}")
            return []
    return trains


trains = load_trains()

if not trains:
    st.error("❌ No train data available. Please generate sample trains first.")
    st.stop()

# Train selector
train_options = {train['train_id']: idx for idx, train in enumerate(trains)}
selected_train_id = st.sidebar.selectbox(
    "Select Train",
    options=list(train_options.keys()),
)

# Load selected train data
selected_train = trains[train_options[selected_train_id]]
cars_df = trains_json_to_dataframe([selected_train])

# Calculate metrics once
total_tonnage = calculate_total_tonnage(cars_df)
hazmat_tonnage = calculate_hazmat_tonnage(cars_df)
safe_tonnage = total_tonnage - hazmat_tonnage
hazmat_count = cars_df['is_hazmat'].sum()
braking_ratio = calculate_braking_ratio(hazmat_tonnage, total_tonnage)
weight_dist = get_weight_distribution(cars_df)
hazmat_summary = get_hazmat_summary(cars_df)

st.sidebar.markdown("---")
st.sidebar.subheader("Quick Stats")
st.sidebar.metric("Total Cars", len(cars_df))
st.sidebar.metric("Total Weight", f"{total_tonnage:.0f} tons")
st.sidebar.metric("Hazmat Cars", int(hazmat_count))
st.sidebar.metric("Braking Ratio", f"{braking_ratio:.2%}")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 Manifest Table", "🚃 Train Layout"])

# ===== TAB 1: DASHBOARD =====
with tab1:
    st.header(f"Train {selected_train_id} - Dashboard")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Cars",
            len(cars_df),
            delta="cars",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Total Weight",
            f"{total_tonnage:.0f}",
            delta="tons",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "Hazmat Cars",
            int(hazmat_count),
            delta=f"{(hazmat_count/len(cars_df)*100):.1f}%",
        )
    
    with col4:
        st.metric(
            "Braking Ratio",
            f"{braking_ratio:.3f}",
            delta="hazmat/total",
            delta_color="off"
        )
    
    st.markdown("---")
    
    # Weight breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cargo Tonnage Breakdown")
        fig_tonnage = create_tonnage_breakdown(hazmat_tonnage, safe_tonnage)
        st.plotly_chart(fig_tonnage, use_container_width=True)
    
    with col2:
        st.subheader("Weight Distribution")
        dist_data = pd.DataFrame({
            'Section': ['Front (1-50)', 'Middle (51-100)', 'Rear (101-150)'],
            'Percentage': [weight_dist['front'], weight_dist['middle'], weight_dist['rear']]
        })
        st.bar_chart(dist_data.set_index('Section'))
    
    st.markdown("---")
    
    # Hazmat summary table
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hazmat Summary by Class")
        if hazmat_summary:
            hazmat_df = pd.DataFrame([
                {
                    'Hazmat Class': key,
                    'Car Count': value['count'],
                    'Total Tonnage': value['tonnage']
                }
                for key, value in hazmat_summary.items()
            ])
            st.dataframe(hazmat_df, use_container_width=True)
        else:
            st.info("No hazmat cargo detected on this train.")
    
    with col2:
        st.subheader("Car Type Distribution")
        fig_car_types = create_car_type_distribution(cars_df)
        st.plotly_chart(fig_car_types, use_container_width=True)


# ===== TAB 2: MANIFEST TABLE =====
with tab2:
    st.header(f"Train {selected_train_id} - Manifest")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_term = st.text_input("Search", placeholder="Car ID, cargo, origin, destination...")
    
    with col2:
        hazmat_only = st.checkbox("Hazmat Only")
    
    with col3:
        car_types = st.multiselect(
            "Car Types",
            options=sorted(cars_df['car_type'].unique()),
            default=None
        )
    
    with col4:
        hazmat_classes = st.multiselect(
            "Hazmat Classes",
            options=sorted([int(c) for c in cars_df[cars_df['is_hazmat']]['hazmat_class'].dropna().unique()]),
            default=None
        )
    
    # Apply filters
    filtered_df = apply_filters(
        cars_df,
        search_term=search_term if search_term else None,
        hazmat_only=hazmat_only,
        hazmat_classes=hazmat_classes if hazmat_classes else None,
        car_types=car_types if car_types else None,
    )
    
    st.markdown(f"**Showing {len(filtered_df)} of {len(cars_df)} cars**")
    
    # Format and display table
    display_df = format_cargo_table(filtered_df)
    
    # Color-code rows
    def color_hazmat_rows(row):
        if row['Hazmat'] == 'Yes':
            return ['background-color: #ffcccc'] * len(row)
        else:
            return ['background-color: #ccffcc'] * len(row)
    
    st.dataframe(
        display_df.style.apply(color_hazmat_rows, axis=1),
        use_container_width=True,
        height=600
    )


# ===== TAB 3: TRAIN LAYOUT =====
with tab3:
    st.header(f"Train {selected_train_id} - Visual Layout")
    
    st.markdown("""
    **Legend:**
    - 🔴 Red = Hazmat Cargo
    - 🟢 Green = Safe Cargo
    
    Hover over cars to see details.
    """)
    
    # Create and display train layout
    fig_layout = create_train_layout(cars_df)
    st.plotly_chart(fig_layout, use_container_width=True)
    
    st.markdown("---")
    
    # Hazmat distribution chart
    if hazmat_summary:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Hazmat by Class (Visual)")
            fig_hazmat = create_hazmat_distribution(hazmat_summary)
            st.plotly_chart(fig_hazmat, use_container_width=True)
        
        with col2:
            st.subheader("Hazmat Details")
            for hazmat_class, data in hazmat_summary.items():
                st.write(f"**{hazmat_class}**: {data['count']} cars, {data['tonnage']} tons")
    else:
        st.info("No hazmat cargo on this train.")


# Footer
st.markdown("---")
st.markdown("""
**FreightcarchecK v1.0** | Heavy Haul Manifest Viewer
- Built for train crews, conductors, and first responders
- Emergency response support during derailments, incidents, and safety audits
- For POC validation with static sample data
""")
