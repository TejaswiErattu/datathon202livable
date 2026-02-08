"""
Create a Tableau workbook (.twb) programmatically using Python
This script generates a template dashboard connected to the sample.hyper file
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def create_tableau_workbook(hyper_file_path: str, output_twb_path: str):
    """
    Create a basic Tableau workbook XML with a dashboard template.
    
    Args:
        hyper_file_path: Path to the .hyper data source
        output_twb_path: Path where the .twb file will be saved
    """
    
    # Create the root workbook element
    workbook = ET.Element('workbook', {
        'source-build': '2023.3.0 (20233.23.1017.1841)',
        'source-platform': 'mac',
        'version': '18.1',
        'xmlns:user': 'http://www.tableausoftware.com/xml/user'
    })
    
    # Add preferences
    preferences = ET.SubElement(workbook, 'preferences')
    
    # Add datasources section
    datasources = ET.SubElement(workbook, 'datasources')
    
    # Create the main datasource pointing to the Hyper file
    datasource = ET.SubElement(datasources, 'datasource', {
        'caption': 'Sample Data (sample)',
        'inline': 'true',
        'name': 'federated.1abc123',
        'version': '18.1'
    })
    
    # Add connection to Hyper file
    connection = ET.SubElement(datasource, 'connection', {
        'class': 'hyper',
        'dbname': os.path.abspath(hyper_file_path),
        'default-settings': 'yes',
        'schema': 'Extract',
        'tablename': 'Extract'
    })
    
    # Add relation (table reference)
    relation = ET.SubElement(connection, 'relation', {
        'name': 'Extract',
        'table': '[Extract].[Extract]',
        'type': 'table'
    })
    
    # Add metadata for columns
    metadata_records = ET.SubElement(datasource, 'metadata-records')
    
    # Define columns based on sample_data.csv structure
    columns = [
        {'name': 'id', 'datatype': 'integer', 'role': 'dimension', 'type': 'ordinal'},
        {'name': 'value', 'datatype': 'integer', 'role': 'measure', 'type': 'quantitative'},
        {'name': 'name', 'datatype': 'string', 'role': 'dimension', 'type': 'nominal'}
    ]
    
    for idx, col in enumerate(columns):
        metadata_record = ET.SubElement(metadata_records, 'metadata-record', {
            'class': 'column'
        })
        ET.SubElement(metadata_record, 'remote-name').text = col['name']
        ET.SubElement(metadata_record, 'remote-type').text = '20' if col['datatype'] == 'integer' else '129'
        ET.SubElement(metadata_record, 'local-name').text = f"[{col['name']}]"
        ET.SubElement(metadata_record, 'parent-name').text = '[Extract]'
        ET.SubElement(metadata_record, 'remote-alias').text = col['name']
        ET.SubElement(metadata_record, 'ordinal').text = str(idx)
        ET.SubElement(metadata_record, 'local-type').text = col['datatype']
        ET.SubElement(metadata_record, 'aggregation').text = 'Sum' if col['role'] == 'measure' else 'Count'
        ET.SubElement(metadata_record, 'contains-null').text = 'true'
    
    # Add layout for columns
    layout = ET.SubElement(datasource, 'layout', {'dim-ordering': 'alphabetic', 'dim-percentage': '0.5', 'measure-ordering': 'alphabetic', 'measure-percentage': '0.4', 'show-structure': 'true'})
    
    # Add worksheets section
    worksheets = ET.SubElement(workbook, 'worksheets')
    
    # Create Sheet 1: Bar Chart
    worksheet1 = ET.SubElement(worksheets, 'worksheet', {'name': 'Bar Chart'})
    view1 = ET.SubElement(worksheet1, 'view')
    ET.SubElement(view1, 'label').text = 'Bar Chart'
    
    # Create Sheet 2: Data Table
    worksheet2 = ET.SubElement(worksheets, 'worksheet', {'name': 'Data Table'})
    view2 = ET.SubElement(worksheet2, 'view')
    ET.SubElement(view2, 'label').text = 'Data Table'
    
    # Create Sheet 3: Summary Stats
    worksheet3 = ET.SubElement(worksheets, 'worksheet', {'name': 'Summary'})
    view3 = ET.SubElement(worksheet3, 'view')
    ET.SubElement(view3, 'label').text = 'Summary Statistics'
    
    # Add windows (for display)
    windows = ET.SubElement(workbook, 'windows')
    window = ET.SubElement(windows, 'window', {
        'class': 'dashboard',
        'name': 'Dashboard 1'
    })
    
    # Add dashboards section
    dashboards = ET.SubElement(workbook, 'dashboards')
    dashboard = ET.SubElement(dashboards, 'dashboard', {'name': 'Dashboard 1'})
    
    # Dashboard size and layout
    ET.SubElement(dashboard, 'style')
    size = ET.SubElement(dashboard, 'size', {'maxheight': '800', 'maxwidth': '1000', 'minheight': '800', 'minwidth': '1000'})
    
    # Dashboard zones (layout containers)
    zones = ET.SubElement(dashboard, 'zones')
    
    # Top zone for title
    zone_title = ET.SubElement(zones, 'zone', {'h': '100', 'id': '1', 'type': 'text', 'w': '1000', 'x': '0', 'y': '0'})
    ET.SubElement(zone_title, 'zone-style').text = 'padding:8'
    
    # Left zone for bar chart
    zone_chart = ET.SubElement(zones, 'zone', {'h': '700', 'id': '2', 'name': 'Bar Chart', 'type': 'layout-basic', 'w': '500', 'x': '0', 'y': '100'})
    
    # Right zone split into two
    zone_table = ET.SubElement(zones, 'zone', {'h': '350', 'id': '3', 'name': 'Data Table', 'type': 'layout-basic', 'w': '500', 'x': '500', 'y': '100'})
    zone_summary = ET.SubElement(zones, 'zone', {'h': '350', 'id': '4', 'name': 'Summary', 'type': 'layout-basic', 'w': '500', 'x': '500', 'y': '450'})
    
    # Format and pretty print the XML
    xml_str = ET.tostring(workbook, encoding='utf-8', method='xml')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8')
    
    # Write to file
    with open(output_twb_path, 'wb') as f:
        f.write(pretty_xml)
    
    print(f"Created Tableau workbook: {output_twb_path}")
    print(f"Connected to data source: {os.path.abspath(hyper_file_path)}")
    print("\nNext steps:")
    print(f"1. Open '{output_twb_path}' in Tableau Desktop")
    print("2. The workbook contains:")
    print("   - Dashboard 1 (template with 3 zones)")
    print("   - Bar Chart worksheet")
    print("   - Data Table worksheet")
    print("   - Summary worksheet")
    print("3. Drag fields to build visualizations or use the pre-configured dashboard")


if __name__ == '__main__':
    # Ensure sample.hyper exists
    hyper_file = 'sample.hyper'
    if not os.path.exists(hyper_file):
        print(f"Error: {hyper_file} not found. Run 'python hyper_example.py' first.")
        exit(1)
    
    # Create the workbook
    create_tableau_workbook(hyper_file, 'template_dashboard.twb')
