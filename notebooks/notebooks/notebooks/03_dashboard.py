# Sales Dashboard - Step 3: Interactive Dashboard
# Run this after 02_eda.py
# Open browser at http://127.0.0.1:8050 after running

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ── Load Data ──────────────────────────────────────────────────────────────────
df = pd.read_csv('../data/cleaned/superstore_cleaned.csv', parse_dates=['Order Date'])

# ── App Setup ──────────────────────────────────────────────────────────────────
app = Dash(__name__)
app.title = "Sales Performance Dashboard"

COLORS = {'primary': '#4C72B0', 'success': '#55A868', 'danger': '#C44E52', 'bg': '#F8F9FA'}

# ── Layout ─────────────────────────────────────────────────────────────────────
app.layout = html.Div(style={'backgroundColor': COLORS['bg'], 'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[

    html.H1("📊 Sales Performance Dashboard", style={'textAlign': 'center', 'color': '#2C3E50'}),
    html.P("Business Analyst Portfolio Project | MIS Graduate",
           style={'textAlign': 'center', 'color': '#7F8C8D', 'marginBottom': '30px'}),

    # ── Filters ────────────────────────────────────────────────────────────────
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'flexWrap': 'wrap'}, children=[
        html.Div([
            html.Label("Region", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'All Regions', 'value': 'All'}] +
                        [{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
                value='All', clearable=False
            )
        ], style={'flex': '1', 'minWidth': '150px'}),

        html.Div([
            html.Label("Category", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': 'All Categories', 'value': 'All'}] +
                        [{'label': c, 'value': c} for c in sorted(df['Category'].unique())],
                value='All', clearable=False
            )
        ], style={'flex': '1', 'minWidth': '150px'}),

        html.Div([
            html.Label("Year", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': 'All Years', 'value': 'All'}] +
                        [{'label': str(y), 'value': y} for y in sorted(df['Order Year'].unique())],
                value='All', clearable=False
            )
        ], style={'flex': '1', 'minWidth': '120px'}),
    ]),

    # ── KPI Cards ──────────────────────────────────────────────────────────────
    html.Div(id='kpi-cards', style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px', 'flexWrap': 'wrap'}),

    # ── Charts Row 1 ───────────────────────────────────────────────────────────
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'flexWrap': 'wrap'}, children=[
        html.Div(dcc.Graph(id='sales-trend'),  style={'flex': '2', 'minWidth': '300px', 'background': 'white', 'borderRadius': '8px', 'padding': '10px'}),
        html.Div(dcc.Graph(id='category-bar'), style={'flex': '1', 'minWidth': '250px', 'background': 'white', 'borderRadius': '8px', 'padding': '10px'}),
    ]),

    # ── Charts Row 2 ───────────────────────────────────────────────────────────
    html.Div(style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}, children=[
        html.Div(dcc.Graph(id='region-map'),       style={'flex': '1', 'minWidth': '250px', 'background': 'white', 'borderRadius': '8px', 'padding': '10px'}),
        html.Div(dcc.Graph(id='discount-scatter'), style={'flex': '1', 'minWidth': '250px', 'background': 'white', 'borderRadius': '8px', 'padding': '10px'}),
    ]),
])

# ── Callbacks ──────────────────────────────────────────────────────────────────
@app.callback(
    Output('kpi-cards', 'children'),
    Output('sales-trend', 'figure'),
    Output('category-bar', 'figure'),
    Output('region-map', 'figure'),
    Output('discount-scatter', 'figure'),
    Input('region-filter', 'value'),
    Input('category-filter', 'value'),
    Input('year-filter', 'value'),
)
def update_dashboard(region, category, year):
    dff = df.copy()
    if region   != 'All': dff = dff[dff['Region']     == region]
    if category != 'All': dff = dff[dff['Category']   == category]
    if year     != 'All': dff = dff[dff['Order Year'] == year]

    # KPI Cards
    total_sales   = dff['Sales'].sum()
    total_profit  = dff['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0
    total_orders  = dff['Order ID'].nunique()

    def kpi_card(title, value, color):
        return html.Div([
            html.P(title, style={'margin': '0', 'fontSize': '13px', 'color': '#7F8C8D'}),
            html.H3(value, style={'margin': '4px 0 0', 'color': color}),
        ], style={'background': 'white', 'borderRadius': '8px', 'padding': '16px 20px',
                  'flex': '1', 'minWidth': '140px', 'borderLeft': f'4px solid {color}'})

    kpis = [
        kpi_card("Total Revenue",   f"${total_sales:,.0f}",    COLORS['primary']),
        kpi_card("Total Profit",    f"${total_profit:,.0f}",   COLORS['success']),
        kpi_card("Profit Margin",   f"{profit_margin:.1f}%",   '#8E44AD'),
        kpi_card("Total Orders",    f"{total_orders:,}",       '#E67E22'),
    ]

    # Sales Trend
    monthly = dff.groupby(dff['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)
    fig_trend = px.line(monthly, x='Order Date', y='Sales', title='Monthly Sales Trend',
                        markers=True, color_discrete_sequence=[COLORS['primary']])
    fig_trend.update_layout(margin=dict(t=40, b=20), plot_bgcolor='white')

    # Category Bar
    cat = dff.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
    fig_cat = px.bar(cat, x='Category', y=['Sales', 'Profit'], barmode='group',
                     title='Sales & Profit by Category',
                     color_discrete_map={'Sales': COLORS['primary'], 'Profit': COLORS['success']})
    fig_cat.update_layout(margin=dict(t=40, b=20), plot_bgcolor='white')

    # Region Map
    region_data = dff.groupby('Region')['Sales'].sum().reset_index()
    fig_region = px.bar(region_data, x='Region', y='Sales', title='Sales by Region',
                        color='Sales', color_continuous_scale='Blues')
    fig_region.update_layout(margin=dict(t=40, b=20), plot_bgcolor='white')

    # Discount Scatter
    fig_disc = px.scatter(dff, x='Discount', y='Profit', color='Category',
                          title='Discount vs Profit Impact', opacity=0.4,
                          trendline='lowess')
    fig_disc.add_hline(y=0, line_dash='dash', line_color='red', annotation_text='Break-even')
    fig_disc.update_layout(margin=dict(t=40, b=20), plot_bgcolor='white')

    return kpis, fig_trend, fig_cat, fig_region, fig_disc

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n✅ Dashboard running at: http://127.0.0.1:8050\n")
    app.run(debug=True)
