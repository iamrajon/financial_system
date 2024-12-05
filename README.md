# FinancialSystemAPI

A robust and scalable REST API for managing income, expenses, loans, and generating financial reports. This API includes features like user authentication, CRUD operations, filtering, sorting, and detailed Swagger documentation for easy integration.

---

## **Features**
- **User Authentication**: Secure JWT-based user login and registration.
- **Income Management**: Add, view, update, and delete income records.
- **Expense Management**: Add, view, update, and delete expense records.
- **Loan Management**: Track loans with business logic for calculating monthly installments and remaining balance.
- **Financial Reports**: Generate detailed reports, including trends and summary data, with optional filtering by date range.
- **Swagger UI Documentation**: Interactive API documentation for seamless integration.

---

## **Technologies Used**
- **Backend**: Django, Django Rest Framework (DRF)
- **Authentication**: JWT (SimpleJWT)
- **Database**: SQLite (Development), can be extended to PostgreSQL
- **Caching**: Redis (optional, with fallback to local memory cache)
- **Documentation**: drf-spectacular (Swagger/OpenAPI)

---

## **Installation Guide**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/FinanceManagerAPI.git
cd FinanceManagerAPI
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate # for mac
venv\Scripts\activate # for windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

### 6. Access the Swagger UI
```bash
Visit the Swagger UI at http://127.0.0.1:8000/api/schema/swagger-ui/
```

### 6. For Redis Cache Implementation
```bash
1. Install Docker Destkop 
2. Run this command on terminal: docker-compose up -d 
3. Verify Redis is running: redis-cli -h 127.0.0.1 -p 6380 ping
```

---

## **Contributing**

Contributions are welcome! If you'd like to add new features, fix bugs, or improve documentation, please fork this repository and submit a pull request. For major changes, feel free to open an issue first to discuss your ideas.

---

## **Contact Information**

If you have any questions, suggestions, or feedback, feel free to reach out:

- **Email**: vengrajon84@gmail.com  
- **GitHub**: [@iamrajon](https://github.com/iamrajon)  
- **LinkedIn**: [Rajan Chaudhary](https://www.linkedin.com/in/rajanc1209/)  

We appreciate your interest in the **FinanceManagerAPI** project. Happy coding! 🚀