# 🩸 Blood Cancer Dashboard - Installation Guide

## 🚀 Quick Start (Choose One Method)

### **Method 1: Easiest (Windows Batch File)**
1. Double-click `run_dashboard.bat`
2. Wait for libraries to install (2-3 minutes first time)
3. Dashboard opens automatically ✅

---

### **Method 2: Python Script (All Platforms)**
1. Open Command Prompt/PowerShell in this folder
2. Run: `python run_dashboard.py`
3. Dashboard opens automatically ✅

---

### **Method 3: Manual Installation (Full Control)**

#### Step 1: Verify Python Installation
```bash
python --version
```
- Must show Python 3.8 or higher
- If not installed, download from https://www.python.org/

#### Step 2: Install Libraries
```bash
# First, upgrade pip
python -m pip install --upgrade pip

# Then install all requirements
pip install -r requirements.txt
```

#### Step 3: Launch Dashboard
```bash
streamlit run dashboard.py
```

#### Step 4: Open in Browser
- Automatically opens at: `http://localhost:8501`
- If not, manually navigate to that URL

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Python is installed (version 3.8+)
- [ ] All libraries installed without errors
- [ ] Dashboard runs without errors
- [ ] Browser opens automatically
- [ ] Home page displays correctly
- [ ] "Load Dataset" button works
- [ ] Data loads successfully

---

## 🔧 Troubleshooting Installation

### **Error: "python: command not found"**
- **Cause**: Python not in system PATH
- **Solution**: 
  1. Reinstall Python
  2. Check "Add Python to PATH" during installation
  3. Restart computer

### **Error: "pip: command not found"**
- **Cause**: pip not installed
- **Solution**: `python -m pip --version` and then use `python -m pip` instead of `pip`

### **Error: "Module not found" (e.g., streamlit)**
- **Cause**: Libraries not installed
- **Solution**: Run `pip install -r requirements.txt` again

### **Error: "Port 8501 already in use"**
- **Cause**: Dashboard already running
- **Solution**: 
  1. Close other Streamlit instances
  2. Or change port: `streamlit run dashboard.py --server.port 8502`

### **Error: "CSV file not found"**
- **Cause**: Data file in wrong location
- **Solution**: Ensure "Blood Cancer Diseases dataset  - Sheet1.csv" is in same folder as dashboard.py

### **Dashboard loads but won't display content**
- **Solution**:
  1. Refresh browser (F5)
  2. Clear browser cache
  3. Restart dashboard
  4. Try different browser

---

## 📋 System Requirements

### Minimum
- Windows 7+, macOS 10.12+, or Linux
- Python 3.8+
- 4GB RAM
- 500MB disk space

### Recommended
- Windows 10+, macOS 10.15+, or modern Linux
- Python 3.9+
- 8GB RAM
- 2GB disk space
- Modern browser (Chrome, Firefox, Edge, Safari)

---

## 📦 What Gets Installed

The `requirements.txt` file installs:

```
✓ streamlit - Interactive web framework
✓ pandas - Data manipulation
✓ numpy - Numerical computing
✓ plotly - Interactive charts
✓ seaborn - Statistical graphics
✓ matplotlib - Basic plots
✓ scipy - Scientific computing
✓ scikit-learn - Machine learning
```

Total size: ~300-500MB

---

## 🆘 Getting Help

### If installation fails:
1. Check Python version: `python --version`
2. Try upgrading pip: `python -m pip install --upgrade pip`
3. Try installing one package at a time: `pip install streamlit`
4. Check internet connection
5. Try a different terminal/command prompt

### If dashboard won't run:
1. Make sure CSV file exists
2. Check file path in dashboard.py (line 408)
3. Try restart computer
4. Reinstall packages

### Still stuck?
1. Read README.md for detailed information
2. Check Streamlit docs: https://docs.streamlit.io/
3. Try example code first

---

## 🎉 Success!

Once installed successfully:
1. Dashboard opens automatically at startup
2. Click "Load Dataset" on Home page
3. Explore all features
4. Check Tutorial & Help for detailed guides

**You're ready to analyze blood cancer data! 🩸**

---

**Estimated Installation Time**: 3-5 minutes (first time)  
**Subsequent Launches**: 5-10 seconds

Happy analyzing! 📊
