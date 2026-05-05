from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Label
from textual.containers import Container, Horizontal, Vertical
from utils import get_system_info, get_user_prompt

class INDOS(App):
    TITLE = "INDOS - TUI Workspace"
    CSS_PATH = "styles.css"

    def compose(self) -> ComposeResult:
        # Waybar dengan ikon NerdFont
        yield Horizontal(
            Static(" 󰣇  INDOS ", id="os-logo"),
            Button("  ADD SESSION", id="add_btn", classes="btn-action"),
            Static(get_system_info(), id="info-bar"),
            id="waybar"
        )
        # Workspace Area
        yield Container(
            Vertical(
                Label(get_user_prompt()),
                classes="panel"
            ),
            id="workspace"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_btn":
            new_panel = Vertical(
                Label(get_user_prompt()),
                classes="panel"
            )
            self.query_one("#workspace").mount(new_panel)
            self.notify("New workspace session initialized.", title="INDOS")

if __name__ == "__main__":
    app = INDOS()
    app.run()
