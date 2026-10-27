# Smart Water Prediction and Rainwater Management System 🌊

An AI-powered water management system that predicts daily water consumption using Machine Learning, analyzes real-time weather data, and provides intelligent recommendations for water conservation and rainwater harvesting.

---

## 🚀 Features

### 1. User Authentication
- Registration and Login with password hashing
- Session management and profile page
- Secure password handling

### 2. Live Dashboard
- Current temperature, humidity, wind speed, pressure, weather condition
- Today's water prediction
- ML Model performance metrics (R² Score, RMSE, MAE)
- Recent prediction history
- Quick navigation cards

### 3. Live Weather Integration
- Real-time weather data via OpenWeatherMap API
- City-based weather search
- Display: Temperature, Humidity, Pressure, Wind Speed, Cloud Cover, Rainfall
- 5-day weather forecast

### 4. Rain Alert System
- Analyzes forecast data for rainfall prediction
- Displays rain alerts with expected date/time
- Provides actionable recommendations:
  - Store rooftop rainwater
  - Clean rainwater harvesting filters
  - Reduce unnecessary irrigation
  - Delay outdoor water usage
- Rainwater harvesting tips

### 5. Machine Learning Prediction
- **Features**: Temperature, Humidity, Rainfall, Family Size
- **Target**: Daily Water Consumption (Liters)
- **Models Evaluated**:
  - Linear Regression
  - Decision Tree Regressor (Best: R² = 0.9994)
  - Random Forest Regressor
- **Auto-selects best model**
- **Metrics**: R² Score, RMSE, MAE

### 6. Smart Recommendations
- Weather-based water-saving tips
- Personalized recommendations based on predicted usage
- General water conservation tips

### 7. Reports & Analytics
- Total predicted water usage
- Average usage statistics
- Prediction history with detailed table
- Weather records count

### 8. Leak Detection
- Analyzes sudden increases in water consumption
- Detects possible water leakage
- Suggests inspection

### 9. Notifications
- Rain alerts
- Conservation recommendations
- System notifications

### 10. Rainwater Coverage
- Daily rainfall coverage in centimeters
- Past-day rainfall availability chart
- Rainfall totals, averages, highest rainfall, and rainy-day summaries
- Uses stored weather history or live forecast data when history is incomplete
- Environmental condition explanations on the water prediction page

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Structure
- **CSS3** - Custom styling with CSS variables
- **Bootstrap 5** - Responsive grid and components
- **JavaScript** - Interactive features
- **Chart.js** - Data visualization (optional)
- **Font Awesome** - Icons

### Backend
- **Python 3.10+**
- **Flask** - Web framework
- **Flask Blueprints** - Modular architecture

### Database
- **SQLite** - Lightweight, portable database

### Machine Learning
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - ML models (LinearRegression, DecisionTreeRegressor, RandomForestRegressor)
- **Joblib** - Model serialization

### APIs
- **OpenWeatherMap Current Weather API**
- **OpenWeatherMap Forecast API**

---

## 📁 Project Structure

```
Watersystemprediction/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration (API keys, secrets)
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
│
├── controllers/                    # Business logic layer
│   ├── auth_controller.py          # Authentication logic
│   ├── dashboard_controller.py     # Dashboard logic
│   ├── prediction_controller.py    # Prediction logic
│   ├── weather_controller.py       # Weather logic
│   ├── report_controller.py        # Report generation logic
│   └── recommendation_controller.py # Recommendation logic
│
├── routes/                         # Flask route definitions
│   ├── auth.py                     # Auth routes
│   ├── dashboard.py                # Dashboard routes
│   ├── prediction.py               # Prediction routes
│   ├── weather.py                  # Weather routes
│   ├── reports.py                  # Reports routes
│   ├── alerts.py                   # Rain alerts routes
│   └── recommendation.py           # Recommendation routes
│
├── services/                       # Service layer
│   ├── weather_service.py          # Weather data service
│   ├── prediction_service.py       # ML prediction service
│   ├── recommendation_service.py   # Recommendation service
│   ├── notification_service.py     # Notification service
│   └── leak_detection.py           # Leak detection service
│
├── models/                         # Database models
│   ├── user.py                     # User model
│   ├── water_usage.py              # Water usage model
│   ├── prediction.py               # Prediction model
│   ├── recommendation.py           # Recommendation model
│   └── weather.py                  # Weather model
│
├── ml_model/                       # Machine Learning
│   ├── train_model.py              # Model training script
│   ├── predict.py                  # CLI prediction script
│   ├── preprocessing.py            # Data preprocessing
│   ├── model_evaluation.py         # Model evaluation
│   ├── model.pkl                   # Trained model
│   ├── scaler.pkl                  # Feature scaler
│   └── model_metrics.csv           # Model metrics
│
├── database/                       # Database
│   ├── db.py                       # Database connection
│   ├── init_db.py                  # Database initialization
│   ├── sqlite.db                   # SQLite database file
│   └── water_db.sql                # Database schema
│
├── dataset/                        # Training data
│   ├── cleaned_dataset.csv         # Cleaned training data
│   └── water_consumption.csv       # Raw water consumption data
│
├── templates/                      # Jinja2 templates
│   ├── layout.html                 # Base layout
│   ├── index.html                  # Landing page
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard.html              # Main dashboard
│   ├── prediction.html             # Prediction page
│   ├── weather.html                # Weather page
│   ├── alerts.html                 # Rain alerts page
│   ├── recommendations.html        # Recommendations page
│   ├── reports.html                # Reports page
│   ├── profile.html                # User profile page
│   └── error.html                  # Error page
│
├── static/                         # Static assets
│   ├── css/
│   │   ├── style.css               # Main stylesheet
│   │   ├── dashboard.css           # Dashboard styles
│   │   ├── login.css               # Login styles
│   │   ├── register.css            # Register styles
│   │   └── profile.css             # Profile styles
│   └── js/
│       ├── app.js                  # Main application JS
│       ├── dashboard.js            # Dashboard JS
│       ├── weather.js              # Weather JS
│       ├── prediction.js           # Prediction JS
│       └── validation.js           # Form validation JS
│
├── weather/                        # Weather module
│   ├── weather_api.py              # OpenWeatherMap API client
│   ├── weather_parser.py           # Weather data parser
│   ├── forecast.py                 # Forecast script
│   ├── rain_alert.py               # Rain alert logic
│   ├── rain_prediction.py          # Rain prediction logic
│   └── notification.py             # Weather notifications
│
├── reports/                        # Report generation
│   ├── generate_report.py          # Report generator
│   ├── generate_monthly_report.py  # Monthly report generator
│   └── analytics_report.py         # Analytics report generator
│
├── utils/                          # Utilities
│   ├── helper.py                   # Helper functions
│   ├── email.py                    # Email utilities
│   ├── charts.py                   # Chart generation
│   └── constants.py                # Constants
│
└── uploads/                        # Uploaded files
    ├── datasets/
    └── profile_images/
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- OpenWeatherMap API key (included in config.py)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Watersystemprediction
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database
```bash
python -c "from database.init_db import init_database; init_database()"
```

### 5. Train the ML Model
```bash
python ml_model/train_model.py
```

### 6. Run the Application
```bash
python app.py
```

### 7. Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📊 ML Model Performance

| Model | R² Score | RMSE | MAE |
|-------|----------|------|-----|
| Linear Regression | 0.9793 | 4.0572 | 3.2193 |
| Decision Tree | **0.9994** | **0.6811** | **0.064** |
| Random Forest | 0.9991 | 0.8456 | 0.0737 |

**Best Model**: Decision Tree Regressor (auto-selected)

---

## 🌐 API Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/` | GET | Landing page |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/logout` | GET | User logout |
| `/profile` | GET | User profile |
| `/dashboard` | GET | Main dashboard |
| `/prediction` | GET, POST | Water usage prediction |
| `/weather` | GET | Live weather data |
| `/alerts` | GET | Rain alerts |
| `/recommendations` | GET | Water-saving recommendations |
| `/reports` | GET | Reports and analytics |

---

## 🎯 Use Cases

- **Households**: Predict daily water consumption and reduce wastage
- **Apartments**: Monitor community water usage and detect leaks
- **Industries**: Optimize water usage and plan conservation
- **Educational Institutions**: Track water consumption across campuses
- **Hospitals**: Ensure adequate water supply and detect anomalies
- **Hotels**: Manage water resources efficiently
- **Government**: Monitor city-wide water consumption patterns
- **Smart Cities**: Integrate with IoT sensors for real-time monitoring

---

## 🧪 Testing

```bash
# Test the Flask application
python -c "
import requests
base = 'http://127.0.0.1:5000'
s = requests.Session()

# Test registration
r = s.post(base + '/register', data={
    'fullname': 'Test User',
    'email': 'test@example.com',
    'password': 'test123',
    'confirm_password': 'test123'
}, allow_redirects=True)
print('Registration:', r.status_code)

# Test login
r = s.post(base + '/login', data={
    'email': 'test@example.com',
    'password': 'test123'
}, allow_redirects=True)
print('Login:', r.status_code, r.url)

# Test prediction
r = s.post(base + '/prediction', data={
    'temperature': 32,
    'humidity': 65,
    'rainfall': 0,
    'family_size': 4
}, allow_redirects=True)
print('Prediction:', r.status_code, 'Success:', 'Liters' in r.text)
"
```

---

## 🔒 Security

- Passwords hashed using Werkzeug
- Session-based authentication
- SQL injection prevention via parameterized queries
- Input validation and sanitization
- Error handling for all API calls

---

## 🎨 Design

- **Theme**: Dark mode with blue, white, and green accents
- **Responsive**: Mobile-first design with Bootstrap 5
- **Typography**: Inter + Space Grotesk fonts
- **Icons**: Bootstrap Icons
- **Animations**: Smooth transitions and hover effects

---

## 📝 License

This project is developed for educational and demonstration purposes.

---

## 👨‍💻 Author

Smart Water Prediction System - An AI-powered solution for water conservation and management.

---

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Scikit-learn for machine learning algorithms
- Flask community for the web framework
- Bootstrap team for the UI framework