# Using Python with Tableau

This small project includes two practical ways to "import Python to Tableau":

1) Real-time Python analytics from Tableau using TabPy (Tableau Python Server).
   - Tableau Desktop/Server connects to a running TabPy server and calls deployed Python functions.
2) Export data from Python into a Tableau `.hyper` extract using the Tableau Hyper API.
   - Tableau reads the `.hyper` file as a datasource.

Files included
- `requirements.txt` — Python packages to install.
- `sample_data.csv` — tiny sample dataset.
- `tabpy_register.py` — example that deploys a simple function to a running TabPy server.
- `hyper_example.py` — example that converts `sample_data.csv` into `sample.hyper`.
- `create_dashboard.py` — creates a template Tableau dashboard (.twb) programmatically using Python.

Quick setup (macOS, zsh)

1) Create a Python virtual environment and install packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Start TabPy server (in a separate terminal):

```bash
# after installing tabpy
tabpy
# TabPy default listens on http://localhost:9004
```

3) Register the example function with TabPy:

```bash
python tabpy_register.py
```

4) In Tableau Desktop, connect TabPy:
- Help → Settings and Performance → Manage External Service Connection
- Choose "TabPy/External API", server `localhost`, port `9004`, Test Connection.

5) Use the deployed function in Tableau with a calculated field. Example using SCRIPT_REAL:

```
SCRIPT_REAL(
  "return tabpy.query('multiply_by_two', _arg1)['response']",
  SUM([YourNumericField])
)
```

6) Create a Tableau dashboard template programmatically:

```bash
python create_dashboard.py
# creates template_dashboard.twb connected to sample.hyper
```

7) Open the generated workbook in Tableau Desktop:

```bash
open template_dashboard.twb
# or drag the file into Tableau Desktop
```

The template dashboard includes:
- 3 pre-configured worksheets (Bar Chart, Data Table, Summary)
- A dashboard with a 3-zone layout (title, chart, tables)
- Connection to the sample.hyper data source

Notes & next steps
- If you want Tableau Server to call Python, run TabPy on a server reachable by Tableau and secure it.
- The examples are intentionally minimal. I can extend them to demonstrate vectorized functions, examples using model prediction (scikit-learn), or automated workbook generation.

Requirements coverage
- Show how to call Python from Tableau (TabPy): covered.
- Show how to export Python data to Tableau (Hyper): covered.

If you want, I can now run a quick smoke-check (create virtualenv and run `hyper_example.py`) here — tell me if you want me to run installs and execute the examples locally now.
