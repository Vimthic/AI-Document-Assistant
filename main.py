from app.pipeline import process_text_document

def main():

    text = process_text_document(
       # "data/company_policy.txt" 
        "data/hr_policy.txt" 
    )

    print(text)

if __name__ == "__main__":
    main()