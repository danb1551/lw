import requests

SERVER = "http://localhost:8000"

print(f"[INFO] Spouštím tester na adrese {SERVER}")
if "hello from flask!" in requests.get(SERVER).content:
    print(f"[INFO] Test funkčnosti serveru prošel")
else:
    print(f"[INFO] Test funkčnosti serveru neprošel")
uuid: str
message = {"message": "nová zpráva"}
if requests.post(f"{SERVER}/messages", data=message).status_code == 201:
    print(f"[INFO] Test odeslání zprávy prošel")
    response = requests.get(f"{SERVER}/messages?data=true")
    data: dict[str: list[tuple]] = response.json()
    if response.status_code == 200 and data.get("message")[0][1] == message.get("message"):
        print(f"[INFO] Test získání zpráv prošlo")
        uuid = data.json()
    else:
        print(f"[INFO] Test získání zpráv neprošel")

else:
    print(f"[INFO] Test odeslání zprávy neprošel - přeskakuji získání zpráv")
