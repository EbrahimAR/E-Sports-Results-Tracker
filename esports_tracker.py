import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
import csv
import os

# --------------------------------------------------------
# E-Sports Results Tracker (GUI-based Application)
# --------------------------------------------------------
# Features:
# ✅ User Mode: View recent matches, team scores, and game-specific scores.
# ✅ Admin Mode: Manage teams, games, match records, and credentials.
# ✅ Stores all data in CSV files with proper headers.
# ✅ Provides a clean Tkinter interface for navigation and data display.
# --------------------------------------------------------

# -----------------------------
# Define file paths for storage
# -----------------------------
matches_file = 'matches.csv'
teams_file = 'teams.csv'
games_file = 'games.csv'
credentials_file = 'credentials.csv'

# ----------------------------------------------------
# Create and validate CSV files with specified headers
# ----------------------------------------------------
def create_file(file, header):
    """
    Create a CSV file with the given header if it doesn't exist or is empty.
    If the file exists but has a different header, overwrite it with the correct header.
    """
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        # Create new file with header
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    else:
        # Validate header and rewrite if incorrect
        with open(file, 'r') as f:
            existing_header = f.readline().strip().split(',')
        if existing_header != header:
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)

# ✅ Initialize the required files
create_file(matches_file, ['Date', 'Team A', 'Team B', 'Game Title', 'Winning Team'])
create_file(teams_file, ['Teams'])
create_file(games_file, ['Games'])
create_file(credentials_file, ['Username', 'Password'])

# ----------------------------
# Save data to CSV files
# ----------------------------
def save_csv(data, file):
    """
    Save a pandas DataFrame to a CSV file.
    """
    try:
        data.to_csv(file, index=False)
    except OSError as e:
        print(f"Error saving to file {file}: {e}")

# ----------------------------
# Load data from CSV files
# ----------------------------
def load_csv(file, required_columns=None):
    """
    Load data from a CSV file into a pandas DataFrame.
    If the file is empty or missing columns, return an empty DataFrame with required columns.
    """
    try:
        df = pd.read_csv(file)
        if required_columns:
            for col in required_columns:
                if col not in df.columns:
                    df[col] = []  # Add missing columns
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=required_columns if required_columns else [])

# --------------------------------------------------------
# Main Application Class for E-Sports Results Tracker
# --------------------------------------------------------
class EsportsApp(tk.Tk):
    def __init__(self):
        """
        Initialize the Tkinter window and display the main menu.
        """
        super().__init__()
        self.title("E-Sports Results Tracker")
        self.geometry("800x600")
        self.current_mode = None  # Track whether in user or admin mode
        self.main_menu()

    # ---------------------------------
    # Display the main menu
    # ---------------------------------
    def main_menu(self):
        """
        Show the main menu with options for User Mode and Admin Mode.
        """
        self.geometry("800x600")
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(self, text="E-Sports Results Tracker", font=("Century Gothic", 18, "bold")).pack(pady=20)
        ttk.Button(self, text="User Mode", command=self.user_menu).pack(pady=10)
        ttk.Button(self, text="Admin Mode", command=self.admin_login).pack(pady=10)

    # ---------------------------------
    # User Mode Menu
    # ---------------------------------
    def user_menu(self):
        """
        Display the user options menu.
        """
        self.geometry("800x600")
        self.current_mode = "user"
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(self, text="User Mode", font=("Century Gothic", 18, "bold")).pack(pady=20)
        ttk.Button(self, text="Back to Main Menu", command=self.main_menu).pack(pady=10)
        ttk.Button(self, text="View Recent Matches", command=self.show_recent_matches).pack(pady=10)
        ttk.Button(self, text="Overall Team Scores", command=self.show_team_scores).pack(pady=10)
        ttk.Button(self, text="Scores for Specific Game", command=self.show_game_scores).pack(pady=10)

    # ---------------------------------
    # Admin Authentication
    # ---------------------------------
    def admin_login(self):
        """
        Prompt for admin credentials and verify them.
        If invalid, allow registration as a new admin.
        """
        username = simpledialog.askstring("Admin Login", "Enter username:", parent=self)
        password = simpledialog.askstring("Admin Login", "Enter password:", show='*', parent=self)

        credentials = load_csv(credentials_file, required_columns=['Username', 'Password'])

        if not credentials.empty and ((credentials['Username'] == username) & (credentials['Password'] == password)).any():
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.admin_menu()
        else:
            choice = messagebox.askyesno("Invalid Credentials", "Invalid username or password. Would you like to register as a new admin?")
            if choice:
                self.register_admin()

    # ---------------------------------
    # Register a New Admin
    # ---------------------------------
    def register_admin(self):
        """
        Register a new admin using a security pin.
        """
        pin = simpledialog.askstring("Admin Registration", "Enter the admin pin:", show='*', parent=self)
        if pin == "230306":  # Hardcoded admin pin
            username = simpledialog.askstring("Admin Registration", "Enter a new username:", parent=self)
            password = simpledialog.askstring("Admin Registration", "Enter a new password:", show='*', parent=self)
            credentials = load_csv(credentials_file, required_columns=['Username', 'Password'])
            
            if username in credentials['Username'].values:
                messagebox.showinfo("Error", "Username already exists. Please choose a different one.")
            else:
                new_row = pd.DataFrame({'Username': [username], 'Password': [password]})
                credentials = pd.concat([credentials, new_row], ignore_index=True)
                save_csv(credentials, credentials_file)
                messagebox.showinfo("Success", "Admin registered successfully! You can now log in.")
        else:
            messagebox.showerror("Error", "Incorrect pin. Access denied.")

    # ---------------------------------
    # Admin Menu
    # ---------------------------------
    def admin_menu(self):
        """
        Display admin options such as team/game management and match recording.
        """
        self.geometry("800x600")
        self.current_mode = "admin"
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(self, text="Admin Mode", font=("Century Gothic", 18, "bold")).pack(pady=20)
        ttk.Button(self, text="Back to Main Menu", command=self.main_menu).pack(pady=10)
        ttk.Button(self, text="View All Teams", command=self.view_teams).pack(pady=10)
        ttk.Button(self, text="Add a New Team", command=lambda: self.modify_team('add')).pack(pady=10)
        ttk.Button(self, text="Remove a Team", command=lambda: self.modify_team('remove')).pack(pady=10)
        ttk.Button(self, text="View All Games", command=self.view_games).pack(pady=10)
        ttk.Button(self, text="Add a New Game", command=lambda: self.modify_game('add')).pack(pady=10)
        ttk.Button(self, text="Remove a Game", command=lambda: self.modify_game('remove')).pack(pady=10)
        ttk.Button(self, text="Record Match Outcome", command=self.record_match).pack(pady=10)
        ttk.Button(self, text="View All Matches", command=self.view_matches).pack(pady=10)

    # ---------------------------------
    # User Features
    # ---------------------------------
    def show_recent_matches(self):
        """
        Display the 5 most recent matches.
        """
        matches = load_csv(matches_file)
        self.display_table(matches.tail(5), title="Recent Matches")

    def show_team_scores(self):
        """
        Show overall team win counts.
        """
        matches = load_csv(matches_file)
        scores = matches['Winning Team'].value_counts().reset_index()
        scores.columns = ['Team', 'Wins']
        self.display_table(scores, title="Team Scores")

    def show_game_scores(self):
        """
        Show team scores for a specific game.
        """
        game = simpledialog.askstring("Input", "Enter game title:", parent=self)
        matches = load_csv(matches_file)
        game_scores = matches[matches['Game Title'] == game]['Winning Team'].value_counts().reset_index()
        game_scores.columns = ['Team', 'Wins']

        if game_scores.empty:
            messagebox.showinfo("Scores for Game", "No records found for the specified game.")
        else:
            self.display_table(game_scores, title=f"Scores for {game}")

    # ---------------------------------
    # Admin Team Management
    # ---------------------------------
    def view_teams(self):
        teams = load_csv(teams_file, required_columns=['Teams'])
        self.display_table(teams, title="Teams")

    def modify_team(self, action):
        """
        Add or remove a team.
        """
        team = simpledialog.askstring("Input", f"Enter team name to {action}:", parent=self)
        if team:
            teams = load_csv(teams_file, required_columns=['Teams'])
            if action == 'add':
                if team in teams['Teams'].values:
                    messagebox.showinfo("Info", "Team already exists.")
                else:
                    new_row = pd.DataFrame({'Teams': [team]})
                    teams = pd.concat([teams, new_row], ignore_index=True)
                    save_csv(teams, teams_file)
                    messagebox.showinfo("Info", "Team added successfully.")
            elif action == 'remove':
                if team not in teams['Teams'].values:
                    messagebox.showinfo("Info", "Team not found.")
                else:
                    teams = teams[teams['Teams'] != team]
                    save_csv(teams, teams_file)
                    messagebox.showinfo("Info", "Team removed successfully.")

    # ---------------------------------
    # Admin Game Management
    # ---------------------------------
    def view_games(self):
        games = load_csv(games_file, required_columns=['Games'])
        self.display_table(games, title="Games")

    def modify_game(self, action):
        """
        Add or remove a game.
        """
        game = simpledialog.askstring("Input", f"Enter game title to {action}:", parent=self)
        if game:
            games = load_csv(games_file, required_columns=['Games'])
            if action == 'add':
                if game in games['Games'].values:
                    messagebox.showinfo("Info", "Game already exists.")
                else:
                    new_row = pd.DataFrame({'Games': [game]})
                    games = pd.concat([games, new_row], ignore_index=True)
                    save_csv(games, games_file)
                    messagebox.showinfo("Info", "Game added successfully.")
            elif action == 'remove':
                if game not in games['Games'].values:
                    messagebox.showinfo("Info", "Game not found.")
                else:
                    games = games[games['Games'] != game]
                    save_csv(games, games_file)
                    messagebox.showinfo("Info", "Game removed successfully.")

    # ---------------------------------
    # Match Recording
    # ---------------------------------
    def record_match(self):
        """
        Record a new match result with date, teams, game title, and winner.
        """
        date = simpledialog.askstring("Input", "Enter the date (DD-MM-YYYY):", parent=self)
        teams = load_csv(teams_file, required_columns=['Teams'])
        games = load_csv(games_file, required_columns=['Games'])

        if teams.empty or games.empty:
            messagebox.showinfo("Error", "Please ensure teams and games are registered.")
            return

        team_a = simpledialog.askstring("Input", "Enter the first team:", parent=self)
        team_b = simpledialog.askstring("Input", "Enter the second team:", parent=self)
        game_title = simpledialog.askstring("Input", "Enter the game title:", parent=self)

        if team_a not in teams['Teams'].values or team_b not in teams['Teams'].values or game_title not in games['Games'].values:
            messagebox.showinfo("Error", "Please ensure teams and games are correctly registered.")
            return

        winning_team = simpledialog.askstring("Input", "Enter the winning team:", parent=self)

        if winning_team not in [team_a, team_b]:
            messagebox.showinfo("Error", "The winning team must be one of the competing teams.")
            return

        matches = load_csv(matches_file, required_columns=['Date', 'Team A', 'Team B', 'Game Title', 'Winning Team'])
        new_row = pd.DataFrame({'Date': [date], 'Team A': [team_a], 'Team B': [team_b], 'Game Title': [game_title], 'Winning Team': [winning_team]})
        matches = pd.concat([matches, new_row], ignore_index=True)
        save_csv(matches, matches_file)
        messagebox.showinfo("Success", "Match recorded successfully.")

    # ---------------------------------
    # View All Matches
    # ---------------------------------
    def view_matches(self):
        matches = load_csv(matches_file, required_columns=['Date', 'Team A', 'Team B', 'Game Title', 'Winning Team'])
        self.display_table(matches, title="All Matches")

    # ---------------------------------
    # Table Display Utility
    # ---------------------------------
    def display_table(self, data, title):
        """
        Display a pandas DataFrame in a Tkinter Treeview widget.
        """
        self.geometry("800x600")
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(self, text=title, font=("Century Gothic", 16, "bold")).pack(pady=10)
        frame = ttk.Frame(self, relief="solid", borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        columns = list(data.columns)
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)

        # Configure columns and alternating row colors
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)

        tree.tag_configure('oddrow', background='#f4f4f4')
        tree.tag_configure('evenrow', background='#e0e0e0')

        for index, row in data.iterrows():
            row_tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            tree.insert("", "end", values=row.tolist(), tags=(row_tag,))

        tree.pack(fill=tk.BOTH, expand=True)

        # Back button based on current mode
        if self.current_mode == "user":
            ttk.Button(self, text="Back", command=self.user_menu).pack(pady=10)
        elif self.current_mode == "admin":
            ttk.Button(self, text="Back", command=self.admin_menu).pack(pady=10)

# ✅ Entry point
if __name__ == "__main__":
    app = EsportsApp()
    app.mainloop()
