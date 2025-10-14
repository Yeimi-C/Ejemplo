from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def test():
    return {"status": "Activo"}

# Si hay tiempo y por un chocolate

"""

"""