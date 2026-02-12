import pandas as pd
from datetime import datetime
import random
import time
import os

CSV_FILE = "compteurs.csv"
COMMIT_MSG = "Mise à jour automatique du CSV"

while True:
    # Ajouter une nouvelle ligne
    new_row = {
        "timestamp": datetime.now(),
        "humains": random.randint(0, 100),
        "velos": random.randint(0, 50)
    }

    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "humains", "velos"])

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    # Git add / commit / push
    os.system("git add compteurs.csv")
    os.system(f"git commit -m '{COMMIT_MSG}'")
    os.system("git push")

    print(f"{datetime.now()}: ligne ajoutée et push effectué")

    time.sleep(60)  # attente 60 secondes avant le prochain push