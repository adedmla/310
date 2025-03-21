from dotenv import load_dotenv
import requests 
import json 
import os 
import webbrowser


load_dotenv(dotenv_path=".env")

API_URL = os.getenv("API_URL")

def list_podcasts(): 
    """List all podcast jobs:
        a) Build the URL 
        b) loop through the return JSON 
        c) List out the diff parameters
        
        params: None """

    try: 
        response = requests.get(f"{API_URL}/list")
        data = response.json()
        if 'jobs' in data and data['jobs']: 
            print("---Podcast Jobs---")

            for job in data['jobs']: 
                print(f"Job ID: {job.get('jobid')}")
                print(f"Status: {job.get('status')}")
                print(f"Filename: {job.get('original_filename')}")
                print("-" * 30)
            print(f"Total jobs: {data['pagination']['total']}")
        else:
            print("No jobs found.")

    except Exception as e: 
        print(f"Error listing podcasts: {e}")


def get_status():
    """Check the status of a podcast transcription job
        a) Build URL with the passed in jobID
        b) From the JSON extract the ID, status, and Original filename 
        c) If possible extract the different keys 
        
        params: jobID 
        """
    job_id = input("Enter the job ID: ")
    
    if not job_id:
        print("Error: Job ID is required")
        return
    
    try:
        print(f"Checking status for job: {job_id}...")
        params = {
            'jobid': job_id
        }
        response = requests.get(f"{API_URL}/status", params=params)
        

        try:
            data = response.json()
            if response.status_code == 200:
                print("\n=== Job Status ===")
                print(f"Job ID: {data.get('jobid', 'N/A')}")
                print(f"Status: {data.get('status', 'N/A')}")
                print(f"Original Filename: {data.get('original_filename', 'N/A')}")
                
                if data.get('audio_filekey'):
                    print(f"Audio File: {data['audio_filekey']}")
                if data.get('transcript_filekey'):
                    print(f"Transcript File: {data['transcript_filekey']}")
                if data.get('analysis_filekey'):
                    print(f"Analysis File: {data['analysis_filekey']}")
            elif response.status_code == 404:
                print(f"Job not found: {job_id}")
            else:
                print(f"Error checking job status: {data.get('error', 'Unknown error')}")
        except json.JSONDecodeError:
            print("Failed to parse response: Invalid JSON")
            print(f"Response text: {response.text}")
    
    except Exception as e:
        print(f"Error checking job status: {e}")


def upload_file():
    """Upload an audio file to the podcast service
        a) """
    filename = input("Enter filename (e.g., audio.mp3): ")
    
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found in current directory")
        return
    
    try:
        with open(filename, "rb") as file:
            url = f"{API_URL}/upload?filename={os.path.basename(filename)}"
            print(f"Uploading to: {url}")
            
            files = {'file': (os.path.basename(filename), file, f'audio/{os.path.splitext(filename)[1][1:]}' )}
            
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            print(f"File size: {file_size} bytes")
            
            response = requests.post(url, files=files)
            
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response body: {response.text}")
            
            try:
                data = response.json()
                if response.status_code == 200:
                    print("\n=== Upload Successful ===")
                    print(f"Message: {data.get('message', 'N/A')}")
                    print(f"Job ID: {data.get('job_id', 'N/A')}")
                else:
                    print(f"Upload failed with status code: {response.status_code}")
                    print(f"Error message: {data.get('error', data)}")
            except json.JSONDecodeError:
                print("Upload failed: Invalid JSON response")
                print(f"Response text: {response.text}")
    
    except Exception as e:
        print(f"Error uploading file: {e}")


def download_results():
    """Download transcription or analysis results"""
    job_id = input("Enter the job ID: ")
    
    if not job_id:
        print("Error: Job ID is required")
        return
    
    file_type = input("Enter file type (transcript/analysis) [default: transcript]: ").lower()
    if not file_type:
        file_type = "transcript"
    
    if file_type not in ["transcript", "analysis"]:
        print("Invalid file type. Please use 'transcript' or 'analysis'")
        return
    
    if file_type == "transcript":
        format_choice = input("Choose output format (json/text/html) [default: text]: ").lower()
        if not format_choice:
            format_choice = "text"
        
        if format_choice not in ["json", "text", "html"]:
            print("Invalid format. Using default (text)")
            format_choice = "text"
    else:
        format_choice = "json" 
    
    try:
        print(f"Downloading {file_type} for job ID: {job_id}...")
        
        if format_choice in ["text", "html"]:
            params = {
                'jobid': job_id,
                'type': file_type,
                'format': format_choice
            }
            
            print(f"Fetching formatted {format_choice.upper()} content...")
            
            response = requests.get(f"{API_URL}/download", params=params)
            
            if response.status_code == 200:
                extension = ".txt" if format_choice == "text" else ".html"
                default_filename = f"{job_id}_transcript{extension}"
                save_filename = input(f"Enter filename [default: {default_filename}]: ")
                if not save_filename:
                    save_filename = default_filename
                
                with open(save_filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"File saved as: {save_filename}")
                
                if format_choice == "html":
                    open_browser = input("Open in browser? (y/n) [default: y]: ").lower()
                    if open_browser != 'n':
                        print(f"Opening {save_filename} in default browser...")
                        webbrowser.open(f"file://{os.path.abspath(save_filename)}")
            else:
                print(f"Error downloading file. Status code: {response.status_code}")
                try:
                    data = response.json()
                    print(f"Error message: {data.get('error', 'Unknown error')}")
                except:
                    print(f"Response text: {response.text}")
        else:
            params = {
                'jobid': job_id,
                'type': file_type,
                'url_only': 'true'
            }
            
            response = requests.get(f"{API_URL}/download", params=params)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    download_url = data.get('download_url')
                    
                    if download_url:
                        print(f"\nDownload URL generated (valid for {data.get('expires_in', '1 hour')}):")
                        print(download_url)
                        
                        open_browser = input("\nOpen in browser? (y/n) [default: y]: ").lower()
                        if open_browser != 'n':
                            print("Opening URL in default browser...")
                            webbrowser.open(download_url)
                        
                        save_file = input("\nSave to local file? (y/n) [default: y]: ").lower()
                        if save_file != 'n':
                            file_response = requests.get(download_url)
                            
                            default_filename = os.path.basename(data.get('file_key', f"{job_id}_{file_type}.json"))
                            save_filename = input(f"Enter filename [default: {default_filename}]: ")
                            if not save_filename:
                                save_filename = default_filename
                            
                            try:
                                json_content = file_response.json()
                                with open(save_filename, 'w', encoding='utf-8') as f:
                                    json.dump(json_content, f, indent=2)
                                print(f"File saved as: {save_filename} (with pretty formatting)")
                            except:
                                with open(save_filename, 'wb') as f:
                                    f.write(file_response.content)
                                print(f"File saved as: {save_filename}")
                    else:
                        print("Error: No download URL provided in the response")
                except json.JSONDecodeError:
                    print("Failed to parse response: Invalid JSON")
                    print(f"Response text: {response.text}")
            elif response.status_code == 404:
                print(f"Error: {file_type.capitalize()} file not found for job {job_id}")
            else:
                print(f"Error downloading file. Status code: {response.status_code}")
                try:
                    data = response.json()
                    print(f"Error message: {data.get('error', 'Unknown error')}")
                except:
                    print(f"Response text: {response.text}")
    
    except Exception as e:
        print(f"Error downloading results: {e}")


def reset_table():
    """Reset the jobs table (remove all jobs)"""
    
    print("\n!!! WARNING !!!")
    print("This will delete ALL jobs from the database.")
    confirmation = input("Type 'CONFIRM' to proceed: ")
    
    if confirmation != "CONFIRM":
        print("Operation cancelled.")
        return
    
    try:
        params = {
            'confirm': 'true'
        }
        
        response = requests.get(f"{API_URL}/reset", params=params)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("\n=== Table Reset ===")
                print(f"Message: {data.get('message', 'Reset successful')}")
            except json.JSONDecodeError:
                print("Failed to parse response: Invalid JSON")
                print(f"Response text: {response.text}")
        else:
            print(f"Error resetting table. Status code: {response.status_code}")
            try:
                data = response.json()
                print(f"Error message: {data.get('error', 'Unknown error')}")
            except:
                print(f"Response text: {response.text}")
    
    except Exception as e:
        print(f"Error resetting table: {e}")


def main_menu(): 
    """Main menu for user input"""

    while True:
        print("\n--- Podcast Transcription Client ---")
        print("1. List all podcast jobs")
        print("2. Check job status")
        print("3. Upload new audio file")
        print("4. Download results")
        print("5. Reset jobs table")
        print("0. Exit")

        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '0': 
            print("Goodbye!")
            break 
        elif choice == '1':
            list_podcasts()
        elif choice == '2':
            get_status()
        elif choice == '3':
            upload_file()
        elif choice == '4':
            download_results()
        elif choice == '5':
            reset_table()
        else:
            print("Invalid choice. Please try again.")

    print("---Program Terminated---")

if __name__ == '__main__':
    print("Welcome to the Podcast Transcription Client")
    main_menu()