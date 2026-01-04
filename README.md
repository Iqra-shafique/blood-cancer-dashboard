# 🩸 Blood Cancer Diseases Analysis Dashboard

A comprehensive, interactive Streamlit dashboard for analyzing blood cancer patient data with integrated data cleaning, visualization, and clinical insights.

---

## ✨ Features

### 🏠 **Home Page**
- Quick start guide
- One-click data loading
- Feature overview
- Getting started instructions

### 📊 **Data Overview**
- Raw data exploration (first 100 rows)
- Statistical summaries (mean, median, std dev, etc.)
- Column information and data types
- Data quality assessment with visualizations
- Missing values analysis

### 🧹 **Data Cleaning & Preprocessing**
Automated cleaning process with 5 steps:
1. **Remove Duplicates** - Eliminates exact duplicate rows
2. **Handle Missing Values** - Uses median for numeric, mode for categorical
3. **Standardize Text** - Removes extra spaces from categorical data
4. **Outlier Detection** - Uses IQR method to identify unusual values
5. **Data Type Optimization** - Ensures correct data types for calculations

**Features:**
- Detailed cleaning report with metrics
- Before/After comparison
- Visual representation of changes
- Download cleaned data option

### 📈 **Analytics & Visualizations**
Five comprehensive sections with interactive charts:

1. **Distribution Analysis** 🔍
   - Age histogram
   - Gender distribution
   - Key statistics

2. **Cancer Analysis** 🎯
   - Cancer type distribution
   - Cancer type by diagnosis
   - Prevalence patterns

3. **Treatment Analysis** 💊
   - Treatment type distribution
   - Treatment outcomes (Cured/Ongoing/Deceased)
   - Success rate calculations
   - Outcome trends

4. **Genetic Analysis** 🧬
   - Genetic markers distribution
   - Side effects analysis
   - Treatment side effect profiles

5. **Correlation Analysis** 🔗
   - Correlation heatmap of numeric variables
   - Age vs Platelet Count relationship
   - Variable relationship exploration

### 🎯 **Clinical Insights**
Deep medical analysis with four sections:

1. **Treatment Outcomes** 👨‍⚕️
   - Success rates by cancer type
   - Outcomes by treatment type
   - Mortality analysis

2. **Diagnostic Data** 🔬
   - Bone marrow aspiration results
   - Serum Protein Electrophoresis (SPEP)
   - Lymph node biopsy results
   - Diagnosis distribution

3. **Risk Analysis** ⚠️
   - Side effects severity
   - WBC count analysis
   - Risk factor identification

4. **Key Metrics** 📊
   - Overall patient statistics
   - Treatment success rates
   - Advanced clinical metrics

### 📚 **Complete Tutorial & Help**
- Getting started guide
- Feature-by-feature documentation
- Tips and best practices
- Troubleshooting section
- Technical information

---

## 🚀 Quick Start

### Option 1: Automatic Setup (Windows)
1. Download all files to your computer
2. Double-click `run_dashboard.bat`
3. Wait for libraries to install (2-3 minutes first time)
4. Dashboard opens automatically in your browser

### Option 2: Manual Setup

#### Prerequisites
- Python 3.8 or higher
- pip (usually comes with Python)

#### Installation Steps

1. **Open Command Prompt or PowerShell** in the dashboard folder

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

5. **Open in browser:** 
   - Dashboard automatically opens at `http://localhost:8501`
   - If not, manually navigate to that URL

---

## 📋 System Requirements

### Hardware
- **Minimum:** 4GB RAM, 1GB disk space
- **Recommended:** 8GB RAM, 2GB disk space
- **CPU:** Any modern processor (Intel/AMD)

### Software
- **Operating System:** Windows, macOS, or Linux
- **Browser:** Chrome, Firefox, Safari, or Edge (modern versions)
- **Python:** 3.8, 3.9, 3.10, or 3.11

### Required Python Packages
- `streamlit==1.28.1` - Web framework
- `pandas==2.0.3` - Data manipulation
- `numpy==1.24.3` - Numerical computing
- `plotly==5.17.0` - Interactive charts
- `seaborn==0.12.2` - Statistical graphics
- `matplotlib==3.7.2` - Basic plotting
- `scipy==1.11.3` - Scientific computing
- `scikit-learn==1.3.1` - Machine learning tools

---

## 📖 How to Use the Dashboard

### Step 1: Load Data
1. Go to **Home** page
2. Click **"Load Dataset"** button
3. Wait for green success message
4. Sidebar shows dataset info

### Step 2: Explore Raw Data
1. Go to **Data Overview** page
2. Use tabs to view:
   - Raw data
   - Statistics
   - Column information
   - Data quality

### Step 3: Clean Data
1. Go to **Data Cleaning** page
2. Read the tutorial (optional but recommended)
3. Click **"Start Data Cleaning Process"**
4. Review the cleaning report
5. Download cleaned data if needed

### Step 4: Analyze Data
1. Go to **Analytics** page
2. Explore interactive visualizations:
   - Distribution patterns
   - Cancer type analysis
   - Treatment effectiveness
   - Genetic markers
   - Correlations
3. Hover over charts for exact values
4. Use zoom and pan controls

### Step 5: Get Clinical Insights
1. Go to **Clinical Insights** page
2. Review treatment outcomes
3. Analyze diagnostic results
4. Assess risk factors
5. Compare key metrics

### Step 6: Learn More
1. Go to **Tutorial & Help** page
2. Expand sections for detailed information
3. Read tips and best practices
4. Check troubleshooting section

---

## 🎓 Understanding Key Concepts

### Medical Tests & Values

| Test | Normal Range | What It Means |
|------|--------------|---------------|
| **WBC Count** | 4,500-11,000 /cumm | White blood cell count; infection fighting |
| **Platelet Count** | 150,000-400,000 /cumm | Blood clotting cells; bleeding risk when low |
| **Bone Marrow Aspiration** | Positive/Negative/Not Done | Test to detect cancer in bone marrow |
| **SPEP** | Normal/Abnormal | Protein patterns; abnormal suggests cancer |
| **Lymph Node Biopsy** | Positive/Negative/Not Done | Tests lymph nodes for cancer |

### Cancer Types

- **AML** - Acute Myeloid Leukemia
- **ALL** - Acute Lymphoblastic Leukemia
- **CLL** - Chronic Lymphocytic Leukemia
- **CML** - Chronic Myeloid Leukemia
- **Lymphoma** - Cancer in lymph nodes
- **Multiple Myeloma** - Cancer in plasma cells

### Treatment Types

- **Chemotherapy** - Drug-based treatment
- **Radiation** - High-energy beam treatment
- **Targeted Therapy** - Drugs targeting cancer cells
- **Immunotherapy** - Boosting immune system
- **Stem Cell Transplant** - Replacing damaged bone marrow

### Treatment Outcomes

- **Cured** - Patient achieved remission/recovery
- **Ongoing** - Treatment still in progress
- **Deceased** - Patient passed away

---

## 🧹 Data Cleaning Explained

### Why Clean Data?
- Removes errors and inconsistencies
- Improves analysis accuracy
- Prevents biased results
- Ensures valid calculations

### Cleaning Process

1. **Duplicates Removal**
   - Identifies rows that are exactly the same
   - Example: Same patient data entered twice
   - Impact: Prevents double-counting

2. **Missing Value Handling**
   - Categorical: Fill with mode (most common value)
   - Numeric: Fill with median (middle value)
   - Why median? Not affected by extreme values
   - Example: If WBC values are [1000, 2000, 3000, 100000], median is used, not mean

3. **Text Standardization**
   - Removes leading/trailing spaces
   - Ensures consistent formatting
   - Example: "AML " becomes "AML"

4. **Outlier Detection**
   - Uses IQR (Interquartile Range) method
   - Formula: Values outside Q1 - 1.5×IQR to Q3 + 1.5×IQR
   - These are flagged but kept (might be valid rare cases)

5. **Data Type Optimization**
   - Ensures numeric columns are recognized as numbers
   - Enables proper calculations
   - Improves performance

---

## 📊 Chart Interpretation Guide

### Bar Charts
- **X-axis**: Categories
- **Y-axis**: Counts or values
- **Height**: Larger bar = more cases
- **Use**: Compare values across groups

### Pie Charts
- **Slices**: Parts of a whole
- **Size**: Proportion of total
- **Percentages**: Show portion of total
- **Use**: Show distribution of categories

### Scatter Plots
- **X-axis**: First variable
- **Y-axis**: Second variable
- **Dots**: Each data point
- **Pattern**: Look for trends or clusters
- **Use**: Show relationships between variables

### Heatmaps
- **Colors**: Correlation strength
- **Red**: Negative correlation (inverse relationship)
- **Blue**: Positive correlation (same direction)
- **White/Light**: No correlation
- **Use**: Show relationships between many variables

### Box Plots
- **Center line**: Median value
- **Box**: Middle 50% of data (Q1-Q3)
- **Whiskers**: Range of data
- **Dots**: Outliers
- **Use**: Compare distributions across groups

---

## 🔧 Troubleshooting

### Problem: "Python is not installed"
**Solution:**
1. Download Python from https://www.python.org/
2. Install with "Add Python to PATH" checked
3. Restart computer
4. Try again

### Problem: Dashboard won't load
**Solution:**
1. Make sure you're on the Home page first
2. Click "Load Dataset" button
3. Wait for green success message
4. Then navigate to other pages

### Problem: Charts not displaying
**Solution:**
1. Refresh the browser (F5)
2. Clear browser cache
3. Try a different browser
4. Restart the dashboard

### Problem: Slow performance
**Solution:**
1. Go to Data Cleaning page
2. Click "Start Data Cleaning Process"
3. Use cleaned data for analysis
4. Close other browser tabs
5. Reduce number of data points in visualization

### Problem: Can't download cleaned data
**Solution:**
1. Make sure you've run the cleaning process
2. Check browser download settings
3. Ensure you have write permissions
4. Try a different browser

---

## 🎨 Customization

### Change Dashboard Theme
Edit the CSS section in `dashboard.py` (lines 25-45)

### Add More Visualizations
Modify the `show_analytics()` function to add custom charts

### Adjust Color Schemes
Change `color_discrete_sequence` and `color_discrete_map` parameters

### Add New Metrics
Extend the `show_clinical_insights()` function

---

## 📝 File Structure

```
Assignment/
├── Blood Cancer Diseases dataset - Sheet1.csv  (Main data file)
├── dashboard.py                                (Main application)
├── requirements.txt                            (Python dependencies)
├── run_dashboard.bat                           (Windows launcher)
└── README.md                                   (This file)
```

---

## 💻 Advanced Usage

### For Developers

#### Modify Data Cleaning Logic
Edit the `clean_data()` function in `dashboard.py`

#### Add Custom Visualizations
Use Plotly Express for interactive charts:
```python
fig = px.scatter(df, x='Age', y='Platelet Count( (/cumm)')
st.plotly_chart(fig)
```

#### Change Caching Strategy
Modify `@st.cache_data` decorators for different refresh rates

### For Data Scientists

#### Export Cleaned Data
Click download button in Data Cleaning page

#### Use with Other Tools
Combine cleaned data with Jupyter Notebooks, R, or other tools

#### Statistical Analysis
Extend the Clinical Insights page with custom statistics

---

## 📜 License & Usage

This dashboard is designed for educational and clinical research purposes.

**Use responsibly:**
- Respect patient privacy
- Don't share sensitive data
- Follow HIPAA guidelines if applicable
- Use insights ethically

---

## 🤝 Support & Feedback

### Common Questions

**Q: Why isn't my data loading?**
A: Ensure the CSV file is in the correct location as specified in the code.

**Q: Can I modify the data?**
A: Yes, use the Data Overview page to see raw data and download cleaned versions.

**Q: How often is the dashboard updated?**
A: Visualizations refresh each time you interact with controls.

**Q: Can I use this for production?**
A: Yes, with proper security measures and HIPAA compliance.

---

## 🚀 Performance Tips

1. **Clean data first** - Reduces chart loading time
2. **Use filters** - Focus on relevant data subsets
3. **Close unused tabs** - Reduces memory usage
4. **Clear cache** - Fixes display issues
5. **Use modern browser** - Better performance

---

## 📚 Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Plotly Docs**: https://plotly.com/python/
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Medical Terminology**: Consult medical professionals

---

## ✅ Checklist Before Using

- [ ] Python 3.8+ installed
- [ ] All libraries installed from requirements.txt
- [ ] CSV file in correct location
- [ ] Read the Tutorial & Help section
- [ ] Started with Home page
- [ ] Loaded dataset successfully

---

**Version:** 1.0  
**Last Updated:** January 2026  
**Author:** Data Analysis Team  

🎉 **Ready to analyze blood cancer data? Start the dashboard and begin exploring!**
