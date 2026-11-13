import sys
import duckdb
import pyarrow.ipc as ipc
from pathlib import Path

DATA_DIR = Path(__file__).parent / "perspective-app" / "data"

def get_connection():
    conn = duckdb.connect()
    # Register parquet files first (fastest)
    parquet_files = list(DATA_DIR.glob("*.parquet"))
    registered = set()
    for pf in parquet_files:
        name = pf.stem.replace(".lz4", "").replace("-", "_")
        try:
            conn.execute(f"CREATE TABLE \"{name}\" AS SELECT * FROM '{pf}'")
            registered.add(name)
        except Exception:
            pass

    # Register arrow files for anything not covered
    for f in DATA_DIR.glob("*.arrow"):
        name = f.stem.replace(".lz4", "").replace("-", "_")
        if name in registered:
            continue
        try:
            tbl = ipc.open_stream(str(f)).read_all()
            conn.register(name, tbl)
            registered.add(name)
        except Exception:
            pass

    # Aliases
    if "nypdccrb" in registered and "nypd" not in registered:
        conn.execute("CREATE VIEW nypd AS SELECT * FROM nypdccrb")

    # Register Iris dataset
    iris_path = DATA_DIR / "iris.parquet"
    if not iris_path.exists():
        iris_path = Path(__file__).parent / "datasets" / "iris.csv"
    if iris_path.exists() and "iris" not in registered:
        try:
            if str(iris_path).endswith(".parquet"):
                conn.execute(f"CREATE TABLE iris AS SELECT * FROM '{iris_path}'")
            else:
                conn.execute(f"CREATE TABLE iris AS SELECT * FROM read_csv_auto('{iris_path}')")
        except Exception:
            pass

    return conn

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "SHOW TABLES;"
    conn = get_connection()
    try:
        df = conn.execute(query).df()
        print(df.to_string(index=False))
    except Exception as e:
        print(f"SQL Error: {e}")
