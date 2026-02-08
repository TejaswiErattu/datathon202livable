# Quick Start Guide: Python + Tableau Dashboard

## What was created

1. **Data Pipeline**
   - `sample_data.csv` → Python → `sample.hyper` (Tableau extract)
   - Script: `hyper_example.py`

2. **Dashboard Template** 
   - `template_dashboard.twb` — Programmatically generated Tableau workbook
   - Script: `create_dashboard.py`
   - Contains: 3 worksheets + 1 dashboard with layout zones

3. **TabPy Integration**
   - Deploy Python functions callable from Tableau
   - Script: `tabpy_register.py`

## Run the complete workflow

```bash
# 1. Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Generate Hyper extract from CSV
python3 hyper_example.py
# Output: sample.hyper

# 3. Create dashboard template
python3 create_dashboard.py
# Output: template_dashboard.twb

# 4. Open in Tableau Desktop
open template_dashboard.twb
```

## Dashboard Structure

The generated `template_dashboard.twb` includes:

### Worksheets
- **Bar Chart** — Ready for categorical analysis
- **Data Table** — Grid view of data
- **Summary** — KPIs and statistics

### Dashboard Layout
```
┌─────────────────────────────────┐
│        Title Zone (top)         │
├──────────────────┬──────────────┤
│                  │              │
│   Bar Chart      │ Data Table   │
│   (left, 50%)    │ (right-top)  │
│                  ├──────────────┤
│                  │   Summary    │
│                  │ (right-bot)  │
└──────────────────┴──────────────┘
```

### Data Fields Available
From `sample.hyper`:
- `id` (dimension, integer)
- `value` (measure, integer)
- `name` (dimension, string)

## Customizing the Dashboard

### Option 1: Via Tableau Desktop UI
1. Open `template_dashboard.twb`
2. Drag fields to worksheet shelves
3. Add filters, colors, tooltips
4. Rearrange dashboard zones

### Option 2: Modify Python Script
Edit `create_dashboard.py` to:
- Add more worksheets
- Change dashboard layout dimensions
- Add calculated fields
- Configure default mark types

Example: Add a new worksheet
```python
# In create_dashboard.py, add after existing worksheets:
worksheet4 = ET.SubElement(worksheets, 'worksheet', {'name': 'Trend Line'})
view4 = ET.SubElement(worksheet4, 'view')
ET.SubElement(view4, 'label').text = 'Trend Analysis'
```

## TabPy Live Analytics (Optional)

To call Python functions from Tableau in real-time:

```bash
# Terminal 1: Start TabPy server
source .venv/bin/activate
tabpy

# Terminal 2: Deploy function
python3 tabpy_register.py
```

Then in Tableau calculated field:
```
SCRIPT_REAL(
  "return tabpy.query('multiply_by_two', _arg1)['response']",
  SUM([value])
)
```

## File Summary

| File | Purpose | Output |
|------|---------|--------|
| `hyper_example.py` | CSV → Hyper conversion | `sample.hyper` |
| `create_dashboard.py` | Generate workbook XML | `template_dashboard.twb` |
| `tabpy_register.py` | Deploy Python function | TabPy endpoint |
| `sample_data.csv` | Sample dataset | - |
| `requirements.txt` | Python dependencies | - |

## Next Steps

- **Add more data**: Modify `sample_data.csv` or point to a different CSV
- **Complex viz**: Edit worksheets in Tableau Desktop to add charts
- **Automation**: Schedule `hyper_example.py` + `create_dashboard.py` for daily refreshes
- **ML Integration**: Use TabPy to deploy scikit-learn models for predictions
- **Publish**: Upload to Tableau Server/Online for sharing

## Troubleshooting

**Dashboard won't open?**
- Ensure `sample.hyper` exists in the same directory
- Check Tableau Desktop version compatibility (2023.3+)

**Data not showing?**
- Verify the Hyper file path is absolute in the .twb
- Re-run `hyper_example.py` if data changed

**TabPy connection fails?**
- Check TabPy is running: `curl http://localhost:9004/info`
- Verify firewall settings
