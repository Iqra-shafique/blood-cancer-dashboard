"""
Blood Cancer Diseases Dashboard
A comprehensive Streamlit application for analyzing blood cancer datasets
with real-time data cleaning, visualization, and clinical insights.

Author: Data Analysis Team
Version: 1.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG & THEME SETUP
# ============================================================================
st.set_page_config(
    page_title="Blood Cancer Analysis Dashboard",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "### Blood Cancer Diseases Dashboard\nVersion 1.0\nComprehensive Medical Data Analysis Platform"
    }
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
    }
    
    .main {
        padding-top: 2rem;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        border: 2px solid #e0e0e0;
    }
    
    .stMetric label {
        color: #333333 !important;
        font-weight: 600;
        font-size: 0.95rem !important;
    }
    
    .stMetric > div {
        color: #000000 !important;
    }
    
    .stMetric > div > label {
        color: #1f77b4 !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-weight: 600 !important;
    }
    
    .section-header {
        color: #1f77b4;
        font-size: 2rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    
    .tutorial-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE & INITIALIZATION
# ============================================================================
@st.cache_resource
def initialize_app():
    """Initialize app with default settings"""
    return {
        'data_loaded': False,
        'data_cleaned': False,
        'df': None
    }

if 'app_state' not in st.session_state:
    st.session_state.app_state = initialize_app()

# ============================================================================
# DATA LOADING & CLEANING FUNCTIONS
# ============================================================================
@st.cache_data
def load_data(file_path):
    """Load CSV data with error handling"""
    try:
        df = pd.read_csv(file_path)
        # Convert numeric columns
        for col in df.columns:
            if 'WBC' in col or 'Platelet' in col or 'Age' in col:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df, None
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

def analyze_missing_values(df):
    """Analyze missing values in the dataset"""
    # Convert numeric columns to proper types
    for col in df.columns:
        if 'WBC' in col or 'Platelet' in col or 'Age' in col:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    missing_data = {
        'Column': df.columns,
        'Missing_Count': df.isnull().sum().values,
        'Missing_Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
    }
    return pd.DataFrame(missing_data)

def clean_data(df):
    """
    Comprehensive data cleaning function
    Steps:
    1. Remove duplicate rows
    2. Handle missing values intelligently
    3. Standardize categorical values
    4. Remove outliers in numeric columns
    5. Fix data types
    """
    df_clean = df.copy()
    
    cleaning_report = {
        'Original_Rows': len(df),
        'Actions': []
    }
    
    # Step 1: Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_rows - len(df_clean)
    if duplicates_removed > 0:
        cleaning_report['Actions'].append(f"✓ Removed {duplicates_removed} duplicate rows")
    
    # Step 2: Handle missing values
    missing_report = analyze_missing_values(df_clean)
    
    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:
            if df_clean[col].dtype == 'object':
                # For categorical columns, fill with mode or 'Unknown'
                mode_val = df_clean[col].mode()
                if len(mode_val) > 0:
                    df_clean[col].fillna(mode_val[0], inplace=True)
                else:
                    df_clean[col].fillna('Unknown', inplace=True)
            else:
                # For numeric columns, fill with median
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    cleaning_report['Actions'].append(f"✓ Handled missing values using median/mode imputation")
    
    # Step 3: Standardize categorical values
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df_clean[col] = df_clean[col].str.strip()
    
    cleaning_report['Actions'].append(f"✓ Standardized {len(categorical_cols)} categorical columns")
    
    # Step 4: Handle outliers in numeric columns (using IQR method)
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    outliers_removed = 0
    
    for col in numeric_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Keep track of outliers but don't remove, just flag them
        outlier_mask = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
        outliers_removed += outlier_mask.sum()
    
    cleaning_report['Actions'].append(f"✓ Analyzed {len(numeric_cols)} numeric columns for outliers")
    
    # Step 5: Data type optimization
    for col in df_clean.columns:
        # Convert numeric columns
        if col.lower() in ['age', 'wbc', 'platelet']:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        # Convert any column with numbers in header
        if 'WBC' in col or 'Platelet' in col or 'Age' in col:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    cleaning_report['Actions'].append("✓ Optimized data types")
    cleaning_report['Final_Rows'] = len(df_clean)
    cleaning_report['Rows_Removed'] = len(df) - len(df_clean)
    
    return df_clean, cleaning_report, missing_report

# ============================================================================
# MAIN APP LAYOUT
# ============================================================================
def main():
    # Header
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown("# 🩸 Blood Cancer Diseases Analysis Dashboard")
    with col2:
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    st.markdown("---")
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 📋 Navigation Menu")
        page = st.radio(
            "Select a Page:",
            ["🏠 Home", "📊 Data Overview", "🔧 Data Cleaning", "📈 Analytics", 
             "🎯 Clinical Insights", "📚 Tutorial & Help"],
            help="Choose different sections to explore the dashboard"
        )
        
        st.markdown("---")
        st.markdown("### 📁 Dataset Information")
        if st.session_state.app_state['data_loaded']:
            st.success("✓ Data Loaded Successfully")
            st.info(f"📊 Total Records: {len(st.session_state.app_state['df'])}")
            st.info(f"📋 Total Columns: {len(st.session_state.app_state['df'].columns)}")
    
    # Route to pages
    if page == "🏠 Home":
        show_home()
    elif page == "📊 Data Overview":
        show_data_overview()
    elif page == "🔧 Data Cleaning":
        show_data_cleaning()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "🎯 Clinical Insights":
        show_clinical_insights()
    else:
        show_tutorial()

# ============================================================================
# PAGE: HOME
# ============================================================================
def show_home():
    st.markdown("### Welcome to the Blood Cancer Analysis Dashboard 🏥")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📂 **Step 1: Load Data**\nClick 'Load Dataset' below to start")
    with col2:
        st.info("🧹 **Step 2: Clean Data**\nAutomatically clean and prepare data")
    with col3:
        st.info("📊 **Step 3: Analyze**\nExplore insights and visualizations")
    
    st.markdown("---")
    
    # Load Dataset Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Load Dataset", key="load_btn", use_container_width=True):
            with st.spinner("Loading data..."):
                file_path = r"c:\Users\User\Desktop\assignment\Assignment\Blood Cancer Diseases dataset  - Sheet1.csv"
                df, error = load_data(file_path)
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.app_state['df'] = df
                    st.session_state.app_state['data_loaded'] = True
                    st.success("✅ Data loaded successfully!")
                    st.rerun()
    
    st.markdown("---")
    
    # Feature Overview
    st.markdown("### 🎯 Dashboard Features")
    
    features = {
        "📊 Data Overview": "View raw data, column information, and basic statistics",
        "🧹 Data Cleaning": "Automated data cleaning with detailed reports and visualizations",
        "📈 Analytics": "Comprehensive visualizations and correlation analysis",
        "🎯 Clinical Insights": "Medical insights, treatment outcomes, and cancer type analysis",
        "📚 Tutorial & Help": "Complete guide on how to use the dashboard"
    }
    
    for feature, description in features.items():
        st.markdown(f"**{feature}**  \n{description}")
    
    st.markdown("---")
    st.markdown("### 📌 Quick Start Guide")
    st.markdown("""
    1. **Load the Dataset** - Click the button above to load the CSV file
    2. **Clean the Data** - Go to 'Data Cleaning' for automated cleaning
    3. **Explore Data** - Use 'Data Overview' to see raw data
    4. **View Analytics** - Check 'Analytics' for visualizations
    5. **Get Insights** - Visit 'Clinical Insights' for medical analysis
    6. **Learn More** - Read 'Tutorial & Help' for detailed explanations
    """)

# ============================================================================
# PAGE: DATA OVERVIEW
# ============================================================================
def show_data_overview():
    st.markdown("## 📊 Data Overview")
    
    if not st.session_state.app_state['data_loaded']:
        st.warning("⚠️ Please load the dataset first from the Home page!")
        return
    
    df = st.session_state.app_state['df']
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Raw Data", "📊 Statistics", "ℹ️ Column Info", "🔍 Data Quality"])
    
    with tab1:
        st.markdown("### Raw Dataset Preview")
        st.dataframe(df.head(100), use_container_width=True, height=400)
        st.markdown(f"**Showing first 100 rows of {len(df)} total rows**")
    
    with tab2:
        st.markdown("### Statistical Summary")
        st.dataframe(df.describe().T, use_container_width=True)
    
    with tab3:
        st.markdown("### Column Information")
        col_info = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values,
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)
    
    with tab4:
        st.markdown("### Data Quality Assessment")
        missing = analyze_missing_values(df)
        
        # Visualize missing data
        fig = px.bar(
            missing[missing['Missing_Count'] > 0],
            x='Column',
            y='Missing_Percentage',
            title="Missing Values by Column",
            labels={'Missing_Percentage': 'Missing %', 'Column': 'Column Name'},
            color='Missing_Percentage',
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Data quality score
        completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Data Completeness Score", f"{completeness:.2f}%")
        st.dataframe(missing, use_container_width=True)

# ============================================================================
# PAGE: DATA CLEANING
# ============================================================================
def show_data_cleaning():
    st.markdown("## 🧹 Data Cleaning & Preprocessing")
    
    if not st.session_state.app_state['data_loaded']:
        st.warning("⚠️ Please load the dataset first from the Home page!")
        return
    
    df = st.session_state.app_state['df']
    
    st.markdown("### 📚 Tutorial: Data Cleaning Process")
    with st.expander("ℹ️ Learn about each cleaning step", expanded=False):
        st.markdown("""
        #### Cleaning Steps Explained:
        
        1. **Remove Duplicates**: Identifies and removes exact duplicate rows that might skew analysis
        2. **Handle Missing Values**: 
           - Categorical: Filled with mode (most frequent value)
           - Numeric: Filled with median (resistant to outliers)
        3. **Standardize Text**: Removes extra spaces from categorical data
        4. **Outlier Detection**: Uses IQR method to identify unusual values
        5. **Data Type Optimization**: Ensures columns have correct data types
        
        #### Why It Matters:
        - Improves model accuracy
        - Prevents biased analysis
        - Ensures consistent results
        - Reduces computational errors
        """)
    
    # Before Cleaning Analysis
    st.markdown("### 📊 Before Cleaning Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        st.metric("Missing Data %", f"{missing_pct:.2f}%")
    
    # Missing values visualization
    st.markdown("### Missing Values Heatmap")
    missing_data = analyze_missing_values(df)
    fig = px.bar(
        missing_data[missing_data['Missing_Count'] > 0],
        x='Column',
        y='Missing_Count',
        title="Missing Values Count by Column",
        color='Missing_Count',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Clean Data Button
    st.markdown("---")
    st.markdown("### 🔄 Clean the Data")
    
    if st.button("🚀 Start Data Cleaning Process", use_container_width=True, type="primary"):
        with st.spinner("🔄 Cleaning data... This may take a moment..."):
            df_cleaned, report, missing_report = clean_data(df)
            st.session_state.app_state['df_cleaned'] = df_cleaned
            st.session_state.app_state['data_cleaned'] = True
            
            # Display cleaning report
            st.success("✅ Data Cleaning Completed Successfully!")
            
            st.markdown("### 📋 Cleaning Report")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Original Rows", report['Original_Rows'])
            with col2:
                st.metric("Final Rows", report['Final_Rows'])
            with col3:
                st.metric("Rows Removed", report['Rows_Removed'])
            with col4:
                removal_pct = (report['Rows_Removed'] / report['Original_Rows'] * 100)
                st.metric("Removal %", f"{removal_pct:.2f}%")
            
            st.markdown("#### Actions Performed:")
            for action in report['Actions']:
                st.info(action)
            
            # Comparison Table
            st.markdown("#### Before vs After Cleaning")
            comparison = pd.DataFrame({
                'Metric': ['Total Rows', 'Total Columns', 'Missing Values'],
                'Before': [len(df), len(df.columns), df.isnull().sum().sum()],
                'After': [len(df_cleaned), len(df_cleaned.columns), df_cleaned.isnull().sum().sum()]
            })
            st.dataframe(comparison, use_container_width=True)
            
            st.balloons()
    
    # Show cleaned data preview if available
    if st.session_state.app_state['data_cleaned']:
        st.markdown("---")
        st.markdown("### 👁️ Cleaned Data Preview")
        df_cleaned = st.session_state.app_state['df_cleaned']
        st.dataframe(df_cleaned.head(50), use_container_width=True, height=400)
        
        # Download cleaned data
        csv = df_cleaned.to_csv(index=False)
        st.download_button(
            label="📥 Download Cleaned Data (CSV)",
            data=csv,
            file_name=f"blood_cancer_cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============================================================================
# PAGE: ANALYTICS
# ============================================================================
def show_analytics():
    st.markdown("## 📈 Analytics & Visualizations")
    
    if not st.session_state.app_state['data_loaded']:
        st.warning("⚠️ Please load the dataset first from the Home page!")
        return
    
    # Use cleaned data if available, otherwise original
    df = st.session_state.app_state.get('df_cleaned', st.session_state.app_state['df'])
    
    st.markdown("### 📚 Tutorial: Understanding the Visualizations")
    with st.expander("ℹ️ Learn how to interpret charts", expanded=False):
        st.markdown("""
        - **Bar Charts**: Compare values across categories
        - **Pie Charts**: Show proportions of a whole
        - **Scatter Plots**: Show relationships between two variables
        - **Heatmaps**: Display correlations between variables
        - **Line Charts**: Track trends over time or sequences
        """)
    
    # Create tabs for different analytics
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Distribution", "🎯 Cancer Analysis", "💊 Treatment", "🧬 Genetic", "🔗 Correlations"
    ])
    
    with tab1:
        st.markdown("### Age Distribution")
        fig = px.histogram(df, x='Age', nbins=30, title="Age Distribution of Patients",
                          labels={'Age': 'Age (years)', 'count': 'Number of Patients'},
                          color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Age", f"{df['Age'].mean():.1f} years")
        with col2:
            st.metric("Median Age", f"{df['Age'].median():.1f} years")
        with col3:
            st.metric("Age Range", f"{df['Age'].min()}-{df['Age'].max()} years")
        
        st.markdown("### Gender Distribution")
        gender_counts = df['Gender'].value_counts()
        fig = px.pie(values=gender_counts.values, names=gender_counts.index,
                     title="Gender Distribution", color_discrete_sequence=['#FF6B9D', '#4A90E2'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Cancer Type Distribution")
        cancer_counts = df['Cancer_Type(AML, ALL, CLL)'].value_counts()
        fig = px.bar(x=cancer_counts.index, y=cancer_counts.values,
                     title="Number of Patients by Cancer Type",
                     labels={'x': 'Cancer Type', 'y': 'Number of Patients'},
                     color=cancer_counts.values,
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Cancer Type by Diagnosis Result")
        cancer_diagnosis = pd.crosstab(df['Cancer_Type(AML, ALL, CLL)'], df['Diagnosis_Result'])
        fig = px.bar(cancer_diagnosis, barmode='group', title="Cancer Type by Diagnosis Result",
                     labels={'value': 'Count', 'index': 'Cancer Type'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Treatment Type Distribution")
        treatment_counts = df['Treatment_Type(Chemotherapy, Radiation)'].value_counts()
        fig = px.bar(x=treatment_counts.index, y=treatment_counts.values,
                     title="Number of Patients by Treatment Type",
                     labels={'x': 'Treatment Type', 'y': 'Number of Patients'},
                     color=treatment_counts.values,
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Treatment Outcomes")
        outcome_counts = df['Treatment_Outcome'].value_counts()
        colors_map = {'Cured': '#2ecc71', 'Ongoing': '#f39c12', 'Deceased': '#e74c3c'}
        colors = [colors_map.get(x, '#95a5a6') for x in outcome_counts.index]
        fig = px.pie(values=outcome_counts.values, names=outcome_counts.index,
                     title="Treatment Outcomes Distribution",
                     color_discrete_sequence=colors)
        st.plotly_chart(fig, use_container_width=True)
        
        # Success rate
        success_rate = (outcome_counts.get('Cured', 0) / len(df) * 100)
        st.metric("Treatment Success Rate (Cured)", f"{success_rate:.2f}%")
    
    with tab4:
        st.markdown("### Genetic Data Distribution")
        genetic_counts = df['Genetic_Data(BCR-ABL, FLT3)'].value_counts()
        fig = px.bar(x=genetic_counts.index, y=genetic_counts.values,
                     title="Genetic Markers in Patients",
                     labels={'x': 'Genetic Marker', 'y': 'Number of Patients'},
                     color=genetic_counts.values,
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Side Effects by Treatment Type")
        side_effects = pd.crosstab(df['Treatment_Type(Chemotherapy, Radiation)'], df['Side_Effects'])
        fig = px.bar(side_effects, barmode='stack', title="Side Effects by Treatment Type",
                     labels={'value': 'Count'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown("### Correlation Heatmap")
        
        # Select numeric columns for correlation
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10}
            ))
            fig.update_layout(title="Correlation Matrix of Numeric Variables", height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Age vs Platelet Count
        st.markdown("### Age vs Platelet Count Scatter Plot")
        fig = px.scatter(df, x='Age', y='Platelet Count( (/cumm)',
                         color='Treatment_Outcome',
                         title="Relationship between Age and Platelet Count",
                         hover_data=['Cancer_Type(AML, ALL, CLL)', 'Treatment_Type(Chemotherapy, Radiation)'],
                         color_discrete_map={'Cured': '#2ecc71', 'Ongoing': '#f39c12', 'Deceased': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: CLINICAL INSIGHTS
# ============================================================================
def show_clinical_insights():
    st.markdown("## 🎯 Clinical Insights & Analysis")
    
    if not st.session_state.app_state['data_loaded']:
        st.warning("⚠️ Please load the dataset first from the Home page!")
        return
    
    df = st.session_state.app_state.get('df_cleaned', st.session_state.app_state['df'])
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👨‍⚕️ Treatment Outcomes", "🔬 Diagnostic Data", "⚠️ Risk Analysis", "📊 Key Metrics"
    ])
    
    with tab1:
        st.markdown("### Treatment Outcome Analysis by Cancer Type")
        
        outcome_by_cancer = pd.crosstab(
            df['Cancer_Type(AML, ALL, CLL)'],
            df['Treatment_Outcome'],
            margins=True
        )
        st.dataframe(outcome_by_cancer, use_container_width=True)
        
        # Success rate by cancer type
        st.markdown("### Treatment Success Rate by Cancer Type")
        success_by_cancer = df.groupby('Cancer_Type(AML, ALL, CLL)').apply(
            lambda x: (len(x[x['Treatment_Outcome'] == 'Cured']) / len(x) * 100)
        ).sort_values(ascending=False)
        
        fig = px.bar(
            x=success_by_cancer.index,
            y=success_by_cancer.values,
            title="Cure Rate by Cancer Type (%)",
            labels={'x': 'Cancer Type', 'y': 'Cure Rate (%)'},
            color=success_by_cancer.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Outcome by treatment type
        st.markdown("### Treatment Outcomes by Treatment Type")
        outcome_by_treatment = pd.crosstab(
            df['Treatment_Type(Chemotherapy, Radiation)'],
            df['Treatment_Outcome']
        )
        fig = px.bar(outcome_by_treatment, barmode='group', title="Outcomes by Treatment Type",
                     color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Diagnostic Test Results Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### Bone Marrow Aspiration")
            bma = df['Bone Marrow Aspiration(Positive / Negative / Not Done)'].value_counts()
            st.bar_chart(bma)
        
        with col2:
            st.markdown("#### SPEP Results")
            spep = df['Serum Protein Electrophoresis (SPEP)(Normal / Abnormal)'].value_counts()
            st.bar_chart(spep)
        
        with col3:
            st.markdown("#### Lymph Node Biopsy")
            lnb = df['Lymph Node Biopsy(Positive / Negative / Not Done)'].value_counts()
            st.bar_chart(lnb)
        
        st.markdown("### Diagnosis Result Distribution")
        diagnosis_dist = df['Diagnosis_Result'].value_counts()
        colors = {'Confirmed': '#27ae60', 'Suspected': '#f39c12', 'Ruled Out': '#e74c3c'}
        color_list = [colors.get(x, '#95a5a6') for x in diagnosis_dist.index]
        fig = px.pie(values=diagnosis_dist.values, names=diagnosis_dist.index,
                     title="Diagnosis Result Distribution",
                     color_discrete_sequence=color_list)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Risk Factors Analysis")
        
        st.markdown("#### Side Effects Distribution")
        side_effects = df['Side_Effects'].value_counts()
        colors_se = {'None': '#27ae60', 'Mild': '#3498db', 'Moderate': '#f39c12', 'Severe': '#e74c3c'}
        color_list = [colors_se.get(x, '#95a5a6') for x in side_effects.index]
        fig = px.bar(x=side_effects.index, y=side_effects.values,
                     title="Distribution of Side Effects",
                     labels={'x': 'Side Effect Severity', 'y': 'Number of Patients'},
                     color=side_effects.values,
                     color_discrete_sequence=color_list)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Side Effects by Treatment Type")
        side_by_treatment = pd.crosstab(
            df['Treatment_Type(Chemotherapy, Radiation)'],
            df['Side_Effects']
        )
        fig = px.bar(side_by_treatment, barmode='stack', title="Side Effects Profile by Treatment")
        st.plotly_chart(fig, use_container_width=True)
        
        # WBC count analysis
        st.markdown("#### White Blood Cell Count Analysis")
        st.metric("Average WBC Count", f"{df['Total WBC count(/cumm)'].mean():,.0f} /cumm")
        st.metric("Median WBC Count", f"{df['Total WBC count(/cumm)'].median():,.0f} /cumm")
        
        fig = px.box(df, y='Total WBC count(/cumm)', x='Treatment_Outcome',
                     title="WBC Count Distribution by Treatment Outcome",
                     color='Treatment_Outcome',
                     color_discrete_map={'Cured': '#2ecc71', 'Ongoing': '#f39c12', 'Deceased': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Key Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_patients = len(df)
            st.metric("📊 Total Patients", total_patients)
        
        with col2:
            cured = len(df[df['Treatment_Outcome'] == 'Cured'])
            st.metric("✅ Cured Patients", cured, f"{(cured/total_patients*100):.1f}%")
        
        with col3:
            ongoing = len(df[df['Treatment_Outcome'] == 'Ongoing'])
            st.metric("⏳ Ongoing Treatment", ongoing, f"{(ongoing/total_patients*100):.1f}%")
        
        with col4:
            deceased = len(df[df['Treatment_Outcome'] == 'Deceased'])
            st.metric("⚠️ Deceased", deceased, f"{(deceased/total_patients*100):.1f}%")
        
        st.markdown("---")
        
        st.markdown("### Advanced Metrics Table")
        
        metrics_data = {
            'Metric': [
                'Average Age',
                'Median Age',
                'Average WBC Count',
                'Average Platelet Count',
                'Cancer Types',
                'Treatment Types',
                'Confirmed Diagnoses',
                'Severe Side Effects'
            ],
            'Value': [
                f"{df['Age'].mean():.1f} years",
                f"{df['Age'].median():.1f} years",
                f"{df['Total WBC count(/cumm)'].mean():,.0f} /cumm",
                f"{df['Platelet Count( (/cumm)'].mean():,.0f} /cumm",
                f"{df['Cancer_Type(AML, ALL, CLL)'].nunique()} types",
                f"{df['Treatment_Type(Chemotherapy, Radiation)'].nunique()} types",
                f"{len(df[df['Diagnosis_Result'] == 'Confirmed'])} ({len(df[df['Diagnosis_Result'] == 'Confirmed'])/len(df)*100:.1f}%)",
                f"{len(df[df['Side_Effects'] == 'Severe'])} ({len(df[df['Side_Effects'] == 'Severe'])/len(df)*100:.1f}%)"
            ]
        }
        
        st.dataframe(pd.DataFrame(metrics_data), use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: TUTORIAL & HELP
# ============================================================================
def show_tutorial():
    st.markdown("## 📚 Tutorial & Help Guide")
    
    st.markdown("""
    ### 🎓 Complete Dashboard User Guide
    
    Welcome to the Blood Cancer Analysis Dashboard. This guide will help you understand 
    and use all the features effectively.
    """)
    
    # Create accordion sections for different topics
    with st.expander("🏠 **Home Page - Getting Started**", expanded=True):
        st.markdown("""
        The Home page is your entry point to the dashboard.
        
        **What to do:**
        1. Click the "Load Dataset" button to import the blood cancer data
        2. You'll see a green checkmark when data is loaded successfully
        3. The sidebar will show you basic dataset information
        
        **Key Features:**
        - Quick start guide
        - Feature overview
        - Navigation instructions
        """)
    
    with st.expander("📊 **Data Overview - Explore Your Data**"):
        st.markdown("""
        This section lets you examine the raw data and understand its structure.
        
        **Four Tabs Available:**
        
        1. **Raw Data**: View the actual dataset
           - Shows first 100 rows
           - Scroll right to see all columns
           - Click on rows to inspect values
        
        2. **Statistics**: Get numerical summaries
           - Count, mean, std, min, max for each numeric column
           - Useful for understanding data ranges
        
        3. **Column Info**: See metadata about each column
           - Column name and data type
           - Number of non-null and null values
           - Number of unique values in each column
        
        4. **Data Quality**: Assess data completeness
           - Visual representation of missing values
           - Data completeness score (higher is better)
           - Detailed missing values table
        
        **Tips:**
        - Look for columns with high missing percentages
        - Check unique values for categorical columns
        - Use statistics to identify data ranges
        """)
    
    with st.expander("🧹 **Data Cleaning - Prepare Your Data**"):
        st.markdown("""
        Data quality is crucial for accurate analysis. This section automates the cleaning process.
        
        **5 Cleaning Steps Performed:**
        
        1. **Remove Duplicates**
           - Identifies and removes exact duplicate rows
           - Prevents data from being counted twice
           - Important for accurate statistics
        
        2. **Handle Missing Values**
           - Categorical columns: Filled with mode (most common value)
           - Numeric columns: Filled with median (middle value)
           - Why median? It's not affected by extreme values
        
        3. **Standardize Categorical Data**
           - Removes extra spaces
           - Ensures consistent text values
           - Example: "AML " becomes "AML"
        
        4. **Detect Outliers**
           - Uses IQR (Interquartile Range) method
           - Flags unusual but potentially valid values
           - Helps identify data entry errors
        
        5. **Optimize Data Types**
           - Ensures numeric columns are recognized as numbers
           - Improves calculation speed
           - Prevents analysis errors
        
        **How to Use:**
        - Click "Start Data Cleaning Process"
        - Wait for the process to complete
        - Review the cleaning report
        - Download the cleaned data if needed
        
        **What You'll See:**
        - Before/After statistics
        - List of actions performed
        - Cleaned data preview
        - Download option for cleaned dataset
        """)
    
    with st.expander("📈 **Analytics - Visualize Your Data**"):
        st.markdown("""
        Explore patterns and relationships in the data through interactive visualizations.
        
        **Five Analytics Sections:**
        
        1. **Distribution** 🔍
           - Age histogram: Shows age distribution shape
           - Gender pie chart: Shows male/female ratio
           - Insights: Identify age groups and gender balance
        
        2. **Cancer Analysis** 🎯
           - Cancer type bar chart: Count by cancer type
           - Cancer by diagnosis: Cross-tabulation view
           - Insights: Which cancer types are most common?
        
        3. **Treatment** 💊
           - Treatment type distribution
           - Treatment outcomes (Cured/Ongoing/Deceased)
           - Success rate calculation
           - Insights: Which treatments work best?
        
        4. **Genetic** 🧬
           - Genetic markers distribution
           - Side effects by treatment
           - Insights: Genetic patterns in patients
        
        5. **Correlations** 🔗
           - Correlation heatmap of numeric variables
           - Age vs Platelet Count scatter plot
           - Insights: Which variables are related?
        
        **How to Interpret Charts:**
        - **Bar Charts**: Compare values across categories
        - **Pie Charts**: See parts of a whole
        - **Scatter Plots**: Look for trends or clusters
        - **Heatmaps**: Red = strong negative, Blue = strong positive
        
        **Interactive Features:**
        - Hover over data points to see exact values
        - Click legend items to show/hide data series
        - Use zoom buttons to focus on areas
        """)
    
    with st.expander("🎯 **Clinical Insights - Medical Analysis**"):
        st.markdown("""
        Deep dive into clinical outcomes and medical indicators.
        
        **Four Analysis Sections:**
        
        1. **Treatment Outcomes** 👨‍⚕️
           - Success rates by cancer type
           - Outcomes by treatment type
           - Mortality analysis
           - Best treatment recommendations
        
        2. **Diagnostic Data** 🔬
           - Bone marrow aspiration results
           - SPEP (protein) test results
           - Lymph node biopsy results
           - Diagnosis result distribution
        
        3. **Risk Analysis** ⚠️
           - Side effects severity distribution
           - Side effects by treatment type
           - WBC count analysis (lower can indicate issues)
           - Risk factor identification
        
        4. **Key Metrics** 📊
           - Overall survival statistics
           - Average clinical values
           - Key performance indicators
           - Advanced metrics table
        
        **What Each Metric Means:**
        - **WBC Count**: White blood cells (higher = stronger immune system)
        - **Platelet Count**: Blood clotting cells (lower = bleeding risk)
        - **SPEP**: Protein patterns (abnormal = possible cancer)
        - **Diagnosis Result**: Confirmed/Suspected/Ruled Out cancer
        """)
    
    with st.expander("💡 **Tips & Best Practices**"):
        st.markdown("""
        Get the most out of the dashboard with these recommendations.
        
        **General Tips:**
        - Always load data first from the Home page
        - Clean data before doing detailed analysis
        - Use multiple tabs to cross-reference information
        - Hover over charts for precise values
        
        **Analysis Tips:**
        - Start with Data Overview to understand raw data
        - Use Data Cleaning to prepare for analysis
        - Compare statistics before and after cleaning
        - Look for patterns in the Analytics section
        - Verify insights with the Clinical section
        
        **Common Questions:**
        
        Q: Why are some values filled in instead of removed?
        A: Removing rows with missing data wastes information. Filling with median/mode preserves the dataset.
        
        Q: What's the difference between "Cured" and "Ongoing"?
        A: Cured = patient recovered; Ongoing = treatment still in progress.
        
        Q: Why should I clean the data?
        A: Dirty data leads to incorrect analysis and wrong conclusions.
        
        Q: Can I use the cleaned data for my own analysis?
        A: Yes! Use the download button in the Data Cleaning section.
        """)
    
    with st.expander("🔧 **Technical Information**"):
        st.markdown("""
        Details about the dashboard's technical implementation.
        
        **Technologies Used:**
        - **Streamlit**: Web application framework
        - **Pandas**: Data manipulation and analysis
        - **Plotly**: Interactive visualizations
        - **NumPy**: Numerical computing
        - **Seaborn/Matplotlib**: Statistical graphics
        
        **Dataset Information:**
        - **File**: Blood Cancer Diseases dataset
        - **Format**: CSV (Comma-Separated Values)
        - **Records**: ~2,000+ patient records
        - **Columns**: 15+ medical and clinical attributes
        
        **Browser Requirements:**
        - Modern web browser (Chrome, Firefox, Safari, Edge)
        - JavaScript enabled
        - Good internet connection for smooth interaction
        
        **Performance Notes:**
        - Visualizations are cached for faster loading
        - Data cleaning is optimized for large datasets
        - Dashboard responsive on desktop and tablet
        """)
    
    st.markdown("---")
    
    st.markdown("### 📞 Need Help?")
    st.info("""
    **Quick Troubleshooting:**
    - **Data not loading?** Make sure the CSV file is in the correct location
    - **Charts not showing?** Try refreshing the page or clearing browser cache
    - **Slow performance?** Consider cleaning the data first
    
    **Features Overview:**
    - ✅ Automatic data cleaning
    - ✅ Interactive visualizations
    - ✅ Statistical analysis
    - ✅ Clinical insights
    - ✅ Data export capability
    - ✅ Comprehensive documentation
    """)

# ============================================================================
# RUN MAIN APP
# ============================================================================
if __name__ == "__main__":
    main()
