# 🎮 E-Sports Results Tracker

A **Python desktop application** to manage and track E-Sports match results with a **user-friendly GUI** built using **Tkinter**.  
This app supports **Admin & User roles**, team/game management, and match result recording.

---

## ✅ Features
- **User Mode**
  - View recent matches
  - View overall team scores
  - View scores for a specific game

- **Admin Mode**
  - Secure login & registration
  - Add / Remove Teams
  - Add / Remove Games
  - Record match outcomes
  - View all matches

---

## 🛠 Tech Stack
- **Python 3**
- **Tkinter** (GUI)
- **Pandas** (Data handling)
- **CSV files** for persistence

---

## 📂 Project Structure
    E-Sports Result Tracker/
    │── credentials.csv # Admin login credentials
    │── games.csv # List of games
    │── matches.csv # Match history
    │── teams.csv # List of teams
    │── esports_tracker.py # Main application

---

## 🚀 How to Run
### 1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/esports-results-tracker.git
   cd esports-results-tracker
   ```

### 2. **Install dependencies**
    pip install pandas

### 3. **Run the app**
    python esports_tracker.py

---

## ▶ Usage
### **Launching the App**

  - Run the script:
    ```bash
    python esports_tracker.py
    ```
User Mode

Choose User Mode from the main menu.

View:

Recent Matches (last 5 recorded)

Overall Team Scores

Scores for a Specific Game

Admin Mode

Choose Admin Mode from the main menu.

Log in with existing credentials or register as a new admin (requires an admin PIN).

Perform actions:

View/Add/Remove Teams

View/Add/Remove Games

Record Match Outcomes

View All Matches

Admin PIN for Registration

Default PIN: 230306 (You can modify it in the code).

## 🔮 Future Improvements
- AI-based match outcome prediction

- Natural language queries (NLP)

- Voice commands for user interaction

- AI-generated performance insights

---

## 👨‍💻 Author
Ebrahim Abdul Raoof

[LinkedIn](https://www.linkedin.com/in/ebrahim-ar/)

[GitHub](https://github.com/EbrahimAR)

---

## 📜 License
This project is licensed under the MIT License. See [LICENSE](https://github.com/EbrahimAR/E-Sports-Results-Tracker/blob/main/LICENSE) for details.
