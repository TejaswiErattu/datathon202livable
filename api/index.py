from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AirRisk Dashboard - Deployment Notice</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; margin-bottom: 20px; }
                p { color: #666; line-height: 1.6; margin-bottom: 20px; }
                .notice { background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
                .github-link { background: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌬️ AirRisk Dashboard</h1>
                <p><strong>Professional Air Quality Intelligence Platform</strong></p>
                <p>EPA Air Quality Index analysis across US counties (2021-2024)</p>
                
                <div class="notice">
                    <h3>📋 Deployment Notice</h3>
                    <p>This Streamlit dashboard is optimized for local development and specialized hosting platforms that support Python applications with persistent processes.</p>
                </div>
                
                <h3>🚀 To run locally:</h3>
                <p>1. Clone the repository<br>
                2. Install requirements: <code>pip install -r requirements.txt</code><br>
                3. Run: <code>streamlit run streamlit_dashboard/app.py</code></p>
                
                <a href="https://github.com/TejaswiErattu/datathon202livable" class="github-link">View Source Code</a>
                
                <p style="margin-top: 30px; color: #888; font-size: 14px;">
                    Author: Tejaswi Erattutaj | Datathon 2026
                </p>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
