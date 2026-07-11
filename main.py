from app.document_service import summarize_document,explain_document

def main():

    summary = summarize_document(
        #"data/company_policy.txt"
        "data/it_policy.txt"
    )
    print(summary)
'''
    explain = explain_document(
        "data/it_policy.txt"
    )
    print(explain)
'''
if __name__ == "__main__":
    main()