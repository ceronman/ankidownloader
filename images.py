from serpwow.google_search_results import GoogleSearchResults
import json

# create the serpwow object, passing in our API key
serpwow = GoogleSearchResults("900563DFC40148A89917EDB74CE871AE")

# set up a dict for the search parameters
params = {
  "q" : "pen",
  "search_type" : "images",
  "images_size" : "medium",
  "images_type" : "clipart"
}

# retrieve the search results as JSON
result = serpwow.get_json(params)

# pretty-print the result
print(json.dumps(result, indent=2, sort_keys=True))