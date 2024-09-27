from functions import fetch_google_results,fetch_and_combine_contents


google_results = fetch_google_results("top crime news detaisl kerala")
print(google_results)
results = fetch_and_combine_contents(google_results)
print(results)


