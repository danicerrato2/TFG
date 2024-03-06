import requests

TFG_API_KEY = "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"
API_URL = "https://api.openai.com/v1/chat/completions"

text = "Create a small dataset about total sales over the last year. The format of the dataset should be a data frame with 12 rows and 2 columns. The columns should be called 'month' and 'total_sales_usd'. The 'month' column should contain the shortened forms of month names from 'Jan' to 'Dec'. The 'total_sales_usd' column should contain random numeric values taken from a normal distribution with mean 100000 and standard deviation 5000. Provide Python code to generate the dataset, then provide the output in the format of a markdown table."

response = requests.post(
	url=API_URL,
	headers={
		"Authorization": "Bearer " + TFG_API_KEY
	},
	data={
		"model": "gpt-3.5-turbo",
		"messages": [{
			"role": "system",
			"content": "You're a rewriter"
		},
		{
			"role": "user",
			"content": "Rewrite just one sentence of your choice of the next text:\n" + text
		}]
	}
)

print(response.text)