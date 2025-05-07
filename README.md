# 🍽️ Food Waste Reducer with Recipe Suggestions

A smart Django web application that helps reduce food waste by suggesting recipes based on available ingredients, tracking your kitchen inventory, and sending daily email alerts for items nearing expiry.

---

## 🚀 Overview

This project was built to solve a common real-world problem: **food waste** due to unused or forgotten ingredients. The app provides personalized recipe suggestions, allows users to save favorite recipes, and manages food inventory efficiently — with automatic daily notifications to prevent wastage.

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS(Tailwind), JavaScript (Django Templates)
- **Database:** MySQL
- **Authentication:** Django’s built-in Auth System
- **Email Notifications:** Python’s SMTP
- **Recipe API:** Public Recipe API (such as Spoonacular)

---

## 🌟 Features

### ✅ Ingredient-Based Recipe Suggestions
- Input the ingredients you have at home
- Get recipe suggestions instantly using an external API

### ✅ User Authentication
- Register, log in, and get a personalized experience

### ✅ Save Recipes to Profile
- Save your favorite recipes
- View saved recipes anytime under your profile section

### ✅ Inventory Module 
- Track food items in your kitchen
- Add items with quantity and expiry dates
- View your inventory in an organized list

### ✅ Daily Email Alerts 
- Receive daily emails warning you about food items nearing expiry
- Promotes timely usage and reduces waste

### ✅ Clean & Responsive UI
- Modern layout, accessible from desktop and mobile devices

---

## 📁 Project Structure

```bash
FoodWasteReducer/
├── myapp/           # Authentication and general pages
├── recipe/          # Recipe suggestion logic
├── inventory/       # Inventory management & email alerts
├── templates/       # HTML templates (shared across apps)
├── static/          # CSS, JavaScript, and images
├── manage.py        # Django project entry point
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## ⚙️ How to Run the Project

1. **Clone the Repository**
```bash
git clone https://github.com/parshv09/FoodWasteReducer.git
cd FoodWasteReducer
```
2.Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```
3.Install Required Packages
```bash
pip install -r requirements.txt
```
4.Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
5.Start the Development Server
```bash
python manage.py runserver
```
6.Open in Browser 
```bash
http://127.0.0.1:8000/
```
---
### 👨‍💻 Author
Parshv Athane




