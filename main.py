from app.file_reader import read_text_file
from app.csv_loader import load_csv

def main():

    print("AI Document Assistant")

    text = read_text_file("data/sample.txt")
    print(text)

    df = load_csv("data/sample.csv")
    print(df)

if __name__ == "__main__":
    main()