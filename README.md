# Evan and Emmy's Library Database - Library DB

This project was created for **CMPT 354 - Spring 2025** under the guidance of **Dr. Eugenia Ternovska**, Associate Professor at SFU.

## Table of Contents
- [Setup Instructions](#setup-instructions)
  - [Step 1: Set Up and Dependencies](#step-1-set-up-and-dependencies)
  - [Step 2: Backend Server](#step-2-backend-server)
  - [Step 3: Frontend Webpage](#step-3-frontend-webpage)
- [Feature Guide](#feature-guide)

---

## Setup Instructions

### Step 1: Set Up and Dependencies
1. Open a terminal.
2. Clone this repository:
   ```sh
   git clone https://github.com/EvanDongChen/CMPT354-LibraryDataBase.git
   ```

### Step 2: Backend Server
1. Navigate to the backend folder:
   ```sh
   cd CMPT354-LibraryDataBase/backend
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   ```
   **For Windows:**
   ```sh
   .\venv\Scripts\activate
   ```
   **For Mac/Linux:**
   ```sh
   source venv/bin/activate
   ```
3. If activation fails on Windows, try running:
   ```sh
   Set-ExecutionPolicy Unrestricted -Scope Process
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Populate the database:
   ```sh
   python library_populate.py
   ```
6. Start the backend server:
   ```sh
   python run.py
   ```

### Step 3: Frontend Webpage
1. Open a new terminal window and navigate to the frontend folder:
   ```sh
   cd CMPT354-LibraryDataBase/frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the frontend server:
   ```sh
   npm start
   ```
4. Open up the web app in the browser

---

## Feature Guide
1.📚 **Find an item** in the library
-Use the search bar on the top right and enter a desired search result; results will appear at the center of the webpage.
-By default all library items are displayed at the center of the page
<img width="406" alt="image" src="https://github.com/user-attachments/assets/f776a6e3-d059-4171-8208-2a9661cf49d4" />
<img width="1121" alt="image" src="https://github.com/user-attachments/assets/1c5ef332-ccc0-4773-833c-c01182669193" />


2.📖 **Borrow an item** from the library
-In the Library Items Catalog or Search Results, click the borrow button in each book box to borrow a book.
<img width="642" alt="image" src="https://github.com/user-attachments/assets/3a269f05-6530-488a-b295-eb88ea8ce3da" />

3.🔄 **Return a borrowed item**
-Click on the return tab in the nav-bar and click on the red return button to return a book.
-Books can also be returned using the Library Items Catalog
<img width="686" alt="image" src="https://github.com/user-attachments/assets/514d4a0c-946f-4481-b80b-05078d9f0a93" />

4.🎁 **Donate an item** to the library
-Click on the Donate tab in the nav-bar, fill in the form and submit a book. It will show up in the library items after refreshing the page.

5.📅 **Find an event** in the library
-Click on the Event tab in the nav-bar; all currently available events will be displayed.

6.📝 **Register for an event**
-Click on the Event tab in the nav-bar. Click on the register button to register for an event.
-Registration is based upon the currently logged-in users.
-If a user is not a member, they can also register for an event using the login page.
Image: Member Event Reg
<img width="647" alt="image" src="https://github.com/user-attachments/assets/635d3db1-98d1-4d8f-9537-40a64c2dc167" />
Image: Non-Member Event Reg
![image](https://github.com/user-attachments/assets/7a6e9584-079a-4f8d-81f7-31bfc925f474)

7.🤝 **Volunteer** for the library
-Click on the Volunteer tab in the nav-bar. Select a desired role and click "register as a volunteer"
-Volunteer registration is based on the user currently logged in.
![image](https://github.com/user-attachments/assets/94d4ef0d-8596-4ddb-b311-c5d91ea74a39)

8.❓ **Ask for help** from a librarian
-Click on the Contact tab in the nav-bar. Fill in a the form to submit a question, all past asked questions are displayed below the form.
![image](https://github.com/user-attachments/assets/0fd365f4-4428-4688-b2cf-34faf36fbc7b)
![image](https://github.com/user-attachments/assets/1d149f59-672a-43e3-9ca8-d2c368c82a97)


---

Thank you for checking out our library database web app!
If you are having trouble running the web app, please contact us at eca165@sfu.ca !

