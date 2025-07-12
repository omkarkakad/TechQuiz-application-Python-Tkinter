# 🧠 Technical Quiz Application using Python Tkinter

A fully interactive and category-based **Quiz Application** built with **Python-Tkinter**, supporting real-time scoring, light/dark theming, CSV result saving, and a 60-second countdown timer.

---

## 🎯 Features

- 📂 **Category & Difficulty Selection**
  - Choose from multiple categories and levels (Easy, Medium, Hard) from JSON

- ⏳ **60-Second Countdown Timer**
  - Quiz ends when timer runs out

- 🌙 **Theme Toggle**
  - Switch between light and dark UI

- ✅ **Multiple Navigation Options**
  - Next, Previous, Submit, Restart controls with real-time validation

- 📋 **Result Display & CSV Logging**
  - Name, Category, Difficulty, Score stored in `techquiz_results.csv`

- 🔁 **Question Randomization**
  - Questions get shuffled on each start

- 🔐 **Safe Exit Handling**
  - Prompts confirmation before closing mid-quiz

---

## 💻 Tech Stack

- Python 3
- Tkinter (GUI)
- JSON (for questions)
- CSV (for saving results)
- OS, Time, Threading, Random (Python modules)

---

## 📁 Files

- `main.py` — Main quiz application
- `quiz_questions_complete.json` — Questions data file
- `techquiz_results.csv` — Result storage (auto-generated)

---

## 🚀 How to Run

1. Clone the repo  
2. Make sure `quiz_questions_complete.json` is present  
3. Run:

```bash
python main.py
