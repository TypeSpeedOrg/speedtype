from textual.widget import Widget


class BaseWidget(Widget):

    def hide(self):
        self.styles.display = 'none'

    def show(self):
        self.styles.display = 'block'
