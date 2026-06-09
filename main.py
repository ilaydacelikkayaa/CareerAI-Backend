from fastapi import FastAPI

# 1. FastAPI sistemimizi başlatıyoruz
app = FastAPI(title="CareerAI API")

# 2. İlan listemiz (İleride veri tabanından çekeceğimiz Mock Data)
mock_jobs = [
    {
        "id": "ios-dev-intern",
        "title": "iOS Developer Intern",
        "company": "Phinia",
        "description": "UIKit ve Swift ile mobil arayüz geliştirme stajı.",
        "requirements": ["Swift", "UIKit", "SnapKit"],
        "responsibilities": ["Ekran tasarlamak"],
        "benefits": ["Mentorluk desteği"],
        "skills": ["Swift"],
        "salary": "Asgari Ücret",
        "location": "Isparta"
    }
]

# 3. İnternet kapımız (Endpoint)
@app.get("/api/jobs")
def get_jobs():
    return mock_jobs