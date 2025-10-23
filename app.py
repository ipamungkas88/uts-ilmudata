from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.utils
import json

app = Flask(__name__)

# Data sanitization function (from GitHub project)
def _sanitize(obj):
    """Recursively convert numpy/pandas objects to plain Python types"""
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    if isinstance(obj, (pd.Series, pd.Index)):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    return obj

def _fig_json(fig: go.Figure) -> str:
    """Convert Plotly figure to JSON string with sanitization"""
    obj = fig.to_plotly_json()
    obj = _sanitize(obj)
    return json.dumps(obj)

def _no_data_fig(title, xaxis_title='', yaxis_title='', height=400):
    """Create a placeholder figure when no data is available"""
    fig = go.Figure()
    fig.add_annotation(
        text="No data available",
        xref="paper", yref="paper",
        x=0.5, y=0.5, xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=20, color="gray")
    )
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        template='plotly_white',
        height=height
    )
    return fig

# Load and preprocess data
def load_and_preprocess_data():
    try:
        data = pd.read_csv('computer_prices_all.csv')
        
        # Remove specified columns if they exist
        columns_to_drop = ['battery_wh', 'charger_watts', 'psu_watts']
        existing_columns = [col for col in columns_to_drop if col in data.columns]
        if existing_columns:
            data.drop(existing_columns, axis=1, inplace=True)
        
        # Create performance score
        data['performance_score'] = (data['cpu_tier'] + data['gpu_tier'] + 
                                   data['cpu_cores']/4 + data['vram_gb']/2 + 
                                   data['ram_gb']/8) * data['cpu_boost_ghz']
        
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Load data
data = load_and_preprocess_data()

def get_descriptive_statistics():
    """Generate descriptive statistics for all columns like in cell 7"""
    if data is None:
        return {}
    
    stats = {}
    
    # Get categorical columns
    categorical_cols = ['device_type', 'brand', 'model', 'os', 'form_factor', 'cpu_brand', 
                       'cpu_model', 'gpu_brand', 'gpu_model', 'storage_type', 'display_type', 
                       'resolution', 'wifi']
    
    # Get numerical columns  
    numerical_cols = ['release_year', 'cpu_tier', 'cpu_cores', 'cpu_threads', 'cpu_base_ghz', 
                     'cpu_boost_ghz', 'gpu_tier', 'vram_gb', 'ram_gb', 'storage_gb', 
                     'storage_drive_count', 'display_size_in', 'refresh_hz', 'bluetooth', 
                     'weight_kg', 'warranty_months', 'price', 'performance_score']
    
    # Process categorical columns
    for col in categorical_cols:
        if col in data.columns:
            desc = data[col].describe()
            counts = data[col].value_counts()
            
            stats[col] = {
                'type': 'categorical',
                'describe': desc.to_dict(),
                'value_counts': counts.head(10).to_dict(),  # Top 10 values
                'total_unique': len(counts)
            }
    
    # Process numerical columns
    for col in numerical_cols:
        if col in data.columns:
            desc = data[col].describe()
            
            stats[col] = {
                'type': 'numerical',
                'describe': desc.to_dict(),
                'quartiles': {
                    'Q1': data[col].quantile(0.25),
                    'Q2': data[col].quantile(0.5),
                    'Q3': data[col].quantile(0.75)
                }
            }
    
    return stats

def create_plotly_charts():
    """Create all visualizations using Plotly Graph Objects for better control and consistency"""
    
    if data is None:
        return {}
    
    charts = {}
    
    try:
        # 1. Scatter Plot: Price vs Performance Score
        sample_data = data.sample(n=min(2000, len(data)), random_state=42)  # Sample for performance
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=sample_data['performance_score'].tolist(),
            y=sample_data['price'].tolist(),
            mode='markers',
            marker=dict(color='#667eea', size=6, opacity=0.6),
            name='Price vs Performance'
        ))
        
        fig1.update_layout(
            title={
                'text': 'Price vs Performance Score',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            xaxis_title='Performance Score',
            yaxis_title='Price ($)',
            template='plotly_white',
            autosize=True,
            height=500,  # Larger height
            width=None,
            margin=dict(l=90, r=60, t=120, b=90),  # More generous margins
            font=dict(size=12, family='Arial, sans-serif'),
            showlegend=False,
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white'
        )
        charts['scatter_price_performance'] = _fig_json(fig1)
        
        # 2. Bar Chart: Top 10 Brands by Average Price
        avg_price_by_brand = data.groupby('brand', observed=True)['price'].mean().sort_values(ascending=False).head(10)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=avg_price_by_brand.index.tolist(),
            y=avg_price_by_brand.values.tolist(),
            marker_color='#667eea',
            text=[f'${val:.0f}' for val in avg_price_by_brand.values],
            textposition='outside'
        ))
        
        fig2.update_layout(
            title={
                'text': 'Top 10 Brands with Highest Average Price',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            xaxis_title='Brand',
            yaxis_title='Average Price ($)',
            template='plotly_white',
            autosize=True,
            height=500,
            margin=dict(l=90, r=60, t=120, b=120),  # Extra space for labels
            showlegend=False,
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family='Arial, sans-serif')
        )
        fig2.update_xaxes(tickangle=-35, tickfont=dict(size=11))  # Better angle for readability
        charts['bar_top_brands'] = _fig_json(fig2)
        
        # 3. Box Plot: Price Distribution by OS
        os_list = data['os'].value_counts().head(8).index.tolist()  # Top 8 OS for clarity
        filtered_data = data[data['os'].isin(os_list)]
        
        fig3 = go.Figure()
        for os_name in os_list:
            os_data = filtered_data[filtered_data['os'] == os_name]['price']
            fig3.add_trace(go.Box(
                y=os_data.tolist(),
                name=os_name,
                boxpoints='outliers'
            ))
        
        fig3.update_layout(
            title={
                'text': 'Price Distribution by Operating System',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            xaxis_title='Operating System',
            yaxis_title='Price ($)',
            template='plotly_white',
            autosize=True,
            height=500,
            margin=dict(l=90, r=60, t=120, b=100),
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family='Arial, sans-serif')
        )
        charts['box_price_os'] = _fig_json(fig3)
        
        # 4. Histogram: Price Distribution
        fig4 = go.Figure()
        fig4.add_trace(go.Histogram(
            x=data['price'].tolist(),
            nbinsx=50,
            marker_color='#667eea',
            name='Price Distribution'
        ))
        
        fig4.update_layout(
            title={
                'text': 'Price Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            xaxis_title='Price ($)',
            yaxis_title='Frequency',
            template='plotly_white',
            autosize=True,
            height=500,
            margin=dict(l=90, r=60, t=120, b=90),
            showlegend=False,
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family='Arial, sans-serif')
        )
        charts['hist_price'] = _fig_json(fig4)
        
        # 5. Pie Chart: Device Type Distribution
        device_counts = data['device_type'].value_counts()
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
        
        fig5 = go.Figure()
        fig5.add_trace(go.Pie(
            labels=device_counts.index.tolist(),
            values=device_counts.values.tolist(),
            hole=0.35,
            marker_colors=colors[:len(device_counts)],
            textinfo='label+percent+value',
            hovertemplate='%{label}<br>Count: %{value}<br>% of total: %{percent}<extra></extra>'
        ))
        
        fig5.update_layout(
            title={
                'text': 'Distribution of Device Types',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            template='plotly_white',
            autosize=True,
            height=500,
            margin=dict(l=60, r=60, t=120, b=80),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, family='Arial, sans-serif')
        )
        charts['pie_device_type'] = _fig_json(fig5)
        
        # 6. Heatmap: Correlation Matrix
        numeric_cols = ['price', 'performance_score', 'cpu_cores', 'cpu_threads', 'ram_gb', 
                       'storage_gb', 'vram_gb', 'cpu_base_ghz', 'cpu_boost_ghz', 'release_year']
        
        available_cols = [col for col in numeric_cols if col in data.columns]
        corr_matrix = data[available_cols].corr().round(3)
        
        fig6 = go.Figure()
        fig6.add_trace(go.Heatmap(
            z=corr_matrix.values.tolist(),
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={'size': 10},
            hoverongaps=False
        ))
        
        fig6.update_layout(
            title={
                'text': 'Correlation Matrix of Numeric Variables',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            template='plotly_white',
            autosize=True,
            height=600,  # Taller for heatmap readability
            margin=dict(l=100, r=60, t=120, b=100),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=11, family='Arial, sans-serif')
        )
        charts['heatmap_correlation'] = _fig_json(fig6)
        
        # 7. Bar Chart: Average Price by CPU Brand
        cpu_brand_data = data.groupby('cpu_brand', observed=True)['price'].mean().sort_values(ascending=False)
        
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            x=cpu_brand_data.index.tolist(),
            y=cpu_brand_data.values.tolist(),
            marker_color='#764ba2',
            text=[f'${val:.0f}' for val in cpu_brand_data.values],
            textposition='outside'
        ))
        
        fig7.update_layout(
            title={
                'text': 'Average Price by CPU Brand',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            xaxis_title='CPU Brand',
            yaxis_title='Average Price ($)',
            template='plotly_white',
            autosize=True,
            height=500,
            margin=dict(l=90, r=60, t=120, b=90),
            showlegend=False,
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family='Arial, sans-serif')
        )
        charts['bar_cpu_brand'] = _fig_json(fig7)
        
        # 8. Line Chart: Price Trend by Release Year
        yearly_stats = data.groupby('release_year', observed=True).agg({
            'price': ['mean', 'count']
        }).round(2)
        yearly_stats.columns = ['avg_price', 'count']
        yearly_stats = yearly_stats.reset_index()
        
        # Filter years with reasonable data
        yearly_stats = yearly_stats[yearly_stats['count'] >= 10]
        
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(
            x=yearly_stats['release_year'].tolist(),
            y=yearly_stats['avg_price'].tolist(),
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(color='#667eea', size=8),
            name='Average Price'
        ))
        
        fig8.update_layout(
            title={
                'text': 'Average Price Trend by Release Year',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            xaxis_title='Release Year',
            yaxis_title='Average Price ($)',
            template='plotly_white',
            autosize=True,
            height=500,
            margin=dict(l=90, r=60, t=120, b=90),
            showlegend=False,
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family='Arial, sans-serif')
        )
        charts['line_price_trend'] = _fig_json(fig8)
        
        # 9. Stacked Bar Chart: GPU Brand by Device Type
        gpu_brands = data['gpu_brand'].value_counts().head(5).index.tolist()  # Top 5 GPU brands
        device_types = data['device_type'].value_counts().index.tolist()
        
        fig9 = go.Figure()
        colors_gpu = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        
        for i, gpu in enumerate(gpu_brands):
            gpu_data = []
            for device in device_types:
                count = len(data[(data['device_type'] == device) & (data['gpu_brand'] == gpu)])
                total_device = len(data[data['device_type'] == device])
                percentage = (count / total_device * 100) if total_device > 0 else 0
                gpu_data.append(percentage)
            
            fig9.add_trace(go.Bar(
                name=gpu,
                x=device_types,
                y=gpu_data,
                marker_color=colors_gpu[i]
            ))
        
        fig9.update_layout(
            title={
                'text': 'GPU Brand Composition by Device Type (%)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif', 'weight': 700}
            },
            xaxis_title='Device Type',
            yaxis_title='Percentage (%)',
            barmode='stack',
            template='plotly_white',
            autosize=True,
            height=500,
            margin=dict(l=90, r=60, t=120, b=90),
            plot_bgcolor='rgba(248, 249, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family='Arial, sans-serif'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )
        charts['stacked_gpu_device'] = _fig_json(fig9)
        
    except Exception as e:
        print(f"Error creating charts: {e}")
        return {}
    
    return charts

@app.route('/')
def index():
    """Main page - redirect to statistics"""
    return render_template('statistics.html')

@app.route('/statistics')
def statistics():
    """Page 1: Descriptive Statistics"""
    return render_template('statistics.html')

@app.route('/charts')
def charts():
    """Page 2: Data Visualizations"""
    return render_template('charts.html')

@app.route('/api/statistics')
def get_statistics_api():
    """API endpoint to get descriptive statistics"""
    try:
        stats = get_descriptive_statistics()
        return jsonify(stats)
    except Exception as e:
        print(f"Error in get_statistics_api: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/charts')
def get_charts():
    """API endpoint to get all chart data"""
    try:
        charts = create_plotly_charts()
        if not charts:
            return jsonify({"error": "No charts available"}), 500
        return jsonify(charts)
    except Exception as e:
        print(f"Error in get_charts: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/summary')
def get_summary():
    """API endpoint to get basic summary statistics"""
    try:
        if data is None:
            return jsonify({"error": "Data not available"}), 500
            
        summary_data = {
            'total_devices': len(data),
            'avg_price': round(data['price'].mean(), 2),
            'median_price': round(data['price'].median(), 2),
            'min_price': round(data['price'].min(), 2),
            'max_price': round(data['price'].max(), 2),
            'total_brands': data['brand'].nunique(),
            'total_models': data['model'].nunique(),
            'device_types': data['device_type'].value_counts().to_dict(),
            'operating_systems': data['os'].value_counts().to_dict(),
        }
        return jsonify(summary_data)
    except Exception as e:
        print(f"Error in get_summary: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "data_loaded": data is not None})

if __name__ == '__main__':
    print("Starting Flask application...")
    if data is not None:
        print(f"Data loaded successfully with {len(data)} records")
    else:
        print("Warning: Data could not be loaded")
    
    app.run(debug=True, host='127.0.0.1', port=5001)