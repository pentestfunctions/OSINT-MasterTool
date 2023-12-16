from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QGridLayout, QLineEdit, QScrollArea, QSizeGrip, QSizePolicy,
    QAction, QMessageBox, QTextEdit, QCompleter
)
from PyQt5 import QtCore
import qtmodern.styles
import qtmodern.windows
import sys
from urllib.parse import urlparse
import os
import subprocess

# CustomButton class definition
class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super(CustomButton, self).__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.toggle_selection()
        else:
            super(CustomButton, self).mousePressEvent(event)

    def toggle_selection(self):
        tags = self.property("tags") or []
        if 'selected' in tags:
            tags.remove('selected')
            self.setStyleSheet("")
        else:
            tags.append('selected')
            self.setStyleSheet("background-color: #00FF00;")
        self.setProperty("tags", tags)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filters_menu = None
        self.unique_tags = set()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.initialize_ui()

    def initialize_ui(self):
        self.setWindowTitle("OSINT Master Tool | Developed by Robot™")
        self.setGeometry(0, 0, 1200, 530)
        self.central_widget = QWidget()
        self.central_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setCentralWidget(self.central_widget)
        self.setup_menu_bar()
        self.setup_interface_elements()
        self.setup_layouts()
        self.size_grip = QSizeGrip(self.central_widget)
        self.finalize_layouts()
        self.on_combobox_changed(0)

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("File")

        open_selected_action = QAction("Open All Selected", self)
        open_selected_action.triggered.connect(self.open_all_selected)
        file_menu.addAction(open_selected_action)

        rage_mode_action = QAction("Rage Mode", self)
        rage_mode_action.triggered.connect(self.activate_rage_mode)
        file_menu.addAction(rage_mode_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View Menu
        view_menu = menu_bar.addMenu("View")

        # Filters Submenu
        self.filters_menu = view_menu.addMenu("Filters")

        # Theme options for the View menu
        theme_menu = view_menu.addMenu("Themes")

        default_theme_action = QAction("Default", self)
        default_theme_action.triggered.connect(lambda: self.toggle_theme("default"))
        theme_menu.addAction(default_theme_action)

        default_mix_action = QAction("Default-mix", self)
        default_mix_action.triggered.connect(lambda: self.toggle_theme("default-mix"))
        theme_menu.addAction(default_mix_action)

        dark_theme_action = QAction("Dark", self)
        dark_theme_action.triggered.connect(lambda: self.toggle_theme("dark"))
        theme_menu.addAction(dark_theme_action)

        pink_theme_action = QAction("Pink", self)
        pink_theme_action.triggered.connect(lambda: self.toggle_theme("pink"))
        theme_menu.addAction(pink_theme_action)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")

        # Tips Menu
        extra_tips = QAction("Tips", self)
        extra_tips.triggered.connect(self.show_extra_tips)
        help_menu.addAction(extra_tips)
        
        # About Menu
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def toggle_theme(self, theme_name):
        if theme_name == "default":
            QApplication.setStyle("Fusion")
            self.setStyleSheet("")
        elif theme_name == "default-mix":
            self.apply_default_mix()
        elif theme_name == "dark":
            self.apply_dark_theme()
        elif theme_name == "pink":
            self.apply_pink_theme()

    def apply_default_mix(self):
       default_mix_stylesheet = """
       QWidget {
           /* Neutral colors for a light theme */
           background-color: #F0F0F0;
           color: #000000;
       }
       QPushButton {
           background-color: #E0E0E0;
           border: 1px solid #C0C0C0;
           padding: 5px;
           border-radius: 4px;
       }
       QPushButton:hover {
           background-color: #D3D3D3;
       }
       QPushButton:pressed {
           background-color: #C0C0C0;
       }
       QLineEdit, QTextEdit, QComboBox {
           background-color: #FFFFFF;
           border: 1px solid #C0C0C0;
           padding: 2px;
           border-radius: 4px;
       }
       QLabel, QMenu {
           color: #000000;
       }
       /* Additional styling for scroll bars, sliders, etc. */
       """
       self.setStyleSheet(default_mix_stylesheet)
    
    def apply_dark_theme(self):
        dark_theme_stylesheet = """
        QWidget {
            background-color: #2D2D2D;
            color: #CCCCCC;
        }
        QPushButton {
            background-color: #3C3C3C;
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #626262;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #3C3C3C;
            border: 1px solid #555555;
            padding: 2px;
            border-radius: 4px;
            color: #FFFFFF;
        }
        QLabel, QMenu {
            color: #CCCCCC;
        }
        /* Additional styling for scroll bars, sliders, etc. */
        """
        self.setStyleSheet(dark_theme_stylesheet)
    
    def apply_pink_theme(self):
        pink_theme_stylesheet = """
        QMainWindow {
            background-color: #FFF0F5; /* Light pink background */
        }
        QPushButton {
            background-color: #FF69B4; /* Vibrant pink for buttons */
            color: #FFFFFF; /* White text for contrast */
            border: none; /* No border for a modern look */
            padding: 5px; /* Padding for better touch interaction */
            border-radius: 4px; /* Slightly rounded corners */
        }
        QPushButton:hover {
            background-color: #FFB6C1; /* Lighter pink on hover */
        }
        QPushButton:pressed {
            background-color: #FF1493; /* Deeper pink when pressed */
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #FFFFFF; /* White background for input fields */
            color: #000000; /* Black text for readability */
            border: 1px solid #FFC0CB; /* Light pink border */
            border-radius: 4px; /* Consistent rounded corners */
            padding: 2px; /* Padding for text alignment */
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: #FFC0CB;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }
        QComboBox::down-arrow {
            image: url(path_to_your_down_arrow_icon); /* Replace with the path to your arrow icon */
        }
        QComboBox QAbstractItemView {
            background-color: #FFD1DC; /* Light pink for dropdown list */
            color: #000000;
            selection-background-color: #FF69B4; /* Vibrant pink for selection */
        }
        QLabel, QMenu {
            color: #000000; /* Black text for readability */
        }
        /* Additional styling for scroll bars, sliders, etc., can be added here */
        """
        self.setStyleSheet(pink_theme_stylesheet)

    def open_all_selected(self):
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and 'selected' in widget.property("tags"):
                url = widget.toolTip()
                if url:
                    self.open_url(url)
 
    def activate_rage_mode(self):
        selected_filters = [action.text() for action in self.filters_menu.actions() if action.isChecked()]
        manual_filter = self.filter_input.text().lower()
        urls_to_open = []
    
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                tags = widget.property("tags")
                url = widget.toolTip()
                text_matches = manual_filter in widget.text().lower() or manual_filter in url.lower()
    
                if (not selected_filters or any(tag in selected_filters for tag in tags)) and (not manual_filter or text_matches):
                    if url:
                        urls_to_open.append(url)
    
        # Rage mode stuff for confirmation dialog
        count = len(urls_to_open)
        reply = QMessageBox.question(self, 'Rage Mode Confirmation',
                                     f'You are about to open {count} URLs. Do you want to continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
        if reply == QMessageBox.Yes:
            for url in urls_to_open:
                self.open_url(url)

    def apply_category_filter(self):
        selected_filters = [action.text() for action in self.filters_menu.actions() if action.isChecked()]
        self.filter_buttons(selected_filters)

    def filter_buttons(self, selected_filters):
        for i in range(self.grid_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            if isinstance(button, QPushButton):
                tags = button.property("tags")
                if any(tag in selected_filters for tag in tags):
                    button.show()
                else:
                    button.hide()

    def show_extra_tips(self):
        about_text = (
            "<h1>Extra tips for the wicked</h1>"
            "<p>Make sure you manually check things like:</strong></p>"
            "<ul>"
            "<li>Requesting $0.01 on paypal from their email address</li>"
            "<li>Checking email headers for IP addresses</li>"
            "<li>Checking any pictures you have for EXIF data</li>"
            "<li>Check pimeyes for facial recognition on any pictures you have of them</li>"
            "<p>If you have a rough location, job etc use that for dorks to find information</strong></p>"
            "<p>Look for where they have talked about certain items they own, if you have a picture of something they have owned - ask them about it in a sly manner to see how they respond confirming their identity</strong></p>"
            "</ul>"
        )
        QMessageBox.about(self, "Extra tips & hints", about_text)

    def show_about_dialog(self):
        about_text = (
            "<h1>OSINT Master Tool</h1>"
            "<p><strong>Version:</strong> 1.0</p>"
            "<p>This tool is designed to assist in Open Source Intelligence (OSINT) by aggregating various online resources and tools related to specific query types such as email addresses, usernames, and domains.</p>"
            "<p><strong>Features:</strong></p>"
            "<ul>"
            "<li>Search across multiple platforms using email, username, or domain.</li>"
            "<li>Access to a wide range of OSINT resources with easy navigation.</li>"
            "<li>Filter results based on categories like social media, DNS records, and more.</li>"
            "<li>User-friendly interface with theme customization.</li>"
            "</ul>"
            "<p>Developed with the intention of simplifying online investigations and research, OSINT Master Tool serves as a convenient hub for various OSINT-related queries and data exploration.</p>"
        )
        QMessageBox.about(self, "About OSINT Master Tool", about_text)

    def setup_interface_elements(self):
        self.example_combo_box = QComboBox()
        self.example_combo_box.addItems(["Email Address", "Username", "Domain", "IP Address", "Phone Number"])
        self.example_combo_box.currentIndexChanged.connect(self.on_combobox_changed)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter email address")

        # filter input
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter domains or keywords")
        self.filter_input.textChanged.connect(self.apply_filter)
    
        self.completer = QCompleter([])
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_input.setCompleter(self.completer)

    def setup_layouts(self):
        # making section for notes
        horizontal_layout = QHBoxLayout()
    
        # notes section
        self.notes_text_edit = QTextEdit()
        self.notes_text_edit.setPlaceholderText("Enter your notes here...")
        self.notes_text_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        horizontal_layout.addWidget(self.notes_text_edit, 2)  # Adjust the ratio as needed
    
        # Main content layout
        main_content_layout = QVBoxLayout()
        main_content_layout.addWidget(self.example_combo_box)
        main_content_layout.addWidget(self.input_field)
    
        # Scroll area for the grid layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        main_content_layout.addWidget(self.scroll_area)
    
        # Filter input
        main_content_layout.addWidget(self.filter_input)
    
        # Add main content layout to the horizontal layout
        horizontal_layout.addLayout(main_content_layout, 8)
    
        # Set the horizontal layout to the central widget
        self.central_widget.setLayout(horizontal_layout)

    def on_combobox_changed(self, index):
        self.clear_content_layout()
        self.input_field.clear()
        self.current_option = self.example_combo_box.itemText(index)
        self.input_field.setPlaceholderText(f"Enter {self.current_option.lower()}")
        self.input_field.textChanged.connect(self.setup_grid_layout)
        self.setup_grid_layout()
        self.update_view_menu()

    def update_view_menu(self):
        self.filters_menu.clear()
        self.unique_tags.clear()
        self.generate_urls()  # Call generate_urls to update self.unique_tags based on the current option
        for tag in sorted(self.unique_tags):
            action = QAction(tag, self, checkable=True)
            action.triggered.connect(self.apply_category_filter)
            self.filters_menu.addAction(action)


    def generate_urls(self):
        user_input = self.input_field.text()
        urls = []
        if self.current_option == "Username":
            username_urls = [
                {"url": "https://about.me/$username", "tags": ["profile", "social media"]},
                {"url": "https://ask.fm/$username", "tags": ["profile", "social media"]},
                {"url": "https://buzzfeed.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://chaos.social/@$username", "tags": ["profile", "social media"]},
                {"url": "https://community.eintracht.de/fans/$username", "tags": ["profile", "social media"]},
                {"url": "https://imgur.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://medium.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://myspace.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://pastebin.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://play.google.com/store/apps/developer?id=$username", "tags": ["profile", "social media"]},
                {"url": "https://soundcloud.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://themeforest.net/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://twitter.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://behance.net/$username", "tags": ["profile", "social media"]},
                {"url": "https://reverbnation.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://wykop.pl/ludzie/$username", "tags": ["profile", "social media"]},
                {"url": "https://$username.bandcamp.com/", "tags": ["profile", "social media"]},
                {"url": "https://$username.newgrounds.com", "tags": ["profile", "social media"]},
                {"url": "http://dating.ru/$username", "tags": ["profile", "social media"]},
                {"url": "http://en.gravatar.com/$username", "tags": ["profile", "social media"]},
                {"url": "http://forum.3dnews.ru/member.php?username=$username", "tags": ["profile", "social media"]},
                {"url": "http://forum.igromania.ru/member.php?username=$username", "tags": ["profile", "social media"]},
                {"url": "http://promodj.com/$username", "tags": ["profile", "social media"]},
                {"url": "http://uid.me/$username", "tags": ["profile", "social media"]},
                {"url": "http://authorstream.com/$username/", "tags": ["profile", "social media"]},
                {"url": "http://jeuxvideo.com/profil/$username?mode=infos", "tags": ["profile", "social media"]},
                {"url": "http://wikidot.com/user:info/$username", "tags": ["profile", "social media"]},
                {"url": "https://$username.blogspot.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.booth.pm/", "tags": ["profile", "social media"]},
                {"url": "https://$username.carbonmade.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.contently.com/", "tags": ["profile", "social media"]},
                {"url": "https://$username.crevado.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.deviantart.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.exposure.co/", "tags": ["profile", "social media"]},
                {"url": "https://$username.gitbook.io/", "tags": ["profile", "social media"]},
                {"url": "https://$username.itch.io/", "tags": ["profile", "social media"]},
                {"url": "https://$username.jimdosite.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.livejournal.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.newgrounds.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.rajce.idnes.cz/", "tags": ["profile", "social media"]},
                {"url": "https://$username.skyrock.com/", "tags": ["profile", "social media"]},
                {"url": "https://$username.slack.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.smugmug.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.webnode.cz/", "tags": ["profile", "social media"]},
                {"url": "https://$username.weebly.com/", "tags": ["profile", "social media"]},
                {"url": "https://$username.wix.com", "tags": ["profile", "social media"]},
                {"url": "https://$username.wordpress.com/", "tags": ["profile", "social media"]},
                {"url": "https://$username.www.nn.ru/", "tags": ["profile", "social media"]},
                {"url": "https://2Dimensions.com/a/$username", "tags": ["profile", "social media"]},
                {"url": "https://8tracks.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://account.venmo.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://admireme.vip/$username", "tags": ["profile", "social media"]},
                {"url": "https://airbit.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://airlinepilot.life/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://akniga.org/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://allmylinks.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://aminoapps.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://anilist.co/user/$username/", "tags": ["profile", "social media"]},
                {"url": "https://apclips.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://api.mojang.com/users/profiles/minecraft/$username", "tags": ["profile", "social media"]},
                {"url": "https://app.intigriti.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://apps.runescape.com/runemetrics/app/overview/player/$username", "tags": ["profile", "social media"]},
                {"url": "https://archive.org/details/@$username", "tags": ["profile", "social media"]},
                {"url": "https://archiveofourown.org/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://asciinema.org/~$username", "tags": ["profile", "social media"]},
                {"url": "https://ask.fedoraproject.org/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://audiojungle.net/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://auth.geeksforgeeks.org/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://bezuzyteczna.pl/uzytkownicy/$username", "tags": ["profile", "social media"]},
                {"url": "https://bitbucket.org/$username/", "tags": ["profile", "social media"]},
                {"url": "https://bitcoinforum.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://blip.fm/$username", "tags": ["profile", "social media"]},
                {"url": "https://blog.naver.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://bodyspace.bodybuilding.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://buymeacoff.ee/$username", "tags": ["profile", "social media"]},
                {"url": "https://caddy.community/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://career.habr.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://ch.tetr.io/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://chaturbate.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://choice.community/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://clapperapp.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://codeforces.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://codepen.io/$username", "tags": ["profile", "social media"]},
                {"url": "https://coderwall.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://codesnippets.fandom.com/wiki/User:$username", "tags": ["profile", "social media"]},
                {"url": "https://coinvote.cc/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://community.bitwarden.com/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://community.brave.com/u/$username/", "tags": ["profile", "social media"]},
                {"url": "https://community.cartalk.com/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://community.cloudflare.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://community.cryptomator.org/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://community.icons8.com/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://community.native-instruments.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://community.oracle.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://community.signalusers.org/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://community.windy.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://community.wolfram.com/web/$username/home", "tags": ["profile", "social media"]},
                {"url": "https://crowdin.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://ctan.org/author/$username", "tags": ["profile", "social media"]},
                {"url": "https://cults3d.com/en/users/$username/creations", "tags": ["profile", "social media"]},
                {"url": "https://d3.ru/user/$username/posts", "tags": ["profile", "social media"]},
                {"url": "https://data.typeracer.com/pit/profile?user=$username", "tags": ["profile", "social media"]},
                {"url": "https://dev.to/$username", "tags": ["profile", "social media"]},
                {"url": "https://developer.apple.com/forums/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://deviantart.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://devrant.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://discourse.joplinapp.org/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://discourse.wicg.io/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://discuss.elastic.co/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://discussions.apple.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://disqus.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://disqus.com/by/$username", "tags": ["profile", "social media"]},
                {"url": "https://dmoj.ca/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://dribbble.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://ebio.gg/$username", "tags": ["profile", "social media"]},
                {"url": "https://egpu.io/forums/profile/$username/", "tags": ["profile", "social media"]},
                {"url": "https://en.wikipedia.org/wiki/Special:CentralAuth/$username?uselang=qqx", "tags": ["profile", "social media"]},
                {"url": "https://euw.op.gg/summoner/userName=$username", "tags": ["profile", "social media"]},
                {"url": "https://f3.cool/$username/", "tags": ["profile", "social media"]},
                {"url": "https://facebook.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://fameswap.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://fiverr.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://flickr.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://flipboard.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://fortnitetracker.com/profile/all/$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.dangerousthings.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.guns.ru/forummisc/blog/$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.hackthebox.eu/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.ionicframework.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.leasehackr.com/u/$username/summary/", "tags": ["profile", "social media"]},
                {"url": "https://forum.rclone.org/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.sublimetext.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.velomania.ru/member.php?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://forums.envato.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://forums.mmorpg.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://forums.pcgamer.com/members/?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://forums.whonix.org/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://fosstodon.org/@$username", "tags": ["profile", "social media"]},
                {"url": "https://freelance.habr.com/freelancers/$username", "tags": ["profile", "social media"]},
                {"url": "https://freesound.org/people/$username/", "tags": ["profile", "social media"]},
                {"url": "https://genius.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://genius.com/artists/$username", "tags": ["profile", "social media"]},
                {"url": "https://gfycat.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://giphy.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://gitee.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://github.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://github.com/search?q=$username&type=repositories", "tags": ["profile", "social media"]},
                {"url": "https://gitlab.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://gitlab.gnome.org/$username", "tags": ["profile", "social media"]},
                {"url": "https://grep.app/search?q=$username", "tags": ["profile", "social media"]},
                {"url": "https://habr.com/ru/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://hackaday.io/$username", "tags": ["profile", "social media"]},
                {"url": "https://hackerearth.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://hackerone.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://hackerrank.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://hashnode.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://help.nextcloud.com/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://holopin.io/@$username", "tags": ["profile", "social media"]},
                {"url": "https://hosted.weblate.org/user/$username/", "tags": ["profile", "social media"]},
                {"url": "https://houzz.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://hub.docker.com/u/$username/", "tags": ["profile", "social media"]},
                {"url": "https://hubpages.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://hubski.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://icq.im/$username/en", "tags": ["profile", "social media"]},
                {"url": "https://imgsrc.ru/main/user.php?user=$username", "tags": ["profile", "social media"]},
                {"url": "https://imgup.cz/$username", "tags": ["profile", "social media"]},
                {"url": "https://independent.academia.edu/$username", "tags": ["profile", "social media"]},
                {"url": "https://instagram.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://irc-galleria.net/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://irecommend.ru/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://issuu.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://jbzd.com.pl/uzytkownik/$username", "tags": ["profile", "social media"]},
                {"url": "https://keybase.io/$username", "tags": ["profile", "social media"]},
                {"url": "https://kik.me/$username", "tags": ["profile", "social media"]},
                {"url": "https://ko-fi.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://kwork.ru/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://lab.pentestit.ru/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://last.fm/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://launchpad.net/~$username", "tags": ["profile", "social media"]},
                {"url": "https://leetcode.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://letterboxd.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://lichess.org/@/$username", "tags": ["profile", "social media"]},
                {"url": "https://linktr.ee/$username", "tags": ["profile", "social media"]},
                {"url": "https://listed.to/@$username", "tags": ["profile", "social media"]},
                {"url": "https://lobste.rs/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://lolchess.gg/profile/na/$username", "tags": ["profile", "social media"]},
                {"url": "https://lottiefiles.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://mapify.travel/$username", "tags": ["profile", "social media"]},
                {"url": "https://mastodon.cloud/@$username", "tags": ["profile", "social media"]},
                {"url": "https://mastodon.social/@$username", "tags": ["profile", "social media"]},
                {"url": "https://mastodon.technology/@$username", "tags": ["profile", "social media"]},
                {"url": "https://mastodon.xyz/@$username", "tags": ["profile", "social media"]},
                {"url": "https://moikrug.ru/$username", "tags": ["profile", "social media"]},
                {"url": "https://monkeytype.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://motherless.com/m/$username", "tags": ["profile", "social media"]},
                {"url": "https://mstdn.io/@$username", "tags": ["profile", "social media"]},
                {"url": "https://music.yandex/users/$username/playlists", "tags": ["profile", "social media"]},
                {"url": "https://my.flightradar24.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://myanimelist.net/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://nationstates.net/nation=$username", "tags": ["profile", "social media"]},
                {"url": "https://nationstates.net/region=$username", "tags": ["profile", "social media"]},
                {"url": "https://news.ycombinator.com/user?id=$username", "tags": ["profile", "social media"]},
                {"url": "https://nightbot.tv/t/$username/commands", "tags": ["profile", "social media"]},
                {"url": "https://ninjakiwi.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://notabug.org/$username", "tags": ["profile", "social media"]},
                {"url": "https://note.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://nyaa.si/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://ogu.gg/$username", "tags": ["profile", "social media"]},
                {"url": "https://open.spotify.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://opensource.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://osu.ppy.sh/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://ourdjtalk.com/members?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://packagist.org/packages/$username/", "tags": ["profile", "social media"]},
                {"url": "https://patreon.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://php.ru/forum/members/?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://pikabu.ru/@$username", "tags": ["profile", "social media"]},
                {"url": "https://plugins.gradle.org/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://pocketstars.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://pokemonshowdown.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://polarsteps.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://polymart.org/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://pornhub.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://pr0gramm.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://profil.chatujme.cz/$username", "tags": ["profile", "social media"]},
                {"url": "https://profile.codersrank.io/user/$username/", "tags": ["profile", "social media"]},
                {"url": "https://profiles.wordpress.org/$username/", "tags": ["profile", "social media"]},
                {"url": "https://prog.hu/azonosito/info/$username", "tags": ["profile", "social media"]},
                {"url": "https://psnprofiles.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://pt.bongacams.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://pypi.org/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://queer.af/@$username", "tags": ["profile", "social media"]},
                {"url": "https://rateyourmusic.com/~$username", "tags": ["profile", "social media"]},
                {"url": "https://reddit.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://replit.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://robertsspaceindustries.com/citizens/$username", "tags": ["profile", "social media"]},
                {"url": "https://royalcams.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://rubygems.org/profiles/$username", "tags": ["profile", "social media"]},
                {"url": "https://rumble.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://satsis.info/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://scholar.harvard.edu/$username", "tags": ["profile", "social media"]},
                {"url": "https://scratch.mit.edu/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://search.0t.rocks/records?usernames=$username", "tags": ["profile", "social media"]},
                {"url": "https://sessionize.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://sketchfab.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://slashdot.org/~$username", "tags": ["profile", "social media"]},
                {"url": "https://slides.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://slideshare.net/$username", "tags": ["profile", "social media"]},
                {"url": "https://social.tchncs.de/@$username", "tags": ["profile", "social media"]},
                {"url": "https://sourceforge.net/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://soylentnews.org/~$username", "tags": ["profile", "social media"]},
                {"url": "https://speedrun.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://spletnik.ru/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://splice.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://splits.io/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://steamcommunity.com/groups/$username", "tags": ["profile", "social media"]},
                {"url": "https://swapd.co/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://t.me/$username", "tags": ["profile", "social media"]},
                {"url": "https://tellonym.me/$username", "tags": ["profile", "social media"]},
                {"url": "https://tenor.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://tiktok.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://tldrlegal.com/users/$username/", "tags": ["profile", "social media"]},
                {"url": "https://traewelling.de/@$username", "tags": ["profile", "social media"]},
                {"url": "https://traktrain.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://translate.jellyfin.org/user/$username/", "tags": ["profile", "social media"]},
                {"url": "https://trashbox.ru/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://trello.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://tryhackme.com/p/$username", "tags": ["profile", "social media"]},
                {"url": "https://tumblr.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://tuna.voicemod.net/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://tweakers.net/gallery/$username", "tags": ["profile", "social media"]},
                {"url": "https://twitch.tv/$username", "tags": ["profile", "social media"]},
                {"url": "https://ultimate-guitar.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://unsplash.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://vero.co/$username", "tags": ["profile", "social media"]},
                {"url": "https://vimeo.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://virgool.io/@$username", "tags": ["profile", "social media"]},
                {"url": "https://vk.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://vsco.co/$username", "tags": ["profile", "social media"]},
                {"url": "https://wiki.vg/User:$username", "tags": ["profile", "social media"]},
                {"url": "https://7cups.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://9gag.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://airliners.net/user/$username/profile/photos", "tags": ["profile", "social media"]},
                {"url": "https://alik.cz/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://allthingsworn.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://artstation.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://autofrage.net/nutzer/$username", "tags": ["profile", "social media"]},
                {"url": "https://avizo.cz/$username/", "tags": ["profile", "social media"]},
                {"url": "https://baby.ru/u/$username/", "tags": ["profile", "social media"]},
                {"url": "https://babyblog.ru/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://bandcamp.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://bazar.cz/$username/", "tags": ["profile", "social media"]},
                {"url": "https://biggerpockets.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://bikemap.net/en/u/$username/routes/created/", "tags": ["profile", "social media"]},
                {"url": "https://bookcrossing.com/mybookshelf/$username/", "tags": ["profile", "social media"]},
                {"url": "https://cgtrader.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://championat.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://chess.com/member/$username", "tags": ["profile", "social media"]},
                {"url": "https://clozemaster.com/players/$username", "tags": ["profile", "social media"]},
                {"url": "https://clubhouse.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://cnet.com/profiles/$username/", "tags": ["profile", "social media"]},
                {"url": "https://codecademy.com/profiles/$username", "tags": ["profile", "social media"]},
                {"url": "https://codechef.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://codewars.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://colourlovers.com/lover/$username", "tags": ["profile", "social media"]},
                {"url": "https://coroflot.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://couchsurfing.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://cracked.com/members/$username/", "tags": ["profile", "social media"]},
                {"url": "https://dailykos.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://dailymotion.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://dealabs.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://discogs.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://drive2.ru/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://duolingo.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://erome.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://etsy.com/shop/$username", "tags": ["profile", "social media"]},
                {"url": "https://eyeem.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://fandom.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://finanzfrage.net/nutzer/$username", "tags": ["profile", "social media"]},
                {"url": "https://fiverr.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://fixya.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://fl.ru/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://flickr.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://forumophilia.com/profile.php?mode=viewprofile&u=$username", "tags": ["profile", "social media"]},
                {"url": "https://freecodecamp.org/$username", "tags": ["profile", "social media"]},
                {"url": "https://freelancer.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://furaffinity.net/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://g2g.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://gaiaonline.com/profiles/$username", "tags": ["profile", "social media"]},
                {"url": "https://gamespot.com/profile/$username/", "tags": ["profile", "social media"]},
                {"url": "https://geocaching.com/p/default.aspx?u=$username", "tags": ["profile", "social media"]},
                {"url": "https://gesundheitsfrage.net/nutzer/$username", "tags": ["profile", "social media"]},
                {"url": "https://getmyuni.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://giantbomb.com/profile/$username/", "tags": ["profile", "social media"]},
                {"url": "https://github.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://goodreads.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://grailed.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://gumroad.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://gutefrage.net/nutzer/$username", "tags": ["profile", "social media"]},
                {"url": "https://hackster.io/$username", "tags": ["profile", "social media"]},
                {"url": "https://heavy-r.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://hexrpg.com/userinfo/$username", "tags": ["profile", "social media"]},
                {"url": "https://hunting.ru/forum/members/?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://ifttt.com/p/$username", "tags": ["profile", "social media"]},
                {"url": "https://imagefap.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://instructables.com/member/$username", "tags": ["profile", "social media"]},
                {"url": "https://interpals.net/$username", "tags": ["profile", "social media"]},
                {"url": "https://itemfix.com/c/$username", "tags": ["profile", "social media"]},
                {"url": "https://kaggle.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://keakr.com/en/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://kickstarter.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://kongregate.com/accounts/$username", "tags": ["profile", "social media"]},
                {"url": "https://lesswrong.com/users/@$username", "tags": ["profile", "social media"]},
                {"url": "https://linux.org.ru/people/$username/profile", "tags": ["profile", "social media"]},
                {"url": "https://livelib.ru/reader/$username", "tags": ["profile", "social media"]},
                {"url": "https://lushstories.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://memrise.com/user/$username/", "tags": ["profile", "social media"]},
                {"url": "https://mercadolivre.com.br/perfil/$username", "tags": ["profile", "social media"]},
                {"url": "https://metacritic.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://minds.com/$username/", "tags": ["profile", "social media"]},
                {"url": "https://mixcloud.com/$username/", "tags": ["profile", "social media"]},
                {"url": "https://modelhub.com/$username/videos", "tags": ["profile", "social media"]},
                {"url": "https://motorradfrage.net/nutzer/$username", "tags": ["profile", "social media"]},
                {"url": "https://mydramalist.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://myminifactory.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://nairaland.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://needrom.com/author/$username/", "tags": ["profile", "social media"]},
                {"url": "https://nintendolife.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://nitrotype.com/racer/$username", "tags": ["profile", "social media"]},
                {"url": "https://npmjs.com/~$username", "tags": ["profile", "social media"]},
                {"url": "https://opennet.ru/~$username", "tags": ["profile", "social media"]},
                {"url": "https://openstreetmap.org/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://patreon.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://pepper.it/profile/$username/overview", "tags": ["profile", "social media"]},
                {"url": "https://periscope.tv/$username/", "tags": ["profile", "social media"]},
                {"url": "https://pinkbike.com/u/$username/", "tags": ["profile", "social media"]},
                {"url": "https://pinterest.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://polygon.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://producthunt.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://redbubble.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://reddit.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://redtube.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://reisefrage.net/nutzer/$username", "tags": ["profile", "social media"]},
                {"url": "https://researchgate.net/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://roblox.com/user.aspx?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://rockettube.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://rusfootball.info/user/$username/", "tags": ["profile", "social media"]},
                {"url": "https://sbazar.cz/$username", "tags": ["profile", "social media"]},
                {"url": "https://scribd.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://searchblogspot.com/search?q=$username", "tags": ["profile", "social media"]},
                {"url": "https://shitpostbot.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://shpock.com/shop/$username/items", "tags": ["profile", "social media"]},
                {"url": "https://slant.co/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://smule.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://snapchat.com/add/$username", "tags": ["profile", "social media"]},
                {"url": "https://sporcle.com/user/$username/people", "tags": ["profile", "social media"]},
                {"url": "https://sportlerfrage.net/nutzer/$username", "tags": ["profile", "social media"]},
                {"url": "https://sports.ru/profile/$username/", "tags": ["profile", "social media"]},
                {"url": "https://strava.com/athletes/$username", "tags": ["profile", "social media"]},
                {"url": "https://svidbook.ru/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://tiktok.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://tnaflix.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://toster.ru/user/$username/answers", "tags": ["profile", "social media"]},
                {"url": "https://tradingview.com/u/$username/", "tags": ["profile", "social media"]},
                {"url": "https://trakt.tv/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://twitch.tv/$username", "tags": ["profile", "social media"]},
                {"url": "https://virustotal.com/gui/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://warriorforum.com/members/$username.html", "tags": ["profile", "social media"]},
                {"url": "https://wattpad.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://wordnik.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://younow.com/$username/", "tags": ["profile", "social media"]},
                {"url": "https://zhihu.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://znanylekarz.pl/$username", "tags": ["profile", "social media"]},
                {"url": "https://xboxgamertag.com/search/$username", "tags": ["profile", "social media"]},
                {"url": "https://xhamster.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://xvideos.com/profiles/$username", "tags": ["profile", "social media"]},
                {"url": "https://youpic.com/photographer/$username/", "tags": ["profile", "social media"]},
                {"url": "https://youporn.com/uservids/$username", "tags": ["profile", "social media"]},
                {"url": "https://youtube.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://forums.adobe.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://angel.co/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://$username.basecamphq.com", "tags": ["profile", "social media"]},
                {"url": "http://blackplanet.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://canva.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://codementor.io/@$username", "tags": ["profile", "social media"]},
                {"url": "https://evewho.com/pilot/$username/", "tags": ["profile", "social media"]},
                {"url": "http://fanpop.com/fans/$username", "tags": ["profile", "social media"]},
                {"url": "https://fotolog.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://foursquare.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://gpodder.net/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://investing.com/traders/$username", "tags": ["profile", "social media"]},
                {"url": "https://khanacademy.org/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://kiwifarms.net/members/?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://linkedin.com/in/$username", "tags": ["profile", "social media"]},
                {"url": "https://npmjs.com/package/$username", "tags": ["profile", "social media"]},
                {"url": "https://pexels.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://pixabay.com/en/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://powershellgallery.com/profiles/$username", "tags": ["profile", "social media"]},
                {"url": "https://dating.rambler.ru/page/$username", "tags": ["profile", "social media"]},
                {"url": "http://shockwave.com/member/profiles/$username.jsp", "tags": ["profile", "social media"]},
                {"url": "https://stream.me/$username", "tags": ["profile", "social media"]},
                {"url": "https://user.teknik.io/$username", "tags": ["profile", "social media"]},
                {"url": "https://market.yandex.ru/user/$username/achievements", "tags": ["profile", "social media"]},
                {"url": "http://$username.insanejournal.com/profile", "tags": ["profile", "social media"]},
                {"url": "https://trip.skyscanner.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://sports-tracker.com/view_profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://bbs.boingboing.net/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://elwo.ru/index/8-0-$username", "tags": ["profile", "social media"]},
                {"url": "http://ingvarr.net.ru/index/8-0-$username", "tags": ["profile", "social media"]},
                {"url": "https://forum.redsun.tf/members/?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://creativemarket.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://pvpru.com/board/member.php?username=$username&tab=aboutme#aboutme", "tags": ["profile", "social media"]},
                {"url": "https://easyen.ru/index/8-0-$username", "tags": ["profile", "social media"]},
                {"url": "http://pedsovet.su/index/8-0-$username", "tags": ["profile", "social media"]},
                {"url": "https://radioskot.ru/index/8-0-$username", "tags": ["profile", "social media"]},
                {"url": "https://coderwall.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://tamtam.chat/$username", "tags": ["profile", "social media"]},
                {"url": "https://zomato.com/pl/$username/foodjourney", "tags": ["profile", "social media"]},
                {"url": "https://mixer.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://api.kano.me/progress/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://yandex.ru/collections/user/$username/", "tags": ["profile", "social media"]},
                {"url": "https://paypal.com/paypalme/$username", "tags": ["profile", "social media"]},
                {"url": "https://imageshack.us/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://$username.en.aptoide.com/", "tags": ["profile", "social media"]},
                {"url": "https://crunchyroll.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://support.t-mobile.com/people/$username", "tags": ["profile", "social media"]},
                {"url": "https://opencollective.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://segmentfault.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "http://fr.viadeo.com/en/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://meetme.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://tracr.co/users/1/$username", "tags": ["profile", "social media"]},
                {"url": "https://taringa.net/$username", "tags": ["profile", "social media"]},
                {"url": "https://photobucket.com/user/$username/library", "tags": ["profile", "social media"]},
                {"url": "https://4pda.ru/forum/index.php?act=search&source=pst&noform=1&username=$username", "tags": ["profile", "social media"]},
                {"url": "http://pokerstrategy.net/user/$username/profile/", "tags": ["profile", "social media"]},
                {"url": "https://filmo.gs/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://500px.com/p/$username", "tags": ["profile", "social media"]},
                {"url": "https://badoo.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://pling.com/u/$username/", "tags": ["profile", "social media"]},
                {"url": "https://realmeye.com/player/$username", "tags": ["profile", "social media"]},
                {"url": "https://travellerspoint.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://gdprofiles.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://alltrails.com/members/$username", "tags": ["profile", "social media"]},
                {"url": "https://beta.cent.co/@$username", "tags": ["profile", "social media"]},
                {"url": "https://anobii.com/$username/profile", "tags": ["profile", "social media"]},
                {"url": "https://forums.kali.org/member.php?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://namemc.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://steamid.uk/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://tripadvisor.com/members/$username", "tags": ["profile", "social media"]},
                {"url": "https://house-mixes.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://quora.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://sparkpeople.com/mypage.asp?id=$username", "tags": ["profile", "social media"]},
                {"url": "https://cloob.com/name/$username", "tags": ["profile", "social media"]},
                {"url": "https://1337x.to/user/$username/", "tags": ["profile", "social media"]},
                {"url": "http://en.tm-ladder.com/$username_rech.php", "tags": ["profile", "social media"]},
                {"url": "https://plug.dj/@/$username", "tags": ["profile", "social media"]},
                {"url": "https://facenama.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://designspiration.net/$username/", "tags": ["profile", "social media"]},
                {"url": "https://capfriendly.com/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://gab.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://fancentro.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://codeforces.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://smashcast.tv/api/media/live/$username", "tags": ["profile", "social media"]},
                {"url": "https://countable.us/$username", "tags": ["profile", "social media"]},
                {"url": "https://open.spotify.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://steamcommunity.com/id/$username", "tags": ["profile", "social media"]},
                {"url": "https://raidforums.com/User-$username", "tags": ["profile", "social media"]},
                {"url": "https://pinterest.com/$username/", "tags": ["profile", "social media"]},
                {"url": "https://pcpartpicker.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://ebay.com/usr/$username", "tags": ["profile", "social media"]},
                {"url": "https://ebay.de/usr/$username", "tags": ["profile", "social media"]},
                {"url": "https://$username.ghost.io/", "tags": ["profile", "social media"]},
                {"url": "https://discuss.atom.io/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://gam1ng.com.br/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://ogusers.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://otzovik.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://echo.msk.ru/users/$username", "tags": ["profile", "social media"]},
                {"url": "https://ello.co/$username", "tags": ["profile", "social media"]},
                {"url": "https://github.community/u/$username/summary", "tags": ["profile", "social media"]},
                {"url": "https://gurushots.com/$username/photos", "tags": ["profile", "social media"]},
                {"url": "https://g.dev/$username", "tags": ["profile", "social media"]},
                {"url": "https://mastodon.technology/@$username", "tags": ["profile", "social media"]},
                {"url": "https://zoomit.ir/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://facebook.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://binarysearch.io/@/$username", "tags": ["profile", "social media"]},
                {"url": "https://create.arduino.cc/projecthub/$username", "tags": ["profile", "social media"]},
                {"url": "https://kooapp.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://weheartit.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://tinder.com/@$username", "tags": ["profile", "social media"]},
                {"url": "https://coil.com/u/$username", "tags": ["profile", "social media"]},
                {"url": "https://onlyfans.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://instagram.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://ok.ru/$username", "tags": ["profile", "social media"]},
                {"url": "https://forumhouse.ru/members/?username=$username", "tags": ["profile", "social media"]},
                {"url": "https://enjin.com/profile/$username", "tags": ["profile", "social media"]},
                {"url": "https://irl.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://munzee.com/m/$username", "tags": ["profile", "social media"]},
                {"url": "https://quizlet.com/$username", "tags": ["profile", "social media"]},
                {"url": "https://youtube.com/c/$username", "tags": ["profile", "social media"]},
                {"url": "https://youtube.com/user/$username", "tags": ["profile", "social media"]},
                {"url": "https://forums.gunsandammo.com/profile/$username", "tags": ["profile", "social media"]},
            ]
            urls = [{"url": url["url"].replace('$username', user_input), "tags": url["tags"]} for url in username_urls]
        elif self.current_option == "Domain":
            domain_urls = [
                {"url": "https://viewdns.info/reverseip/?host=$domain&t=1", "tags": ["DNS", "Hosting", "Shared Servers", "IP Lookup"]},
                {"url": "https://viewdns.info/iphistory/?domain=$domain", "tags": ["DNS", "History", "Networking", "Domain Information"]},
                {"url": "https://viewdns.info/httpheaders/?domain=$domain", "tags": ["DNS", "HTTP Headers", "Networking", "Web Headers"]},
                {"url": "https://web.archive.org/cdx/search/cdx?url=*.$domain&output=xml&fl=original&collapse=urlkey", "tags": ["Archives", "Networking", "Web History", "Archived Pages"]},
                {"url": "https://web.archive.org/web/20230000000000*/$domain", "tags": ["Archives", "Networking", "Web History", "Archived Pages"]},
                {"url": "https://viewdns.info/dnsrecord/?domain=$domain", "tags": ["DNS", "History", "Networking", "DNS Records"]},
                {"url": "https://viewdns.info/portscan/?host=$domain", "tags": ["Ports", "Networking", "Security", "Network Scanning"]},
                {"url": "https://crt.sh/?q=$domain", "tags": ["Certificates", "Networking", "SSL/TLS", "Certificate Search"]},
                {"url": "https://who.is/whois/$domain", "tags": ["Whois", "Networking", "Domain Information", "Whois Lookup"]},
                {"url": "https://securitytrails.com/list/apex_domain/$domain", "tags": ["Subdomains", "Networking", "Domain Information", "Subdomain Search"]},
                {"url": "https://urlscan.io/search/#$domain", "tags": ["DNS", "Networking", "URL Analysis", "Website Scanning"]},
                {"url": "https://www.shodan.io/search?query=$domain", "tags": ["DNS", "Networking", "IoT", "Shodan Search"]},
                {"url": "https://search.censys.io/search?resource=hosts&sort=RELEVANCE&per_page=25&virtual_hosts=EXCLUDE&q=$domain", "tags": ["DNS", "Networking", "Security", "Host Search"]},
                {"url": "https://dnshistory.org/dns-records/$domain", "tags": ["DNS", "History", "Records", "DNS Record History"]},
                {"url": "https://www.wappalyzer.com/lookup/$domain/", "tags": ["Software", "Networking", "Website Analysis", "Technology Detection"]},
                {"url": "https://builtwith.com/$domain", "tags": ["DNS", "Hosting", "Subdomains", "Technology Detection"]},
                {"url": "https://sitereport.netcraft.com/?url=http://$domain", "tags": ["DNS", "Networking", "Website Analysis", "Site Report"]},
                {"url": "https://www.statscrop.com/www/$domain", "tags": ["DNS", "Networking", "Website Analysis", "Website Stats"]},
                {"url": "https://spyonweb.com/$domain", "tags": ["DNS", "Networking", "Website Analysis", "Online Visibility"]},
                {"url": "https://securityheaders.com/?q=$domain&followRedirects=on", "tags": ["DNS", "Networking", "Security", "HTTP Security Headers"]},
                {"url": "https://github.com/search?q=$domain&type=code", "tags": ["DNS", "Code", "Networking", "Code Search"]},
                {"url": "https://grep.app/search?q=$domain", "tags": ["DNS", "Networking", "Code", "Code Search"]},
                {"url": "https://trends.google.com/trends/explore?q=$domain", "tags": ["DNS", "Trends", "Networking", "Google Trends"]},
                {"url": "https://dnssec-debugger.verisignlabs.com/$domain", "tags": ["DNS", "Networking", "DNSSEC", "DNS Security"]},
                {"url": "https://dnsviz.net/d/$domain/analyze/", "tags": ["DNS", "Networking", "DNS Analysis", "DNS Visualization"]},
                {"url": "https://buckets.grayhatwarfare.com/files?keywords=$domain", "tags": ["DNS", "Networking", "Cloud Storage", "Bucket Search"]}
            ]
            urls = [{"url": url["url"].replace('$domain', user_input), "tags": url["tags"]} for url in domain_urls]
        elif self.current_option == "Email Address":
            email_urls = [
                {"url": "https://viewdns.info/reversewhois/?q=$email", "tags": ["domain", "whois"]},
                {"url": "https://epieos.com/?q=$email&t=email", "tags": ["Google", "Name"]},
                {"url": "https://thatsthem.com/email/$email", "tags": ["Google", "Name"]},
                {"url": "https://google.com/search?q=%22$email%22", "tags": ["Google", "Name"]},
            ]
            urls = [{"url": url["url"].replace('$email', user_input), "tags": url["tags"]} for url in email_urls]
        elif self.current_option == "IP Address":
            ip_urls = [
                {"url": "https://iknowwhatyoudownload.com/en/peer/?ip=$ip", "tags": ["IP", "ip address"]},
            ]
            urls = [{"url": url["url"].replace('$ip', user_input), "tags": url["tags"]} for url in ip_urls]
        elif self.current_option == "Phone Number":
            phone_urls = [
                {"url": "https://www.phonevalidator.com/", "tags": ["phone", "number"]},
                {"url": "https://spydialer.com/", "tags": ["phone", "number"]},
            ]
            urls = [{"url": url["url"].replace('$phone', user_input), "tags": url["tags"]} for url in phone_urls]        
        elif self.current_option == "Image":
            image_urls = [
                {"url": "https://www.aperisolve.com/", "tags": ["image", "info"]},
            ]
            urls = [{"url": url["url"].replace('$image', user_input), "tags": url["tags"]} for url in image_urls]  
        for url_info in urls:
            self.unique_tags.update(url_info['tags'])

        # Update the completer's model with new unique tags
        self.completer.setModel(QtCore.QStringListModel(sorted(self.unique_tags)))

        return urls

    def clear_content_layout(self):
        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    def setup_grid_layout(self):
        self.clear_grid_layout()
        url_data = self.generate_urls()
        max_text_length = 30

        for i, data in enumerate(url_data):
            domain = urlparse(data["url"]).netloc
            button_text = domain if len(domain) <= max_text_length else domain[:max_text_length - 3] + "..."
            button = CustomButton(button_text)
            button.setToolTip(data["url"])
            button.clicked.connect(lambda checked, url=data["url"]: self.open_url(url))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # Check if data["tags"] is a list or a string and assign correctly because was bugging
            if isinstance(data["tags"], list):
                button.setProperty("tags", data["tags"])
            else:
                button.setProperty("tags", data["tags"].split())
            self.grid_layout.addWidget(button, i // 4, i % 4)

    def clear_grid_layout(self):
        while self.grid_layout.count():
            layout_item = self.grid_layout.takeAt(0)
            if layout_item.widget():
                widget = layout_item.widget()
                widget.deleteLater()

    def open_url(self, url):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', url))
        elif os.name == 'nt':  # For Windows
            os.startfile(url)
        elif os.name == 'posix':  # For Linux, Unix, etc.
            subprocess.call(('xdg-open', url))

    def finalize_layouts(self):
        # Layout for the size grip
        grip_layout = QHBoxLayout()
        grip_layout.addWidget(self.size_grip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
    
        # Adding the size grip and footer label to the bottom of the central widget's layout
        layout = self.central_widget.layout()
        if layout is not None:
            layout.addLayout(grip_layout)


    def apply_filter(self, text):
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                # get stored tags
                tags = widget.property("tags")
                if any(tag in text.lower() for tag in tags) or text.lower() in widget.text().lower():
                    widget.show()
                else:
                    widget.hide()

def main():
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    main_window = Window()
    modern_window = qtmodern.windows.ModernWindow(main_window)
    modern_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
