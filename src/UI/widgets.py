import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=40, corner_radius=20, bg='#ffffff', fg='#307DF6',
                 **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, **kwargs)
        self.command = command
        self.bg = bg
        self.fg = fg

        # Create rounded rectangle
        self.rect = self.create_rounded_rect(0, 0, width, height, corner_radius, fill=bg)
        self.text = self.create_text(width / 2, height / 2, text=text, fill=fg, font=("Arial", 14))

        # Bind events
        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_click(self, event):
        self.command()

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill='#f5f5f5')

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg)