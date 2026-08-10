from http.server import BaseHTTPRequestHandler
import urllib.parse
import json
import requests
import os

CLIENT_ID = "1535841871429902426"
CLIENT_SECRET = "xK09uuQrG7NJV0Jv7H11Pb5GLhUZIdqA"
REDIRECT_URI = "https://your-vercel-domain.vercel.app/callback" 

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        code = query_params.get("code", [None])[0]
        
        if not code:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>잘못된 접근입니다. 인증 코드가 없습니다.</h1>".encode('utf-8'))
            return

        token_url = "https://discord.com/api/oauth2/token"
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        resp = requests.post(token_url, data=payload, headers=headers)
        if resp.status_code != 200:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>디스코드 토큰 발급에 실패했습니다.</h1>".encode('utf-8'))
            return
            
        token_data = resp.json()
        access_token = token_data.get("access_token")
        
        user_resp = requests.get("https://discord.com/api/users/@me", headers={"Authorization": f"Bearer {access_token}"})
        if user_resp.status_code != 200:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>유저 정보 조회에 실패했습니다.</h1>".encode('utf-8'))
            return
            
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html_content = """
        <html>
            <head><meta charset="utf-8"><title>인증 완료</title></head>
            <body style="text-align: center; font-family: sans-serif; margin-top: 50px;">
                <h1 style="color: #2ecc71;">✨ 인증이 성공적으로 완료되었습니다!</h1>
                <p>디스코드 창으로 돌아가셔도 됩니다. 창을 닫으세요.</p>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))