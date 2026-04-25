import scrape

scrape.get_file(filename = "presidential_results_2024.xlsx", url = "https://www.fec.gov/resources/cms-content/documents/2024presgeresults.xlsx", show_results = False)

senate_df = scrape.html_table_by_headers(url = "https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress", table_headers = ["Office"], index = 0, show_results = False)
house_df = scrape.html_table_by_headers(url = "https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress", table_headers = ["Office"], index = 1, show_results = False)

senate_df.fillna("N/A", inplace = True)
house_df.fillna("N/A", inplace = True)

senate_df.to_csv("senate_data_4-26.csv", index = False)
house_df.to_csv("house_data_4-26.csv", index = False)