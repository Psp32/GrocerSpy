# GrocerSpy

#### 🎥 Video Demo:  https://youtu.be/3QCe6qFqswI

---

## 📦 Project Overview

**GrocerSpy** is a Python-based intelligent grocery price comparison tool that enables users to effortlessly identify the best prices for grocery items across top online platforms such as **Blinkit**, **Swiggy Instamart**, and **JioMart**. The tool is designed with automation, simplicity, and user convenience in mind.

Users can input multiple grocery products during a session, and the application uses browser automation and fuzzy string matching to locate the most relevant product listings and retrieve their prices. At the end of the session, the tool presents all data in a clean, tabular format—highlighting the platform offering the **lowest price** for each product.

GrocerSpy simplifies the otherwise tedious and time-consuming task of manually comparing prices across platforms. With just a few inputs and one command, users can optimize their shopping expenses and make smarter purchasing decisions.

---

## ✨ Key Features

- 🧑‍💻 **Interactive Input Flow**: Enter multiple product names in a single session.
- 🧭 **Automated Price Retrieval**: Uses **Playwright** for headless browser automation.
- 🔍 **Fuzzy String Matching**: Powered by `thefuzz` library for best-match accuracy.
- 📊 **Tabular Summary**: Presents results in a user-friendly table with highlights.
- 🌐 **Cross-platform Compatibility**: Works on Windows, macOS, and Linux.
- 💡 **Smart Decision-Making**: Empowers users to save both time and money.

---

## 📌 How It Works

1. **User Input**: Enter product names interactively (ends with Ctrl+C).
2. **Scraping**: Automated browser fetches product listings from:
   - Blinkit
   - Swiggy Instamart
   - JioMart
3. **Matching & Extraction**: Fuzzy matching ensures the most relevant items are picked and priced.
4. **Output**: Displays a comparison table with the lowest price highlighted.

---

## 🧪 Example Output

| Product         | Blinkit | Swiggy Instamart | Jio Mart |    Best Site     |
|-----------------|---------|------------------|----------|------------------|
| Amul Milk 1L    | ₹55.00  |     ₹56.00       | ₹58.00   | Blinkit (₹55.0)  |
| Rice 200 Gm     | ₹32.00  |     ₹28.50       | ₹27.00   | Jio Mart (₹27.0) |

*The best price per product is automatically detected and shown in the last column.*

---

## ⚙️ Installation & Setup

To get started with **GrocerSpy**, follow these steps:

```bash
# 1. Clone the repository
git clone <repository-url>
cd GrocerSpy

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies manually
pip install playwright pandas thefuzz rich
playwright install

# 4. Run the application
python grocerspy.py
