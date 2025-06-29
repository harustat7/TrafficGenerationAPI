from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.post("/generate-pcap")
def generate_pcap():
    try:
        # Run the script (make sure it doesn't auto-run when imported)
        subprocess.run(["python", "attackgeneraterfinal.py"], check=True)
        return {"status": "success", "message": "PCAP generated successfully."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
