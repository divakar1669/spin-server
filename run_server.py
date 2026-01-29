import sys

def main():
    try:
        import uvicorn
    except Exception:
        print("uvicorn is not installed. Install dependencies with 'python3 -m pip install -r requirements.txt'", file=sys.stderr)
        sys.exit(1)
    uvicorn.run("rules_app.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
