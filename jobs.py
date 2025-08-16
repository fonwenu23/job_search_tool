import requests
import pandas as pd

def auth():
    """Retrieve API token from environment."""
    token = ""
    return token

def fetch_jobs():
    """Fetch job listings from TheirStack API."""
    token = auth()   
    if not token:
        raise ValueError("No API token found")
    else:
        headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {token}"
                  }
        url = "https://api.theirstack.com/v1/jobs/search"
        payload = {
                    "page": 0,
                    "limit": 5,
                    "job_country_code_or": [
                      "US"
                    ],
                    "job_title_or": [
                    "assistant",
                    "data entry"
                      ],
                    'company_location_pattern_or': [
                        "wyandotte",
                        "brownstown",
                        "flat rock",
                        "woodhaven" 
                        ],
                    "posted_at_max_age_days": 3
                    }
        r = requests.post(url, json=payload, headers=headers)
        if r.status_code not in [200, 201]:
            print("Error:", r.status_code, r.text)
            return None
        else:
            print("Success:", r.status_code)
            data = r.json()
            return data

def parse_jobs(data):
    """Extract relevant job fields into a list of dictionaries."""
    jobs = []
    for job in data['data']:
        jobs.append({
            'id' : job.get('id', []),
            'job_title' :job.get('job_title', []),
            'url' : job.get('url', []),
            'date_posted' : job.get('date_posted', []),
            'company' : job.get('company', []),
            'location' : job.get('location', []),
            'remote' : job.get('remote', []),
            'hybrid' : job.get('hybrid', []),
            'salary' : job.get('salary_string', []),
            'employment_status' : job.get('employment_status', [])
        })
    return jobs
        
if __name__ == "__main__":       
    data = fetch_jobs()
    if data is None:
        print("No data retrieved.")
    else:
        jobs = parse_jobs(data)
        if jobs:
            df = pd.DataFrame(jobs)
            print(f"Filtered Jobs ({len(jobs)} results):")
            print(df.head(10))
            df.to_csv('jobs.csv', sep='|', index=False)








