from app.document_service import summarize_document

def main():

    summary = summarize_document(
        "data/company_policy.txt"
    )

    print(summary)

if __name__ == "__main__":
    main()