import json
import os
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Label, Input
from textual.containers import Container, Horizontal, Vertical, Center
# Import fungsi sistem dari utils
from utils import get_system_info, get_user_prompt, open_file_manager, open_gemini_chat

# Lokasi file konfigurasi
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "user_config.json")

# --- SIGN UP SCREEN ---
class SignUpScreen(Screen):
    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="login-box"):
                yield Label("󰣇", id="login-icon")
                yield Label("INITIAL SETUP: CREATE ACCOUNT", id="login-title")
                yield Input(placeholder="Create New Username", id="new-user")
                yield Input(placeholder="Create New Password", password=True, id="new-pass")
                yield Button("CREATE ACCOUNT", variant="success", id="setup-btn")
                yield Label("Welcome! Please set your credentials.", id="status-msg")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "setup-btn":
            username = self.query_one("#new-user").value
            password = self.query_one("#new-pass").value
            
            if username and password:
                data = {"username": username, "password": password}
                with open(CONFIG_PATH, "w") as f:
                    json.dump(data, f, indent=4)
                
                self.app.notify("Account created! Please login.", title="INDOS")
                self.app.push_screen(LoginScreen())
            else:
                self.query_one("#status-msg").update("[red]Fields cannot be empty![/red]")

# --- LOGIN SCREEN ---
class LoginScreen(Screen):
    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="login-box"):
                yield Label("󰣇", id="login-icon")
                yield Label("INDOS SECURE LOGIN", id="login-title")
                yield Input(placeholder="Username", id="user-input")
                yield Input(placeholder="Password", password=True, id="pass-input")
                yield Button("LOGIN", variant="primary", id="login-btn")
                yield Label("", id="status-msg")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login-btn":
            self.check_login()

    def check_login(self) -> None:
        try:
            if not os.path.exists(CONFIG_PATH):
                self.app.push_screen(SignUpScreen())
                return

            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            
            user_input = self.query_one("#user-input").value
            pass_input = self.query_one("#pass-input").value

            if user_input == data["username"] and pass_input == data["password"]:
                self.app.push_screen(MainWorkspace())
            else:
                self.query_one("#status-msg").update("[red]󰚌 Access Denied![/red]")
        except Exception as e:
            self.query_one("#status-msg").update(f"[red]Error: {str(e)}[/red]")

# --- MAIN WORKSPACE ---
class MainWorkspace(Screen):
    def compose(self) -> ComposeResult:
        # Waybar dengan tombol tambahan untuk Yazi dan AI
        yield Horizontal(
            Static(" 󰣇  INDOS ", id="os-logo"),
            Button("  SESSION", id="add_btn", classes="btn-action"),
            Button("󰝰  FILES", id="yazi_btn", classes="btn-action"),
            Button("󰧑  AI", id="ai_btn", classes="btn-action"),
            Static(get_system_info(), id="info-bar"),
            id="waybar"
        )
        yield Container(
            Vertical(Label(get_user_prompt()), classes="panel"),
            id="workspace"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_btn":
            new_panel = Vertical(Label(get_user_prompt()), classes="panel")
            self.query_one("#workspace").mount(new_panel)
        
        elif event.button.id == "yazi_btn":
            # Suspend TUI untuk membuka Yazi di terminal
            with self.app.suspend():
                open_file_manager()
        
        elif event.button.id == "ai_btn":
            # Suspend TUI untuk membuka Gemini CLI chat
            with self.app.suspend():
                open_gemini_chat()

class INDOS(App):
    CSS_PATH = "styles.css"
    BINDINGS = [("q", "quit", "Quit INDOS")]

    def on_mount(self) -> None:
        if os.path.exists(CONFIG_PATH):
            self.push_screen(LoginScreen())
        else:
            self.push_screen(SignUpScreen())

if __name__ == "__main__":
    app = INDOS()
    app.run()
