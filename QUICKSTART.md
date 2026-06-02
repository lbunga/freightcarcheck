# 🚂 FreightcarchecK - Quick Start Guide

## 60-Second Setup

### Windows

#### Option 1: Automated (Easiest)
```powershell
cd c:\Users\Sunny\Documents\Trevo\workspace\freightcarcheck
run.bat
```

#### Option 2: Manual
```powershell
# Install dependencies
python -m pip install --user -r requirements.txt

# Generate sample data
python data_generator.py

# Validate installation
python validate.py

# Launch app
python -m streamlit run app.py
```

### macOS / Linux

```bash
cd ~/Documents/Trevo/workspace/freightcarcheck

# Install dependencies (use venv recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate sample data
python3 data_generator.py

# Validate installation
python3 validate.py

# Launch app
python3 -m streamlit run app.py
```

The app will automatically open at **http://localhost:8501**

---

## What You Get

### ✅ Dashboard Tab
- **Real-time KPIs**: 150 cars, ~10,000 tons, ~27 hazmat cars, braking ratios
- **Visual charts**: Cargo breakdown (hazmat vs safe), weight distribution, car types
- **Hazmat analysis**: DOT Class 1-9 breakdown with tonnage

### ✅ Manifest Table Tab
- **Searchable manifest**: 150 cars with all details (car ID, type, weight, cargo, hazmat class, UN code, route)
- **Smart filters**: Hazmat-only toggle, car type selection, hazmat class filtering
- **Color-coded**: Red rows = hazmat, green rows = safe cargo

### ✅ Train Layout Tab
- **Interactive train diagram**: 150 cars rendered as horizontal bars
- **Color-coding**: Red = hazmat, green = safe (matches table)
- **Hover details**: See car info on hover
- **Hazmat distribution chart**: Visual breakdown by DOT class

---

## Validation Results ✅

```
Imports................................. ✅ PASS
Data Generation......................... ✅ PASS
Data Loading............................ ✅ PASS
Filters................................. ✅ PASS

Sample Data:
- 3 realistic 150-car trains
- ~27 hazmat cars per train (~18%)
- ~10,300 tons per train
- Realistic car types: flat, tank, gondola, hopper, box
- Realistic hazmat: Classes 3, 4, 5, 6, 8, 9 with UN codes
```

---

## Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application (starts here!) |
| `models.py` | Data structures (Train, Car, Cargo) |
| `data_generator.py` | Generates realistic 150-car manifests |
| `validate.py` | Tests all components |
| `utils/` | Helper modules (calculations, filters, visualizations) |
| `data/sample_trains.json` | 3 sample trains (auto-generated) |
| `.streamlit/config.toml` | Streamlit settings |
| `README.md` | Full documentation |
| `requirements.txt` | Python dependencies |

---

## Troubleshooting

### 1. "No module named streamlit"
```bash
python -m pip install --user streamlit pandas plotly numpy
```

### 2. "sample_trains.json not found"
```bash
python data_generator.py
```

### 3. Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

### 4. Using virtual environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # macOS/Linux
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## Features Overview

### For Train Conductors 🚂
- ✅ Audit train composition before departure
- ✅ Verify hazmat placements and UN codes
- ✅ Check weight distribution for grade climbing

### For First Responders 👨‍🚒
- ✅ Rapid hazmat assessment during incidents
- ✅ Identify safe evacuation zones
- ✅ Quick tonnage data for rescue planning

### For Safety Teams 🛡️
- ✅ Pre-departure safety audits
- ✅ Regulatory compliance (DOT, FRA)
- ✅ Train handling optimization

---

## Key Metrics Explained

| Metric | What It Means | Why It Matters |
|--------|--------------|----------------|
| **Total Tonnage** | Sum of all car + cargo weights | Affects fuel efficiency, braking power |
| **Hazmat Tonnage** | Weight of dangerous materials only | For emergency planning |
| **Braking Ratio** | Hazmat weight / Total weight | Critical on steep grades (prevents train break-in-two) |
| **Weight Distribution** | Front/middle/rear percentages | Locomotive strain, coupling stress |
| **Hazmat Count** | Number of cars with hazardous cargo | For emergency responder preparation |

---

## Next Steps

1. **Run the app**: `python -m streamlit run app.py`
2. **Explore the Dashboard**: Check KPIs and charts
3. **Filter the Manifest**: Try search, hazmat toggle, car type filters
4. **View Train Layout**: See the 150-car visual diagram
5. **Read full docs**: Open `README.md` for detailed information

---

## Need Help?

- 📖 **Full Documentation**: See `README.md`
- 🧪 **Run Validation**: `python validate.py`
- 🔧 **Generate Data**: `python data_generator.py`
- 💬 **Contact**: Reach out to the development team

---

## Technical Stack

- **Language**: Python 3.10+
- **UI Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Data Format**: JSON (embedded in app)

---

🎉 **FreightcarchecK v1.0** - Ready for POC validation!

**Estimated first run**: 2-3 minutes (app loads at http://localhost:8501)
