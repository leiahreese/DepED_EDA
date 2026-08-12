from dash import Dash, html, dcc, Input, Output, State, ctx
import plotly.express as px
import pandas as pd
import base64
import io


def initial_dataset(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skiprows=4)

    df = df.fillna('Not Applicable')

    # Clean column names:
    df.columns = (
        df.columns
        .str.replace('-', '', regex=False)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

    return df

# Styling
COLORS = {
    'background': '#f5f5f7',
    'white': '#ffffff',
    'primary': '#0071e3',  # Apple blue
    'secondary': '#f56300',  # Orange
    'accent': '#6e6e73',  # Dark gray
    'text': '#1d1d1f',
    'border': '#d2d2d7',
    'success': '#34c759',  # Green
    'warning': '#ff9500',  # Orange/amber
    'error': '#ff3b30',  # Red
    'purple': '#af52de',
    'light_gray': '#f2f2f2',
    
    # Colors for the metric cards
    'blue': '#0071e3',  # Male card
    'pink': '#ff375f',  # Female card
    'teal': '#64d2ff',  # Total enrollees
    'green': '#30b247'  # Total schools
}

# Component styles
header_style = {
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'space-between',
    'padding': '16px 24px',
    'backgroundColor': COLORS['white'],
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'borderRadius': '12px',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
}

header_text_style = {
    'marginLeft': '14px',
    'fontWeight': 'normal',
    'color': COLORS['text'],
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

upload_container_style = {
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'space-between',
    'marginBottom': '16px',
    'backgroundColor': COLORS['white'],
    'padding': '14px 24px',
    'borderRadius': '12px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
}

# Base metric card style
metric_card_style = {
    'backgroundColor': COLORS['white'],
    'padding': '14px',
    'borderRadius': '10px',
    'flex': '1',
    'minWidth': '180px',
    'textAlign': 'center',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'alignItems': 'center',
    'transition': 'all 0.2s ease',
    'height':'60px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
}

# Different styled metric cards
male_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

female_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

total_enrollees_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

total_schools_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

# Styled metric numbers based on card
male_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color': '#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

female_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color':'#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

total_enrollees_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color': '#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

total_schools_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color': '#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

metric_label_style = {
    'fontSize': '14px',
    'color': COLORS['accent'],
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'fontWeight': '500'
}

chart_container_style = {
    'backgroundColor': COLORS['white'],
    'borderRadius': '12px',
    'padding': '16px 20px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'width': '100%'
}

status_box_style = {
    'padding': '8px 14px',
    'backgroundColor': COLORS['purple'],
    'color': COLORS['white'],
    'borderRadius': '8px',
    'fontSize': '13px',
    'opacity': '0.9',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'fontWeight': '500'
}

filters_container_style = {
    'width': '16%',
    'padding': '16px 20px',
    'backgroundColor': COLORS['white'],
    'borderRadius': '12px',
    'marginRight': '5px',
    'color': COLORS['text'],
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'height': 'fit-content',
    'alignSelf': 'flex-start',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

button_style = {
    'padding': '10px 16px',
    'border': 'none',
    'borderRadius': '8px',
    'cursor': 'pointer',
    'fontSize': '14px',
    'fontWeight': '500',
    'outline': 'none',
    'textTransform': 'none',
    'height': '40px',
    'margin': '0 10px 0 0',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'transition': 'all 0.2s ease'
}

primary_button_style = {
    **button_style,
    'backgroundColor': '#0038a8',
    'color': 'white',
}

danger_button_style = {
    **button_style,
    'backgroundColor': '#c81323',
    'color': 'white',
}

filter_button_style = {
    **button_style,
    'backgroundColor': '#616867',
    'color': 'white',
    'marginBottom': '16px',
    'width': '100%',
}

filter_label_style = {
    'fontWeight': '600',
    'marginBottom': '4px',
    'marginTop': '10px',
    'fontSize': '13px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'color': COLORS['text']
}

dropdown_style = {
    'marginBottom': '10px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'borderRadius': '8px'
}

chart_heading_style = {
    'fontSize': '16px',
    'fontWeight': '700',
    'margin': '0 0 10px 0',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'color': COLORS['text']
}

# Enhanced styles for chart sections
enrollment_chart_style = {
    'backgroundColor': COLORS['white'],
    'borderRadius': '12px',
    'padding': '16px 20px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'height': '275px'  
}

level_chart_style = {
    'backgroundColor': COLORS['white'],
    'borderRadius': '12px',
    'padding': '16px 20px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'width': '100%',
    'height': '275px'  
}

app = Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='stored-data'),

    # Header with Logo
    html.Div([
        # Left side with logo and title
        html.Div([
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Seal_of_the_Department_of_Education_of_the_Philippines.png',
                style={'height': '50px'}
            ),
            html.Div([
                html.H1("Department of Education",
                        style={'fontSize': '22px', 'margin': '0', 'marginBottom': '2px', 'fontWeight': '600'}),
                html.H2("School Enrollment Dashboard",
                        style={'fontSize': '14px', 'margin': '0', 'fontWeight': '400', 'color': COLORS['accent']})
            ], style=header_text_style)
        ], style={'display': 'flex', 'alignItems': 'center'}),

        # Right side status
        html.Div(id='header-status', style={'color': COLORS['accent'], 'fontSize': '13px'})
    ], style=header_style),

    # Upload Controls
    html.Div([
        html.Div([
            dcc.Upload(
                id='upload-dataset',
                children=html.Button('Upload Data', style=primary_button_style),
                multiple=False
            ),
            html.Button('Clear Data', id='clear-btn', style=danger_button_style),
            
            html.Div(id='output-upload')

        ], style={'display': 'flex', 'alignItems': 'center'}),
    ], style=upload_container_style),

    # Main Content Area
    html.Div([
        # Left: Filters
        html.Div([
            html.Button("Clear Filter", id="clear_btn", style=filter_button_style),

            html.Label("Region", style=filter_label_style),
            dcc.Dropdown(id="region_dd", placeholder="Select Region(s)", multi=True,
                         style=dropdown_style),

            html.Label("Province", style=filter_label_style),
            dcc.Dropdown(id="province_dd", placeholder="Select Province(s)", multi=True,
                         style=dropdown_style),

            html.Label("Division", style=filter_label_style),
            dcc.Dropdown(id="division_dd", placeholder="Select Division(s)", multi=True,
                         style=dropdown_style),

            html.Label("District", style=filter_label_style),
            dcc.Dropdown(id="district_dd", placeholder="Select District(s)", multi=True,
                         style=dropdown_style),

            html.Label("Municipality", style=filter_label_style),
            dcc.Dropdown(id="municipality_dd", placeholder="Select Municipality(s)", multi=True,
                         style=dropdown_style),

            html.Label("Legislative District", style=filter_label_style),
            dcc.Dropdown(id="legislative_district_dd", placeholder="Select Legislative District(s)", multi=True,
                         style=dropdown_style),

            html.Label("Sector", style=filter_label_style),
            dcc.Dropdown(id="sector_dd", placeholder="Select Sector(s)", multi=True,
                         style=dropdown_style),

            html.Label("School Type", style=filter_label_style),
            dcc.Dropdown(id="school_type_dd", placeholder="Select School Type(s)", multi=True,
                         style=dropdown_style),

            html.Label("Modified COC", style=filter_label_style),
            dcc.Dropdown(id="modified_coc_dd", placeholder="Select Modified COC(s)", multi=True,
                         style=dropdown_style),

            html.Label("Subclass", style=filter_label_style),
            dcc.Dropdown(id="school_subclass_dd", placeholder="Select Subclass(s)", multi=True,
                         style=dropdown_style),
        ], style=filters_container_style),

        # Right: Metrics & Charts
        html.Div([
            # Top row metrics
            html.Div([
                html.Div([
                    html.Div(id="male_summary_card", style=male_number_style),
                    html.Div(style=metric_label_style)
                ], style=male_card_style),

                html.Div([
                    html.Div(id="female_summary_card", style=female_number_style),
                    html.Div(style=metric_label_style)
                ], style=female_card_style),

                html.Div([
                    html.Div(id="total_summary_card", style=total_enrollees_number_style),
                    html.Div(style=metric_label_style)
                ], style=total_enrollees_card_style),

                html.Div([
                    html.Div(id="total_school_card", style=total_schools_number_style),
                    html.Div(style=metric_label_style)
                ], style=total_schools_card_style),
            ], style={
                'display': 'flex',
                'gap': '15px',
                'marginBottom': '16px',
                'justifyContent': 'space-between',
                'width': '100%'
            }),

            # Wrap both charts in a flex container
            html.Div([
                html.Div([
                    html.H3("Educational Level Comparison", style=chart_heading_style),
                    dcc.Graph(
                        id="education_bar_chart",
                        style={"height": "250px", "width": "100%"},
                        config={'displayModeBar': False}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),

                html.Div([
                    html.H3("Average Student Count per Grade Level", style=chart_heading_style),
                    dcc.Graph(
                        id="enrollment_rate_chart",
                        style={"height": "250px", "width": "100%"},
                        config={'displayModeBar': False}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),


                html.Div([
                    html.H3("Average Student Count per Track", style=chart_heading_style),
                    dcc.Graph(
                        id="tracks_rate_chart",
                        style={"height": "250px", "width": "100%"},
                        config={'displayModeBar': False}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),



            ], style={"display": "flex", "gap": "15px"}),

            # School Level Charts in a row layout for better comparison
            html.Div([
                # Elementary Level
                html.Div([
                    html.H3("Elementary Level", style=chart_heading_style),
                    dcc.Graph(
                        id="elementary_bar_chart",
                        config={'displayModeBar': False},
                        style={"height": "250px", "width": "100%"}
                    )
                ], style={**level_chart_style, "flex": "1"}),

                # Junior High School
                html.Div([
                    html.H3("Junior High School", style=chart_heading_style),
                    dcc.Graph(
                        id="jhs_bar_chart",
                        config={'displayModeBar': False},
                        style={"height": "250px", "width": "100%"}
                    )
                ], style={**level_chart_style, "flex": "1"}),

                # Senior High School
                html.Div([
                    html.H3("Senior High School", style=chart_heading_style),
                    dcc.Graph(
                        id="shs_bar_chart",
                        config={'displayModeBar': False},
                        style={"height": "250px", "width": "100%"}
                    )
                ], style={**level_chart_style, "flex": "1"}),
            ], style={'display': 'flex', "gap": "15px"})

        ], style={'flex': '1', 'width': '75%'}),


    ], style={'display': 'flex', 'gap': '15px', 'width': '100%'}),

# wrapping up layouts
], style={
    'width': '100%',
    'maxWidth': '1440px',
    'margin': '0 auto',
    'padding': '20px',
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'boxSizing': 'border-box'
})


# Callback: Upload or Clear File
@app.callback(
    Output('output-upload', 'children'),
    Output('stored-data', 'data'),
    Input('upload-dataset', 'contents'),
    Input('clear-btn', 'n_clicks'),
    State('upload-dataset', 'filename')
)
def handle_upload_or_clear(contents, clear_clicks, filename):
    triggered_id = ctx.triggered_id
    if triggered_id == 'clear-btn':
        return "Upload cleared. Please upload a new file.", None
    if contents is None:
        return "No file uploaded yet.", None

    try:
        df = initial_dataset(contents)
        return f"Uploaded: {filename}", df.to_dict('records')
    except Exception as e:
        return f"Error reading file: {e}", None


# Callback: Populate Dropdown filters based on previous selections
@app.callback(
    Output('region_dd', 'options'),
    Output('province_dd', 'options'),
    Output('district_dd', 'options'),
    Output('division_dd', 'options'),
    Output('municipality_dd', 'options'),
    Output('legislative_district_dd', 'options'),
    Output('sector_dd', 'options'),
    Output('school_type_dd', 'options'),
    Output('modified_coc_dd', 'options'),
    Output('school_subclass_dd', 'options'),

    Input('stored-data', 'data'),
    Input('region_dd', 'value'),
    Input('province_dd', 'value'),
    Input('district_dd', 'value'),
    Input('division_dd', 'value'),
    Input('municipality_dd', 'value'),
    Input('legislative_district_dd', 'value'),
    Input('sector_dd', 'value'),
    Input('school_type_dd', 'value'),
    Input('modified_coc_dd', 'value'),
)

def update_dropdown_options(data, region, province, district, division, municipality,
                            legislative_district, sector, school_type, modified_coc):
    if data is None:
        return ([],) * 10

    df = pd.DataFrame(data)

    # Region Options (use full data)
    region_options = [{'label': r, 'value': r} for r in sorted(df['Region'].dropna().unique())]

    # Province Options (filter only by region)
    province_df = df[df['Region'].isin(region)] if region else df
    province_options = [{'label': p, 'value': p} for p in sorted(province_df['Province'].dropna().unique())]

    # District Options (filter by region and province)
    district_df = province_df[province_df['Province'].isin(province)] if province else province_df
    district_options = [{'label': d, 'value': d} for d in sorted(district_df['District'].dropna().unique())]

    # Division Options (filter by region, province, and district)
    division_df = district_df[district_df['District'].isin(district)] if district else district_df
    division_options = [{'label': d, 'value': d} for d in sorted(division_df['Division'].dropna().unique())]

    # Municipality Options (filter by region, province, district, division)
    municipality_df = division_df[division_df['Division'].isin(division)] if division else division_df
    municipality_options = [{'label': m, 'value': m} for m in sorted(municipality_df['Municipality'].dropna().unique())]

    # Legislative District Options
    legislative_district_df = municipality_df[municipality_df['Municipality'].isin(municipality)] if municipality else municipality_df
    legislative_district_options = [{'label': l, 'value': l} for l in sorted(legislative_district_df['Legislative District'].dropna().unique())]

    # Sector Options
    sector_df = legislative_district_df[legislative_district_df['Legislative District'].isin(legislative_district)] if legislative_district else legislative_district_df
    sector_options = [{'label': s, 'value': s} for s in sorted(sector_df['Sector'].dropna().unique())]

    # School Type Options
    school_type_df = sector_df[sector_df['Sector'].isin(sector)] if sector else sector_df
    school_type_options = [{'label': s, 'value': s} for s in sorted(school_type_df['School Type'].dropna().unique())]

    # Modified COC Options
    modified_coc_df = school_type_df[school_type_df['School Type'].isin(school_type)] if school_type else school_type_df
    modified_coc_options = [{'label': m, 'value': m} for m in sorted(modified_coc_df['Modified COC'].dropna().unique())]

    # Subclass Options
    school_subclass_df = modified_coc_df[modified_coc_df['Modified COC'].isin(modified_coc)] if modified_coc else modified_coc_df
    school_subclass_options = [{'label': s, 'value': s} for s in sorted(school_subclass_df['School Subclassification'].dropna().unique())]

    return (region_options, province_options, district_options, division_options,
            municipality_options, legislative_district_options, sector_options,
            school_type_options, modified_coc_options, school_subclass_options)


# clear filter
@app.callback(
    Output('region_dd', 'value'),
    Output('province_dd', 'value'),
    Output('district_dd', 'value'),
    Output('division_dd', 'value'),
    Output('municipality_dd', 'value'),
    Output('legislative_district_dd', 'value'),
    Output('sector_dd', 'value'),
    Output('school_type_dd', 'value'),
    Output('modified_coc_dd', 'value'),
    Output('school_subclass_dd', 'value'),
    Input('clear_btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_all_dropdowns(n_clicks):
    return ([],) * 10


elementary_male = [
    'K Male', 'G1 Male', 'G2 Male', 'G3 Male', 'G4 Male', 'G5 Male', 'G6 Male', 'Elem NG Male'
]
elementary_female = [
    'K Female', 'G1 Female', 'G2 Female', 'G3 Female', 'G4 Female', 'G5 Female', 'G6 Female', 'Elem NG Female'
]

junior_male = [
    'G7 Male', 'G8 Male', 'G9 Male', 'G10 Male', 'JHS NG Male'
]
junior_female = [
    'G7 Female', 'G8 Female', 'G9 Female', 'G10 Female', 'JHS NG Female'
]

senior_male = [
    'G11 ACAD ABM Male', 'G11 ACAD HUMSS Male', 'G11 ACAD STEM Male', 'G11 ACAD GAS Male', 'G11 ACAD PBM Male',
    'G11 TVL Male', 'G11 SPORTS Male', 'G11 ARTS Male', 'G12 ACAD ABM Male', 'G12 ACAD HUMSS Male',
    'G12 ACAD STEM Male', 'G12 ACAD GAS Male', 'G12 ACAD PBM Male', 'G12 TVL Male', 'G12 SPORTS Male', 'G12 ARTS Male'
]
senior_female = [
    'G11 ACAD ABM Female', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Female', 'G11 ACAD GAS Female',
    'G11 ACAD PBM Female',
    'G11 TVL Female', 'G11 SPORTS Female', 'G11 ARTS Female', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Female',
    'G12 ACAD STEM Female', 'G12 ACAD GAS Female', 'G12 ACAD PBM Female', 'G12 TVL Female', 'G12 SPORTS Female',
    'G12 ARTS Female'
]



# Metrics and bar chart callback
@app.callback(
    Output('male_summary_card', 'children'),
    Output('female_summary_card', 'children'),
    Output('total_summary_card', 'children'),
    Output('total_school_card', 'children'),
    Output('education_bar_chart', 'figure'),
    Output('elementary_bar_chart', 'figure'),
    Output('jhs_bar_chart', 'figure'),
    Output('shs_bar_chart', 'figure'),
    Output('enrollment_rate_chart', 'figure'),
    Output('tracks_rate_chart', 'figure'),

    Input('stored-data', 'data'),
    Input('region_dd', 'value'),
    Input('province_dd', 'value'),
    Input('division_dd', 'value'),
    Input('district_dd', 'value'),
    Input('municipality_dd', 'value'),
    Input('legislative_district_dd', 'value'),
    Input('sector_dd', 'value'),
    Input('school_type_dd', 'value'),
    Input('modified_coc_dd', 'value'),
    Input('school_subclass_dd', 'value')
)
def update_metrics_and_chart(data, region, province, division, district, municipality,
                             legislative_district, sector, school_type, modified_coc, school_subclass):
    if data is None:
        empty_fig = px.bar(
            x=["Elementary", "Junior High School", "Senior High School"],
            y=[0, 0, 0],
            title="No data available",
            labels={"x": "Education Level", "y": "Enrollment"}
        )
        empty_fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#1d1d1f'},
            margin=dict(l=10, r=10, t=40, b=10),
            title_font_size=16,
            showlegend=False
        )
        return (
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                                html.Div("Males", style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                                style={
                                    "display": "flex","flexDirection": "column","alignItems": "center"}),
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                                html.Div("Females", style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                                style={
                                    "display": "flex","flexDirection": "column","alignItems": "center"}),
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                                html.Div("Enrollment", style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                                style={
                                    "display": "flex","flexDirection": "column","alignItems": "center"}),
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                                html.Div("Schools", style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                                style={
                                    "display": "flex","flexDirection": "column","alignItems": "center"}), 
            empty_fig, 
            empty_fig, 
            empty_fig, 
            empty_fig, 
            empty_fig, 
            empty_fig)

    df = pd.DataFrame(data)

    # this is fixed enrollees sum (will  not be changed based on the filters)
    enrollment_cols = [col for col in df.columns if 'Male' in col or 'Female' in col]
    df[enrollment_cols] = df[enrollment_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    fixed_enrollee_sum = int(df[enrollment_cols].sum().sum())

    # fixed total schools
    fixed_total_schools = df.drop_duplicates().shape[0]

    # Define columns
    elementary_male = ['K Male', 'G1 Male', 'G2 Male', 'G3 Male', 'G4 Male', 'G5 Male', 'G6 Male', 'Elem NG Male']
    elementary_female = ['K Female', 'G1 Female', 'G2 Female', 'G3 Female', 'G4 Female', 'G5 Female', 'G6 Female',
                         'Elem NG Female']
    junior_male = ['G7 Male', 'G8 Male', 'G9 Male', 'G10 Male', 'JHS NG Male']
    junior_female = ['G7 Female', 'G8 Female', 'G9 Female', 'G10 Female', 'JHS NG Female']
    senior_male = [
        'G11 ACAD ABM Male', 'G11 ACAD HUMSS Male', 'G11 ACAD STEM Male', 'G11 ACAD GAS Male', 'G11 ACAD PBM Male',
        'G11 TVL Male', 'G11 SPORTS Male', 'G11 ARTS Male', 'G12 ACAD ABM Male', 'G12 ACAD HUMSS Male',
        'G12 ACAD STEM Male', 'G12 ACAD GAS Male', 'G12 ACAD PBM Male', 'G12 TVL Male', 'G12 SPORTS Male',
        'G12 ARTS Male'
    ]
    senior_female = [
        'G11 ACAD ABM Female', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Female', 'G11 ACAD GAS Female',
        'G11 ACAD PBM Female',
        'G11 TVL Female', 'G11 SPORTS Female', 'G11 ARTS Female', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Female',
        'G12 ACAD STEM Female', 'G12 ACAD GAS Female', 'G12 ACAD PBM Female', 'G12 TVL Female', 'G12 SPORTS Female',
        'G12 ARTS Female'
    ]
    all_gender_cols = elementary_male + elementary_female + junior_male + junior_female + senior_male + senior_female

    # Apply filters
    filters = {
        'Region': region,
        'Province': province,
        'Division': division,
        'District': district,
        'Municipality': municipality,
        'Legislative District': legislative_district,
        'Sector': sector,
        'School Type': school_type,
        'Modified COC': modified_coc,
        'School Subclassification': school_subclass
    }

    for col, selected_values in filters.items():
        if selected_values:
            df = df[df[col].isin(selected_values)]

    df[all_gender_cols] = df[all_gender_cols].replace('Not Applicable', 0)
    df[all_gender_cols] = df[all_gender_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    total_male = df[[col for col in all_gender_cols if 'Male' in col]].sum().sum()
    total_female = df[[col for col in all_gender_cols if 'Female' in col]].sum().sum()
    total_enrollees = total_male + total_female
    total_schools = df['BEIS School ID'].nunique()

    # Apple-style plot formatting
    apple_theme = {
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {'color': '#1d1d1f', 'family': 'SF Pro Display, Helvetica, Arial, sans-serif'},
        'title_font_size': 16,
        'xaxis': {'showgrid': False},
        'yaxis': {'showgrid': True, 'gridcolor': '#f5f5f7','title': None},
        'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        'margin': dict(l=10, r=10, t=40, b=10),
    }

    male_color = '#0038a8'
    female_color = '#c7a93f'

    # Education Level Bar Chart
    bar_data = pd.DataFrame({
        'Education Level': ['Elementary', 'Elementary', 'Junior High School', 'Junior High School',
                            'Senior High School', 'Senior High School'],
        'Gender': ['Male', 'Female'] * 3,
        'Enrollment': [
            df[elementary_male].sum().sum(), df[elementary_female].sum().sum(),
            df[junior_male].sum().sum(), df[junior_female].sum().sum(),
            df[senior_male].sum().sum(), df[senior_female].sum().sum()
        ]
    })

    # Calculate total enrollment per education level
    bar_data["Total Enrollment"] = bar_data.groupby("Education Level")["Enrollment"].transform("sum")

    bar_data["Education Level"] = bar_data["Education Level"].replace({
        "Junior High School": "Junior HS",
        "Senior High School": "Senior HS"
    })

    edu_order = ["Elementary", "Junior HS", "Senior HS"]

    education_fig = px.bar(
        bar_data,
        y="Enrollment",
        x="Education Level",
        color="Gender",
        barmode="stack",
        custom_data=["Total Enrollment", "Gender"],
        color_discrete_map={'Male': male_color, 'Female': female_color},
        category_orders={"Education Level": edu_order}
    )

    education_fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{y}<br>Total Enrollment: %{customdata[0]:,}<extra></extra>"
    )

    education_fig.update_layout(**apple_theme)

    # Elementary
    grade_levels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'Elem NG']
    male_values = [df[f'{lvl} Male'].sum() for lvl in grade_levels]
    female_values = [df[f'{lvl} Female'].sum() for lvl in grade_levels]
    total_values = [m + f for m, f in zip(male_values, female_values)]


    total_values_repeated = total_values * 2
    genders = ['Male'] * len(grade_levels) + ['Female'] * len(grade_levels)
    enrollments = male_values + female_values

    elementary_df = pd.DataFrame({
        'Grade Level': grade_levels * 2,
        'Gender': genders,
        'Enrollment': enrollments,
        'Total': total_values_repeated  
    })


    elementary_fig = px.bar(
        elementary_df,
        x='Grade Level',
        y='Enrollment',
        color='Gender',
        barmode='stack',
        text='Enrollment',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total', 'Gender'],
        category_orders={
            'Grade Level': ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'Elem NG']
        },
        labels={'Grade Level': 'Grade Level'}
    )

    elementary_fig.update_layout(**apple_theme)

    elementary_fig.update_traces(
        texttemplate='%{text:,}',
        textposition='none',
        hovertemplate="<b>Grade Level: %{x}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{y:,}<br>Total: %{customdata[0]:,}<extra></extra>"
    )


    elementary_fig.update_xaxes(
        tickmode='array',
        tickvals=grade_levels,
        ticktext=[lvl if lvl != 'Elem NG' else 'NG' for lvl in grade_levels]
    )

    # Junior HS
    jhs_levels = ['G7', 'G8', 'G9', 'G10', 'JHS NG']
    jhs_male_values = [df[f'{lvl} Male'].sum() for lvl in jhs_levels]
    jhs_female_values = [df[f'{lvl} Female'].sum() for lvl in jhs_levels]
    jhs_total_values = [m + f for m, f in zip(jhs_male_values, jhs_female_values)]


    jhs_total_repeated = jhs_total_values * 2
    jhs_genders = ['Male'] * len(jhs_levels) + ['Female'] * len(jhs_levels)
    jhs_enrollments = jhs_male_values + jhs_female_values

    jhs_df = pd.DataFrame({
        'Grade Level': jhs_levels * 2,
        'Gender': jhs_genders,
        'Enrollment': jhs_enrollments,
        'Total': jhs_total_repeated 
    })

    jhs_fig = px.bar(
        jhs_df,
        x='Grade Level',
        y='Enrollment',
        color='Gender',
        barmode='stack',
        text='Enrollment',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total', 'Gender'],
        category_orders={'Grade Level': ['G7', 'G8', 'G9', 'G10', 'JHS NG']}
    )

    jhs_fig.update_layout(**apple_theme)

    jhs_fig.update_traces(
        texttemplate='%{text:,}',
        textposition='none',
        hovertemplate="<b>Grade Level: %{x}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{y:,}<br>Total: %{customdata[0]:,}<extra></extra>"
    )


    jhs_fig.update_xaxes(
        tickmode='array',
        tickvals=jhs_levels,
        ticktext=[lvl if lvl != 'JHS NG' else 'NG' for lvl in jhs_levels]
    )


    # Senior HS
    shs_tracks = [
        'ACAD ABM', 'ACAD HUMSS', 'ACAD STEM', 'ACAD GAS', 'ACAD PBM', 'TVL', 'SPORTS', 'ARTS'
    ]

    male_shs_values = [
        df[[f'G11 {track} Male' if 'G11' in f'G11 {track} Male' else f'G11 ACAD {track} Male',
            f'G12 {track} Male' if 'G12' in f'G12 {track} Male' else f'G12 ACAD {track} Male']].sum().sum()
        for track in shs_tracks
    ]
    female_shs_values = [
        df[[f'G11 {track} Female' if 'G11' in f'G11 {track} Female' else f'G11 ACAD {track} Female',
            f'G12 {track} Female' if 'G12' in f'G12 {track} Female' else f'G12 ACAD {track} Female']].sum().sum()
        for track in shs_tracks
    ]

    total_shs_values = [m + f for m, f in zip(male_shs_values, female_shs_values)]
    shs_total_repeated = total_shs_values * 2
    shs_genders = ['Male'] * len(shs_tracks) + ['Female'] * len(shs_tracks)
    shs_enrollments = male_shs_values + female_shs_values

    shs_df = pd.DataFrame({
        'Track': shs_tracks * 2,
        'Gender': shs_genders,
        'Enrollment': shs_enrollments,
        'Total': shs_total_repeated
    })

    shs_df['Track Cleaned'] = shs_df['Track'].str.replace('ACAD ', '', regex=False)


    shs_df = shs_df.sort_values('Total', ascending=False)


    shs_fig = px.bar(
        shs_df,
        orientation='h',
        x='Enrollment',
        y='Track Cleaned',
        color='Gender',
        barmode='stack',
        text='Enrollment',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total', 'Gender']
    )


    shs_fig.update_layout(**apple_theme)

    shs_fig.update_layout(
        yaxis=dict(
            autorange='reversed' 
        )
    )

    shs_fig.update_traces(
        texttemplate='%{text:,}',
        textposition='none',
        hovertemplate="<b>%{y}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{x:,}<br>Total: %{customdata[0]:,}<extra></extra>"
    )

    # Student Count per Grade
    grade_levels = {
        'K': ['K Male', 'K Female'],
        'G1': ['G1 Male', 'G1 Female'],
        'G2': ['G2 Male', 'G2 Female'],
        'G3': ['G3 Male', 'G3 Female'],
        'G4': ['G4 Male', 'G4 Female'],
        'G5': ['G5 Male', 'G5 Female'],
        'G6': ['G6 Male', 'G6 Female'],
        'G7': ['G7 Male', 'G7 Female'],
        'G8': ['G8 Male', 'G8 Female'],
        'G9': ['G9 Male', 'G9 Female'],
        'G10': ['G10 Male', 'G10 Female'],
        'E-NG': ['Elem NG Male', 'Elem NG Female'],  
        'J-NG': ['JHS NG Male', 'JHS NG Female']     
    }

    data = []
    for level, cols in grade_levels.items():
        male_cols = [col for col in cols if 'Male' in col]
        female_cols = [col for col in cols if 'Female' in col]

        df[level + '_Male'] = df[male_cols].sum(axis=1)
        df[level + '_Female'] = df[female_cols].sum(axis=1)

        male_avg = round(df[level + '_Male'].mean())
        female_avg = round(df[level + '_Female'].mean())
        total_avg = male_avg + female_avg

        data.append({'Grade Level': level, 'Gender': 'Male', 'Average Enrollees': male_avg, 'Total Enrollees': total_avg})
        data.append({'Grade Level': level, 'Gender': 'Female', 'Average Enrollees': female_avg, 'Total Enrollees': total_avg})

    df_chart = pd.DataFrame(data)

    
    grade_order_map = {
    'K': 0,
    'G1': 1,
    'G2': 2,
    'G3': 3,
    'G4': 4,
    'G5': 5,
    'G6': 6,
    'G7': 7,
    'G8': 8,
    'G9': 9,
    'G10': 10,
    'E-NG': 11,  
    'J-NG': 12   
    }
    df_chart['Grade Order'] = df_chart['Grade Level'].map(grade_order_map)
    df_chart = df_chart.sort_values('Grade Order')

    df_chart = df_chart.sort_values('Grade Order')

    fig = px.bar(
        df_chart,
        x='Grade Level',
        y='Average Enrollees',
        color='Gender',
        barmode='stack',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total Enrollees', 'Gender'],
    )

    fig.update_traces(
        hovertemplate=
        '<b>%{x}</b><br>' +
        'Gender: %{customdata[1]}<br>' +
        'Average Enrollees: %{y}<br>' +
        'Total Enrollees: %{customdata[0]}<br>' +
        '<extra></extra>'
    )

    fig.update_layout(**apple_theme)

    # Define SHS tracks
    shs_tracks = {
        'ABM': ['G11 ACAD ABM Male', 'G12 ACAD ABM Male', 'G11 ACAD ABM Female', 'G12 ACAD ABM Female'],
        'HUMSS': ['G11 ACAD HUMSS Male', 'G12 ACAD HUMSS Male', 'G11 ACAD HUMSS Female', 'G12 ACAD HUMSS Female'],
        'STEM': ['G11 ACAD STEM Male', 'G12 ACAD STEM Male', 'G11 ACAD STEM Female', 'G12 ACAD STEM Female'],
        'GAS': ['G11 ACAD GAS Male', 'G12 ACAD GAS Male', 'G11 ACAD GAS Female', 'G12 ACAD GAS Female'],
        'PBM': ['G11 ACAD PBM Male', 'G12 ACAD PBM Male', 'G11 ACAD PBM Female', 'G12 ACAD PBM Female'],
        'TVL': ['G11 TVL Male', 'G12 TVL Male', 'G11 TVL Female', 'G12 TVL Female'],
        'SPORTS': ['G11 SPORTS Male', 'G12 SPORTS Male', 'G11 SPORTS Female', 'G12 SPORTS Female'],
        'ARTS': ['G11 ARTS Male', 'G12 ARTS Male', 'G11 ARTS Female', 'G12 ARTS Female']
    }


    data = []
    for track, cols in shs_tracks.items():
        g11_male_col = [col for col in cols if 'G11' in col and 'Male' in col]
        g12_male_col = [col for col in cols if 'G12' in col and 'Male' in col]
        g11_female_col = [col for col in cols if 'G11' in col and 'Female' in col]
        g12_female_col = [col for col in cols if 'G12' in col and 'Female' in col]

        g11_male_avg = df[g11_male_col].mean(axis=1)
        g12_male_avg = df[g12_male_col].mean(axis=1)
        g11_female_avg = df[g11_female_col].mean(axis=1)
        g12_female_avg = df[g12_female_col].mean(axis=1)

        male_avg = round(((g11_male_avg + g12_male_avg) / 2).mean())
        female_avg = round(((g11_female_avg + g12_female_avg) / 2).mean())
        total_avg = male_avg + female_avg

        data.append({'Track': track, 'Gender': 'Male', 'Average Enrollees': male_avg, 'Total Enrollees': total_avg})
        data.append({'Track': track, 'Gender': 'Female', 'Average Enrollees': female_avg, 'Total Enrollees': total_avg})

 
    df_chart = pd.DataFrame(data)

    track_order = (
        df_chart.groupby('Track')['Total Enrollees']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )


    track_order = track_order[::-1] 


    df_chart['Track'] = pd.Categorical(df_chart['Track'], categories=track_order, ordered=True)


    df_chart['Gender'] = pd.Categorical(df_chart['Gender'], categories=['Male', 'Female'], ordered=True)


    df_chart = df_chart.sort_values(by=['Track', 'Gender'], ascending=[True, True])

    # Plot
    fig_tracks = px.bar(
        df_chart,
        x='Average Enrollees',
        y='Track',
        color='Gender',
        barmode='stack',
        color_discrete_map={'Female': female_color, 'Male': male_color},
        custom_data=['Total Enrollees', 'Gender'],
    )

    fig_tracks.update_traces(
        hovertemplate=
        '<b>%{y}</b><br>' +
        'Gender: %{customdata[1]}<br>' +
        'Average Enrollees: %{x}<br>' +
        'Total Enrollees: %{customdata[0]}<br>' +
        '<extra></extra>'
    )

    fig_tracks.update_layout(**apple_theme)


    return (
        html.Div([
            html.H4("Male", style={'fontSize': '15px', 'margin': '0px', 'marginTop':'5px'}),
            html.Div(f"{int(total_male):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(f"{int(total_male)/total_enrollees*100:.1f}% of Total" if total_enrollees > 0 else "0%", 
            style={'fontSize': '14px', 'color': '#888'}),]),

        html.Div([
            html.H4("Female", style={'fontSize': '15px', 'margin': '0px', 'marginTop':'5px'}),
            html.Div(f"{int(total_female):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(f"{int(total_female)/total_enrollees*100:.1f}% of Total" if total_enrollees > 0 else "0%", 
            style={'fontSize': '14px', 'color': '#888'}),]),

        
        html.Div([
            html.H4("Enrollees", style={'fontSize': '15px', 'margin': '0px', 'marginTop':'5px'}),
            html.Div(f"{int(total_enrollees):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(f"{int(total_enrollees)/fixed_enrollee_sum*100:.1f}% of Nationwide" if fixed_enrollee_sum > 0 else "0%", 
            style={'fontSize': '14px', 'color': '#888'}),]),

        
         html.Div([
            html.H4("Schools", style={'fontSize': '15px', 'margin': '0px', 'marginTop':'5px'}),
            html.Div(f"{int(total_schools):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(f"{int(total_schools)/fixed_total_schools*100:.1f}% of Nationwide" if fixed_total_schools > 0 else "0%", 
            style={'fontSize': '14px', 'color': '#888'}),]),

        education_fig,
        elementary_fig,
        jhs_fig,
        shs_fig,
        fig,
        fig_tracks
    )

if __name__ == '__main__':
    app.run(debug=True)













