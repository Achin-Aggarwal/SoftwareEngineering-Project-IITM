Recommended IDE Setup
VSCode + Volar (and disable Vetur).

Customize configuration
See Vite Configuration Reference.

Project Setup
To run our application on your local device, you will need to have the following installed:

Python 3.10

Pip

Node.js

A. Creation of Virtual Environment
Navigate to the project folder:

bash
Copy
cd /mnt/c/Users/...........(path to our project folder)
cd soft-engg-project-jan-2025-se-Jan-16/
cd Backend/
Create the virtual environment:

bash
Copy
python3 -m venv venv
B. Start the Virtual Environment
Activate the virtual environment:

On Windows:

bash
Copy
.\venv\Scripts\activate
On Mac/Linux:

bash
Copy
source venv/bin/activate
C. Package Installation
Install the required Python packages:

bash
Copy
pip install -r requirements.txt
D. Install Node Modules
Navigate to the frontend folder:

bash
Copy
cd /mnt/c/Users/...........(path to our frontend folder)
cd soft-engg-project-jan-2025-se-Jan-16/
cd Frontend/
Install Node.js dependencies:

bash
Copy
npm install
E. Start the Frontend
Run the frontend application:

bash
Copy
npm run dev
F. Start the Backend
Navigate to the backend folder:

bash
Copy
cd /mnt/c/Users/...........(path to our backend folder)
cd soft-engg-project-jan-2025-se-Jan-16/
cd Backend/
Start the backend:

On Windows:

bash
Copy
python3 main.py
On Mac:

bash
Copy
python3 main.py
Open the App
Open the app in your browser by navigating to:
http://localhost:5173/

