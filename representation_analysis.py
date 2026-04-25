import scrape

scrape.get_file(filename = "presidential_results_2024.xlsx", url = "https://www.fec.gov/resources/cms-content/documents/2024presgeresults.xlsx", show_results = False)

senate_df = scrape.html_table_by_headers(table_headers = ["Office"], url = "https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress", index = 0, show_results = False)
house_df = scrape.html_table_by_headers(table_headers = ["Office"], url = "https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress", index = 1, show_results = False)
redistricting_df = scrape.html_table_by_headers(table_headers = ["Potential result of new maps"], url = "https://ballotpedia.org/Redistricting_in_California_ahead_of_the_2026_elections", show_results = False)

senate_df.fillna("N/A", inplace = True)
house_df.fillna("N/A", inplace = True)
redistricting_df.fillna("N/A", inplace = True)
redistricting_df = redistricting_df[~redistricting_df["State"].str.contains("New map")]
useless_index = redistricting_df.index[redistricting_df["State"] == "Net"][0]
redistricting_df = redistricting_df.loc[:useless_index]

senate_df.to_csv("senate_members.csv", index = False)
house_df.to_csv("house_members.csv", index = False)
redistricting_df.to_csv("redistricting_results.csv", index = False)