from src.extract import extract_data
from src.transform import clean
from src.load import load

in_path = "data/raw/tunisianet_smartphones.csv"
out_path = "data/processed/tunisianet_smartphones_.csv"
db_path = "database.db"

def main():
    extract_data()
    clean(in_path, out_path)
    load(out_path, db_path)

if __name__ == "__main__":
    main()

