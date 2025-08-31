import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
import csv
import os

# Define file paths for storing data
matches_file = 'matches.csv'
teams_file = 'teams.csv'
games_file = 'games.csv'
credentials_file = 'credentials.csv'

# Create and validate CSV files with specified headers
def create_file(file, header):
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        f = open(file, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()
    else:
        with open(file, 'r') as f:
            existing_header = f.readline().strip().split(',')
        if existing_header != header:
            f = open(file, 'w', newline='')
            writer = csv.writer(f)
            writer.writerow(header)
            f.close()

# Initialize the required files
create_file(matches_file, ['Date', 'Team A', 'Team B', 'Game Title', 'Winning Team'])
create_file(teams_file, ['Teams'])
create_file(games_file, ['Games'])
create_file(credentials_file, ['Username', 'Password'])

# Save data to CSV files
def save_csv(data, file):
    try:
        data.to_csv(file, index=False)
    except OSError as e:
        print(f"Error saving to file {file}: {e}")

# Load data from CSV files with optional column validation
def load_csv(file, required_columns=None):
    try:
        df = pd.read_csv(file)
        if required_columns:
            for col in required_columns:
                if col not in df.columns:
                    df[col] = []  # Add missing column
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=required_columns if required_columns else [])

# Define the main application class
class EsportsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("E-Sports Results Tracker")
        self.geometry("800x600")
        self.current_mode = None  # Track user/admin mode
        self.main_menu()

    # Display the main menu
    def main_menu(self):
        self.geometry("800x600")
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(self, text="E-Sports Results Tracker", font=("Century Gothic", 18, "bold")).pack(pady=20)
        ttk.Button(self, text="User Mode", command=self.user_menu).pack(pady=10)
        ttk.Button(self, text="Admin Mode", command=self.admin_login).pack(pady=10)

    # Display user-specific options
    def user_menu(self):
        self.geometry("800x600")
        self.current_mode = "user"
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(self, text="User Mode", font=("Century Gothic", 18, "bold")).pack(pady=20)
        ttk.Button(self, text="Back to Main Menu", command=self.main_menu).pack(pady=10)
        ttk.Button(self, text="View Recent Matches", command=self.show_recent_matches).pack(pady=10)
        ttk.Button(self, text="Overall Team Scores", command=self.show_team_scores).pack(pady=10)
        ttk.Button(self, text="Scores for Specific Game", command=self.show_game_scores).pack(pady=10)

    # Authenticate admin credentials
    def admin_login(self):
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

    # Register a new admin account
    def register_admin(self):
        pin = simpledialog.askstring("Admin Registration", "Enter the admin pin:", show='*', parent=self)
        if pin == "230306":
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

    # Display admin-specific options
    def admin_menu(self):
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

    # Display the most recent matches
    def show_recent_matches(self):
        matches = load_csv(matches_file)
        self.display_table(matches.tail(5), title="Recent Matches")

    # Calculate and display team scores
    def show_team_scores(self):
        matches = load_csv(matches_file)
        scores = matches['Winning Team'].value_counts().reset_index()
        scores.columns = ['Team', 'Wins']
        self.display_table(scores, title="Team Scores")

    # Display scores for a specific game
    def show_game_scores(self):
        game = simpledialog.askstring("Input", "Enter game title:", parent=self)
        matches = load_csv(matches_file)
        game_scores = matches[matches['Game Title'] == game]['Winning Team'].value_counts().reset_index()
        game_scores.columns = ['Team', 'Wins']

        if game_scores.empty:
            messagebox.showinfo("Scores for Game", "No records found for the specified game.")
        else:
            self.display_table(game_scores, title=f"Scores for {game}")

    # Display all registered teams
    def view_teams(self):
        teams = load_csv(teams_file, required_columns=['Teams'])
        self.display_table(teams, title="Teams")

    # Add or remove a team
    def modify_team(self, action):
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

    # Display all registered games
    def view_games(self):
        games = load_csv(games_file, required_columns=['Games'])
        self.display_table(games, title="Games")

    # Add or remove a game
    def modify_game(self, action):
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

    # Record match details
    def record_match(self):
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

    # Display all match records
    def view_matches(self):
        matches = load_csv(matches_file, required_columns=['Date', 'Team A', 'Team B', 'Game Title', 'Winning Team'])
        self.display_table(matches, title="All Matches")

    # Display a table in the GUI
    def display_table(self, data, title):
        self.geometry("800x600")
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(self, text=title, font=("Century Gothic", 16, "bold")).pack(pady=10)
        frame = ttk.Frame(self, relief="solid", borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        columns = list(data.columns)
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)

        tree.tag_configure('oddrow', background='#f4f4f4')
        tree.tag_configure('evenrow', background='#e0e0e0')

        for index, row in data.iterrows():
            row_tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            tree.insert("", "end", values=row.tolist(), tags=(row_tag,))

        tree.pack(fill=tk.BOTH, expand=True)

        if self.current_mode == "user":
            ttk.Button(self, text="Back", command=self.user_menu).pack(pady=10)
        elif self.current_mode == "admin":
            ttk.Button(self, text="Back", command=self.admin_menu).pack(pady=10)

if __name__ == "__main__":
    app = EsportsApp()
    app.mainloop()
