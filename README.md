# FreightcarchecK - Heavy Haul Manifest Viewer

## Overview

**FreightcarchecK** is an intuitive Python/Streamlit application designed for Train conductors , Safety Team and first responders to quickly access freight train manifests during emergencies. 

### Problem it Solves
- 🚂 A 150-car freight train can weigh over 18,000 tons and stretch over two miles
- 📋 Crews receive massive text-heavy manifest documents ("consists")
- ⏰ In emergencies (derailments, stuck brakes), seconds matter
- ⚠️ First responders need instant hazmat location data to establish safe evacuation perimeters

### Key Features
✅ **Dashboard** - Real-time KPIs: total cars, tonnage, hazmat count, braking ratios  
✅ **Manifest Table** - Searchable, filterable cargo database with hazmat highlighting  
✅ **Train Layout** - Visual 150-car train diagram with hazmat color-coding (red=hazmat, green=safe)  
✅ **Hazmat Analysis** - DOT Class 1-9 breakdown, UN codes, tonnage calculations  
✅ **Weight Distribution** - Front/middle/rear balance analysis for braking optimization  

---

## Features in Detail

### 📊 Dashboard Tab
- **KPI Cards**: Total cars (150), tonnage (~10,000 tons), hazmat count (~27 cars), braking ratio
- **Cargo Breakdown**: Pie chart showing hazmat vs. safe cargo tonnage
- **Weight Distribution**: Front/middle/rear percentages (important for grade climbing)
- **Hazmat Summary**: Table of hazmat by DOT class, car count, and tonnage
- **Car Type Distribution**: Bar chart of flat cars, tank cars, gondolas, hoppers, boxcars

### 📋 Manifest Table Tab
- **Real-time Filters**:
  - 🔍 Search by car ID, cargo description, origin, destination
  - ☑️ Hazmat-only toggle
  - 📦 Car type multiselect (flat, tank, gondola, etc.)
  - ⚠️ Hazmat class filter (Classes 1-9)
- **Color-Coded Rows**: Red = hazmat, green = safe cargo
- **Full Car Details**: Position, car ID, type, weight, cargo, hazmat class, UN code, route

### 🚃 Train Layout Tab
- **Interactive Horizontal Diagram**: 150 cars rendered as color-coded bars
- **Hover Details**: Car ID, position, weight, cargo, hazmat status on hover
- **Hazmat Distribution Chart**: Bar chart showing hazmat class breakdown
- **Hazmat Details**: Tonnage and car count per class

---

## Use Cases

### 🚂 Train Conductors
- Quick audit of train composition before departure
- Verify hazmat placements and UN codes
- Check weight distribution for grade climbing

### 👨‍🚒 First Responders
- Rapid hazmat assessment during derailment/incident
- Identify safe evacuation zones based on hazmat class
- Quick tonnage data for rescue operation planning

### 🛡️ Safety Teams
- Pre-departure safety audits
- Regulatory compliance documentation (DOT, FRA)
- Train handling optimization for steep grades

---

## Installation & Setup

### Requirements
- Python 3.10+ (3.14 tested)
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

If you encounter permission issues on Windows, add `--user` flag:
```bash
pip install --user -r requirements.txt
```

### Step 2: Generate Sample Data
```bash
python data_generator.py
```

This creates 3 realistic 150-car train manifests in `data/sample_trains.json`.

### Step 3: Run the Application
```bash
python -m streamlit run app.py
```

The app will launch at **http://localhost:8501** in your default browser.

---

## Project Structure

```
freightcarcheck/
├── app.py                    # Main Streamlit application
├── models.py                 # Data classes (Train, Car, Cargo, HazmatInfo)
├── data_generator.py         # Realistic sample data generation
├── requirements.txt          # Python dependencies
├── .gitignore
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py        # Load and parse train JSON data
│   ├── calculations.py       # Tonnage, braking ratio, weight distribution
│   ├── filters.py            # Search and hazmat filtering
│   └── visualizations.py     # Plotly charts and train layout diagrams
│
├── data/
│   └── sample_trains.json    # 3 auto-generated 150-car train manifests
│
└── .streamlit/
    └── config.toml           # Streamlit UI configuration
```



## Sample Data Format

Each train manifest includes 150 cars with realistic distributions:

```json
{
  "train_id": "TRAIN-28074",
  "cars": [
    {
      "car_id": "FLAT-00001",
      "car_type": "flat",
      "capacity_tons": 80,
      "position": 1,
      "cargo": {
        "description": "Grain",
        "weight_tons": 35.5,
        "hazmat_info": {
          "is_hazmat": false,
          "hazmat_class": null,
          "un_code": null,
          "description": ""
        },
        "origin": "Chicago, IL",
        "destination": "New York, NY"
      }
    },
    {
      "car_id": "TANK-00002",
      "car_type": "tank",
      "capacity_tons": 150,
      "position": 2,
      "cargo": {
        "description": "Flammable Liquids (Class 3)",
        "weight_tons": 25.0,
        "hazmat_info": {
          "is_hazmat": true,
          "hazmat_class": 3,
          "un_code": "UN1072",
          "description": "Flammable Liquids (Class 3)"
        },
        "origin": "Houston, TX",
        "destination": "San Francisco, CA"
      }
    }
  ],
  "manifest_date": "2026-05-31T...",
  "total_cars": 150,
  "total_weight_tons": 10325.58
}
```

---

## Hazmat Classification (DOT Standard)

| Class | Category | Example | Color |
|-------|----------|---------|-------|
| 1 | Explosives | TNT, dynamite | 🔴 Red |
| 2 | Gases | Propane, oxygen | 🔴 Red |
| 3 | Flammable Liquids | Gasoline, paint thinner | 🔴 Red |
| 4 | Flammable Solids | Matches, phosphorus | 🔴 Red |
| 5 | Oxidizers | Chlorine, fertilizers | 🔴 Red |
| 6 | Toxic Substances | Poisons, pesticides | 🔴 Red |
| 7 | Radioactive | Uranium (low-level) | 🔴 Red |
| 8 | Corrosives | Sulfuric acid | 🔴 Red |
| 9 | Miscellaneous | PCBs, batteries | 🔴 Red |

---

## Key Calculations

### Tonnage
- **Total Tonnage** = Sum of all (car weight + cargo weight)
  - Flat cars: ~30 tons, Tank cars: ~140 tons, Gondolas: ~38 tons
  
### Hazmat Tonnage
- **Hazmat Weight** = Sum of hazmat cargo only (not car weight)

### Braking Ratio
- **Ratio** = Hazmat Tonnage / Total Tonnage
- Critical for determining train dynamics on grades
- Higher ratio = more braking force needed

### Weight Distribution
- **Front (cars 1-50)**: % of total
- **Middle (cars 51-100)**: % of total
- **Rear (cars 101-150)**: % of total
- Important for preventing "train break-in-two" on steep grades

---

## Testing & Validation

### Run Unit Tests (Optional - Manual Validation)
```bash
# Test data generation
python data_generator.py
# Expected output: Generated 3 sample trains with ~27 hazmat cars each

# Test imports
python -c "from models import Train, Car; from utils.calculations import calculate_total_tonnage; print('✓ All imports successful')"
```

### Verify Application Launch
1. Run `python -m streamlit run app.py`
2. Browser opens at `http://localhost:8501`
3. Sidebar shows "Train Selection" dropdown
4. Dashboard tab shows KPI cards (verify totals are > 0)
5. Manifest Table shows all 150 cars with realistic data
6. Train Layout tab displays horizontal train diagram with color-coding
7. All filters work (search, hazmat toggle, car types, hazmat classes)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Reinstall with correct Python:
```bash
python -m pip install --user streamlit pandas plotly numpy
```

Or use a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

### Data not loading in app
**Solution**: Run `python data_generator.py` first to create `data/sample_trains.json`

### Charts not rendering
**Solution**: Ensure Plotly is installed:
```bash
pip install --user --upgrade plotly
```

### Port 8501 already in use
**Solution**: Run on a different port:
```bash
streamlit run app.py --server.port 8502
```

---

## Future Enhancements (v2.0+)

- 📤 location based train consist data
- 🗺️ Real corridor data (Colorado mountain grades, Tehachapi Pass, Cajon Pass)
- 🚨 Emergency response mode (lightweight UI, hazmat-only view, large text)
- 📱 Mobile app version for first responders
- 🔗 API integration with rail dispatch systems
- 📊 Historical manifest comparison and trending

---



## License & Attribution
FreightcarchecK v1.0 — MIT License © 2026. Built with Python, Streamlit, Plotly, Pandas, NumPy.

**Quick Links:**
- 📖 [Streamlit Documentation](https://docs.streamlit.io/)
- 🎨 [Plotly Documentation](https://plotly.com/python/)
- 🚂 [FRA Hazmat Guidelines](https://railroads.dot.gov/)
