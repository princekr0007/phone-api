from fastapi import FastAPI, HTTPException
import duckdb

app = FastAPI(title="Phone API")

# princekr8800/My-database ke saare 7 phone files
PARQUET_FILES = [
    "https://huggingface.co/datasets/princekr8800/My-database/resolve/main/idx_phone.0.parquet",
    "https://huggingface.co/datasets/princekr8800/My-database/resolve/main/idx_phone.1.parquet",
    "https://huggingface.co/datasets/princekr8800/My-database/resolve/main/idx_phone.2.parquet",
    "https://huggingface.co/datasets/princekr8800/My-database/resolve/main/idx_phone.3.parquet",
    "https://huggingface.co/datasets/princekr8800/My-database/resolve/main/idx_phone.4.parquet",
    "https://huggingface.co/datasets/princekr8800/My-database/resolve/main/idx_phone.5.parquet",
    "https://huggingface.co/datasets/princekr8800/My-database/resolve/main/idx_phone.6.parquet",
]

con = duckdb.connect(database=":memory:")
con.execute("INSTALL httpfs; LOAD httpfs;")

files_str = "[" + ", ".join([f"'{f}'" for f in PARQUET_FILES]) + "]"

@app.get("/search")
def search(q: str):
    if not q.isdigit() or len(q) != 10:
        raise HTTPException(status_code=400, detail="Invalid 10-digit number")

    try:
        query = f"""
            SELECT *
            FROM read_parquet({files_str})
            WHERE CAST(phoneNumber AS VARCHAR) = '{q}' 
               OR CAST(otherNumber AS VARCHAR) = '{q}'
            LIMIT 1
        """
        result = con.execute(query).fetchdf()

        if result.empty:
            raise HTTPException(status_code=404, detail="Data not found")

        return {
            "status": "success",
            "data": result.to_dict(orient="records")[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
