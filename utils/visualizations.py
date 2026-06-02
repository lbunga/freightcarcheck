"""Visualization utilities for Streamlit app."""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict


def create_train_layout(cars_df: pd.DataFrame) -> go.Figure:
    """
    Create horizontal train layout visualization.
    Shows 150 cars as horizontal bars, color-coded for hazmat (red) vs safe (green).
    """
    # Prepare data
    colors = ['#d62728' if hazmat else '#2ca02c' for hazmat in cars_df['is_hazmat']]
    
    fig = go.Figure()
    
    # Add train cars as horizontal bars
    for idx, (_, row) in enumerate(cars_df.iterrows()):
        fig.add_trace(go.Scatter(
            x=[idx, idx + 1],
            y=[0, 0],
            mode='lines',
            line=dict(color=colors[idx], width=30),
            hovertemplate=(
                f"<b>Car {row['car_id']}</b><br>"
                f"Type: {row['car_type']}<br>"
                f"Position: {int(row['position'])}/150<br>"
                f"Weight: {row['total_weight_tons']:.1f} tons<br>"
                f"Cargo: {row['cargo_description']}<br>"
                f"Hazmat: {'Yes - Class ' + str(int(row['hazmat_class'])) if row['is_hazmat'] else 'No'}<extra></extra>"
            ),
            showlegend=False,
        ))
    
    fig.update_layout(
        title="Train Layout (150 Cars)",
        xaxis=dict(
            title="Car Position",
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        height=300,
        plot_bgcolor='rgba(240,240,240,0.5)',
        hovermode='closest',
        margin=dict(l=50, r=50, t=80, b=50),
    )
    
    # Add legend indicators
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#d62728', width=15),
        name='Hazmat',
        hoverinfo='skip',
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='#2ca02c', width=15),
        name='Safe Cargo',
        hoverinfo='skip',
    ))
    
    return fig


def create_hazmat_distribution(hazmat_summary: Dict) -> go.Figure:
    """Create bar chart showing hazmat distribution by class."""
    if not hazmat_summary:
        return go.Figure().add_annotation(text="No hazmat cargo")
    
    classes = list(hazmat_summary.keys())
    counts = [hazmat_summary[c]['count'] for c in classes]
    tonnages = [hazmat_summary[c]['tonnage'] for c in classes]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=classes,
        y=counts,
        name='Car Count',
        marker_color='#ff7f0e',
        hovertemplate="<b>%{x}</b><br>Cars: %{y}<extra></extra>",
    ))
    
    fig.update_layout(
        title="Hazmat Distribution by Class",
        xaxis_title="Hazmat Class",
        yaxis_title="Number of Cars",
        height=400,
        showlegend=True,
    )
    
    return fig


def create_tonnage_breakdown(hazmat_tons: float, safe_tons: float) -> go.Figure:
    """Create pie chart showing hazmat vs safe cargo tonnage breakdown."""
    labels = ['Hazmat', 'Safe Cargo']
    values = [hazmat_tons, safe_tons]
    colors = ['#d62728', '#2ca02c']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate="<b>%{label}</b><br>Tonnage: %{value:.1f} tons<br>%: %{percent}<extra></extra>",
    )])
    
    fig.update_layout(
        title=f"Cargo Tonnage Breakdown<br>(Total: {hazmat_tons + safe_tons:.0f} tons)",
        height=400,
    )
    
    return fig


def create_car_type_distribution(cars_df: pd.DataFrame) -> go.Figure:
    """Create bar chart showing distribution of car types."""
    car_counts = cars_df['car_type'].value_counts()
    
    fig = go.Figure(data=[go.Bar(
        x=car_counts.index,
        y=car_counts.values,
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    )])
    
    fig.update_layout(
        title="Train Composition by Car Type",
        xaxis_title="Car Type",
        yaxis_title="Number of Cars",
        height=400,
        showlegend=False,
    )
    
    return fig


def format_cargo_table(cars_df: pd.DataFrame) -> pd.DataFrame:
    """Format dataframe for display in Streamlit table with selected columns."""
    display_df = cars_df[[
        'position',
        'car_id',
        'car_type',
        'total_weight_tons',
        'cargo_description',
        'is_hazmat',
        'hazmat_class',
        'un_code',
        'origin',
        'destination',
    ]].copy()
    
    # Rename columns for better display
    display_df.columns = [
        'Pos',
        'Car ID',
        'Type',
        'Weight (tons)',
        'Cargo',
        'Hazmat',
        'Class',
        'UN Code',
        'Origin',
        'Destination'
    ]
    
    # Format hazmat column
    display_df['Hazmat'] = display_df['Hazmat'].apply(lambda x: 'Yes' if x else 'No')
    
    # Format class column
    display_df['Class'] = display_df['Class'].apply(
        lambda x: f"Class {int(x)}" if pd.notna(x) and x != 'nan' else '-'
    )
    
    # Format position as integer
    display_df['Pos'] = display_df['Pos'].astype(int)
    
    return display_df
