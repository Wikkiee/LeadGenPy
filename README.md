<div align="center">
  <p>
      <img width="30%" src="https://i.imgur.com/vOWLuzY.png">
  </p>

  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/selenium)
  ![License](https://img.shields.io/badge/License-MIT-blue.svg)

</div>
LeadGenPy transforms lead generation by extracting Google Maps business details with Selenium, processing data, and dynamically generating personalized messages using the Chat GPT API. Seamlessly integrate with Google Sheets API for an efficient and impactful strategy.

## Overview

The Python script, `main.py`, controls the entire operation of LeadGenPy. It utilizes Selenium with a web driver to enter [Google Maps](https://maps.google.com), search for specific business types, and extract relevant information.

LeadGenPy performs the following tasks:

1. **Data Extraction:**
    - Searches for a specific business type and location.
    - Loops through search results, extracts business details, and stores data in CSV (`data.csv`) and JSON (`data.json`) files simultaneously.
    - Data extracted includes:
        ```json
              {
                  "BusinessName": "Sample Business",
                  "Address": "123 Main Street, Cityville, State 12345",
                  "PhoneNumber": "123-456-7890",
                  "Website": "samplebusiness.com",
                  "Category": "General Business",
                  "Rating": "4.2",
                  "ReviewCount": "10",
                  "google_map_link": "https://www.google.com/maps/place/Sample+Business/data=...",
                  "email": "info@samplebusiness.com",
                  "status": "success"
              }

        ```
2. **User Interaction:**
    - Offers options to the user:
        - Terminate (`mode == 0`).
        - Start extraction (`mode == 1`).
        - View extracted dataset (`mode == 2`).
        - Transfer data to Google Sheets (`mode == 3`).
        - Generate personalized emails using Chat GPT (`mode == 4`).
        - Production mode (combining extraction, data transfer, and email sending) (`mode == 5`).
        - Development mode for sheet cleanup (`else`).

3. **Authentication:**
    - Prompts for Google sign-in if not authenticated (used for storing data in Google Sheets).





## Getting Started

Follow these steps to set up and run LeadGenPy locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/LeadGenPy.git
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   **Dependencies:**
    - `selenium==4.5.0`
    - `python-dotenv==0.21.0`
    - `beautifulsoup4==4.12.2`
    - `requests==2.28.1`
    - `google-auth-oauthlib==1.1.0`
    - `google-auth-httplib2==0.1.0`
    - `google-auth==2.15.0`
    - `google-api-python-client==2.70.0`
    - `google-api-core==2.11.0`
    - `googleapis-common-protos==1.57.0`
    - `openai==0.28.0`
    - `lxml`

3. **Environment Variables:**
    - Create a `.env` file with the following content:
        ```
        OPENAI_API_KEY="Your-OpenAI-API-KEY"
        SPREADSHEET_ID="Your-Google-sheet-ID"
        EMAIL_ADDRESS="Your-Email-Address"
        ```
    - Sample 
4. **Download ChromeDriver:**
    - Download the appropriate version of [ChromeDriver](https://chromedriver.chromium.org/downloads) based on your Chrome browser version to avoid compatibility errors.
    - Copy the Chromedriver.exe to the `assets\chromedriver.exe` folder
    - To check your browser version, Open Chrome and enter this URL ``chrome://version``
      
5. **Run the Script:**
   ```bash
   cd src && python main.py
   ```
6. **Authenticate with Google (if prompted):**
    - This is necessary for storing data in Google Sheets.
7. **Select the desired mode:**
    - Choose the option that corresponds to your workflow.
### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contributing
Feel free to contribute! Check out the [Contributing Guidelines](CONTRIBUTING.md) for more information.

### Contact
- Discord: #wikkie
- LinkedIn: [Vignesh Mayilsamy](https://www.linkedin.com/in/vignesh-mayilsamy/)
- Email: wikkiedev@gmail.com
