# OSINT-MasterTool 🌐

![GitHub release (latest by date)](https://img.shields.io/github/v/release/pentestfunctions/OSINT-MasterTool)
![GitHub last commit](https://img.shields.io/github/last-commit/pentestfunctions/OSINT-MasterTool)
![GitHub issues](https://img.shields.io/github/issues-raw/pentestfunctions/OSINT-MasterTool)
![GitHub pull requests](https://img.shields.io/github/issues-pr/pentestfunctions/OSINT-MasterTool)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-blue)

🔍 **OSINT-MasterTool** is an innovative and user-friendly desktop application designed for Open Source Intelligence (OSINT) gathering. It streamlines the process of aggregating information from various online resources, tailored specifically for queries like email addresses, usernames, domains, IP addresses, and phone numbers. Built with PyQt5 and qtmodern, it offers a modern and sleek interface with multiple theme customization options.

## 🌟 Features

- 📊 Search across multiple platforms using different query types.
- 🌐 Access to a wide range of OSINT resources with easy navigation.
- 🎨 Theme customization for a personalized user experience.
- 🚀 Dynamic filters and quick URL access for efficient information gathering.

## 🛠 Installation

- For Windows userse you can download a release here:
https://github.com/pentestfunctions/OSINT-MasterTool/releases/tag/v0.1

### Prerequisites

- Python 3.x
- PyQt5
- qtmodern

### Building the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/pentestfunctions/OSINT-MasterTool.git
   ```
2. Navigate to the project directory:
   ```bash
   cd OSINT-MasterTool
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Build the application for Windows:
   ```bash
   pyinstaller --onefile --noconsole OSINT.py
   ```

The executable will be available in the dist folder.
🚀 Usage
Launch the application from the executable created in the dist folder.
Select the query type from the dropdown menu (Email, Username, Domain, etc.).
Enter the search query in the provided input field.
Explore the generated links and use filters for refined search results.
🤝 Contributing
Contributions are welcome! Feel free to open pull requests or submit issues for bug reports and feature requests.

📸 Example gif
<p align="center">
  <img src="./static/WorkingOSINT.gif" alt="OSINT-MasterTool in action">
</p>
```
