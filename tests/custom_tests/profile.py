import requests

print(requests.patch("http://127.0.0.1:8080/api/me/profile", json={
    "isPublic": False
}, headers={
    "Authorization": "Bearer 15b4992546502fff1b392700b79aca9950a13145d56df34a15832ba1a041aec5"
}).json())