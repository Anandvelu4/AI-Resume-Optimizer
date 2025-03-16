import requests
#API endpoints
url= "https://ai-resume-optimizer-t0mo.onrender.com/upload"
# Open a sample resume file(Make sure "Sample_resume.pdf" is in the same directory as this file)")
files = {'file': open('sample_resume.pdf', 'rb')}
# Send a POST request to the API endpoint with the resume file as a multipart form data
response = requests.post(url, files=files)
# Print the response status code and text
print(response.json)