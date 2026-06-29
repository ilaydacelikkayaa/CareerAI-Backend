import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types
import json

app = FastAPI(title="CareerAI API")

mock_jobs = [
    {
      "id": "job_001",
      "title": "iOS Developer Intern",
      "company": "TechNova",
      "location": "Istanbul, Türkiye",
      "category": "Mobile Development",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "3 Months",
      "salary": "15.000₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-05-10",
      "deadline": "2026-06-01",
      "description": "TechNova is looking for an iOS Developer Intern who is passionate about building scalable and modern mobile applications. Interns will work closely with senior iOS engineers and product designers.",
      "requirements": [
        "Basic knowledge of Swift",
        "Understanding of UIKit or SwiftUI",
        "Knowledge of MVC or MVVM architecture",
        "Familiarity with REST APIs",
        "Git & GitHub experience",
        "Strong problem-solving skills",
        "Computer Engineering or related department student"
      ],
      "responsibilities": [
        "Develop and maintain iOS features",
        "Fix bugs and optimize performance",
        "Participate in code reviews",
        "Work with backend APIs",
        "Write clean and maintainable code"
      ],
      "benefits": [
        "Hybrid working environment",
        "Mentorship from senior developers",
        "Real-world startup experience",
        "Flexible working hours",
        "Certificate after internship"
      ],
      "skills": [
        "Swift",
        "UIKit",
        "Firebase",
        "REST API",
        "Git"
      ]
    },
    {
      "id": "job_002",
      "title": "Backend Developer Intern",
      "company": "CloudByte",
      "location": "Ankara, Türkiye",
      "category": "Backend Development",
      "workType": "Remote",
      "employmentType": "Internship",
      "duration": "6 Months",
      "salary": "18.000₺ / month",
      "experienceLevel": "Entry Level",
      "postedDate": "2026-05-09",
      "deadline": "2026-06-04",
      "description": "Join CloudByte's backend engineering team and build scalable APIs used by thousands of users.",
      "requirements": [
        "Knowledge of Node.js or Python",
        "Understanding RESTful APIs",
        "Basic database knowledge",
        "Understanding authentication systems",
        "Git experience"
      ],
      "responsibilities": [
        "Develop backend services",
        "Database integration",
        "Write API endpoints",
        "Test backend systems"
      ],
      "benefits": [
        "Fully remote",
        "Monthly tech talks",
        "Internship certificate",
        "Performance bonus"
      ],
      "skills": [
        "Node.js",
        "MongoDB",
        "Express",
        "JWT",
        "Docker"
      ]
    },
    {
      "id": "job_003",
      "title": "Frontend Developer Intern",
      "company": "PixelSoft",
      "location": "Izmir, Türkiye",
      "category": "Frontend Development",
      "workType": "On-site",
      "employmentType": "Internship",
      "duration": "4 Months",
      "salary": "13.500₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-05-08",
      "deadline": "2026-05-28",
      "description": "PixelSoft is searching for creative frontend interns interested in modern UI development.",
      "requirements": [
        "HTML, CSS, JavaScript knowledge",
        "React basics",
        "Responsive design understanding",
        "Figma familiarity"
      ],
      "responsibilities": [
        "Develop responsive interfaces",
        "Implement UI designs",
        "Optimize web performance"
      ],
      "benefits": [
        "Modern office",
        "Free lunch",
        "Mentorship"
      ],
      "skills": [
        "React",
        "JavaScript",
        "TailwindCSS",
        "Figma"
      ]
    },
    {
      "id": "job_004",
      "title": "Machine Learning Intern",
      "company": "AI Labs",
      "location": "Istanbul, Türkiye",
      "category": "Artificial Intelligence",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "5 Months",
      "salary": "22.000₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-05-07",
      "deadline": "2026-06-05",
      "description": "AI Labs develops AI-powered products and is looking for ML interns to support model development.",
      "requirements": [
        "Python knowledge",
        "Numpy & Pandas familiarity",
        "Basic machine learning understanding",
        "Data preprocessing experience"
      ],
      "responsibilities": [
        "Train ML models",
        "Analyze datasets",
        "Improve model accuracy"
      ],
      "benefits": [
        "AI workshops",
        "Mentorship",
        "Research opportunities"
      ],
      "skills": [
        "Python",
        "TensorFlow",
        "Pandas",
        "Scikit-learn"
      ]
    },
    {
      "id": "job_005",
      "title": "Cyber Security Intern",
      "company": "SecureNet",
      "location": "Bursa, Türkiye",
      "category": "Cyber Security",
      "workType": "On-site",
      "employmentType": "Internship",
      "duration": "2 Months",
      "salary": "17.000₺ / month",
      "experienceLevel": "Entry Level",
      "postedDate": "2026-05-05",
      "deadline": "2026-05-30",
      "description": "SecureNet is seeking cybersecurity interns interested in ethical hacking and security analysis.",
      "requirements": [
        "Networking basics",
        "Linux familiarity",
        "Security fundamentals",
        "Problem-solving skills"
      ],
      "responsibilities": [
        "Monitor security systems",
        "Assist penetration testing",
        "Prepare security reports"
      ],
      "benefits": [
        "Hands-on security labs",
        "Certificate",
        "Career mentorship"
      ],
      "skills": [
        "Linux",
        "Wireshark",
        "Cyber Security",
        "Networking"
      ]
    },
    {
      "id": "job_006",
      "title": "DevOps Engineer Intern",
      "company": "DeployHub",
      "location": "Kocaeli, Türkiye",
      "category": "DevOps",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "6 Months",
      "salary": "20.000₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-05-04",
      "deadline": "2026-06-02",
      "description": "DeployHub is looking for DevOps interns to automate deployment pipelines and cloud systems.",
      "requirements": [
        "Linux command line knowledge",
        "Basic Docker understanding",
        "CI/CD interest",
        "Git usage"
      ],
      "responsibilities": [
        "Support deployment pipelines",
        "Maintain cloud infrastructure",
        "Monitor application systems"
      ],
      "benefits": [
        "Cloud certifications",
        "Remote flexibility",
        "Technical mentorship"
      ],
      "skills": [
        "Docker",
        "GitHub Actions",
        "AWS",
        "Linux"
      ]
    },
    {
      "id": "job_007",
      "title": "UI/UX Designer Intern",
      "company": "CreativePixel",
      "location": "Antalya, Türkiye",
      "category": "Design",
      "workType": "Remote",
      "employmentType": "Internship",
      "duration": "3 Months",
      "salary": "12.500₺ / month",
      "experienceLevel": "Entry Level",
      "postedDate": "2026-05-04",
      "deadline": "2026-05-24",
      "description": "Design modern mobile and web experiences together with our creative design team.",
      "requirements": [
        "Figma experience",
        "UI design understanding",
        "Creativity",
        "Portfolio preferred"
      ],
      "responsibilities": [
        "Create UI screens",
        "Design wireframes",
        "Improve user experience"
      ],
      "benefits": [
        "Flexible working hours",
        "Remote work",
        "Portfolio support"
      ],
      "skills": [
        "Figma",
        "UI Design",
        "Wireframing"
      ]
    },
    {
      "id": "job_008",
      "title": "QA Tester Intern",
      "company": "BugHunter",
      "location": "Istanbul, Türkiye",
      "category": "Testing",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "4 Months",
      "salary": "14.000₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-05-03",
      "deadline": "2026-05-27",
      "description": "BugHunter seeks QA interns passionate about software quality and testing automation.",
      "requirements": [
        "Attention to detail",
        "Basic software testing knowledge",
        "Analytical thinking"
      ],
      "responsibilities": [
        "Write test cases",
        "Perform UI testing",
        "Report software bugs"
      ],
      "benefits": [
        "Testing workshops",
        "Mentorship",
        "Hybrid model"
      ],
      "skills": [
        "XCTest",
        "Postman",
        "Manual Testing"
      ]
    },
    {
      "id": "job_009",
      "title": "Data Analyst Intern",
      "company": "DataMind",
      "location": "Eskisehir, Türkiye",
      "category": "Data Science",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "5 Months",
      "salary": "16.500₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-05-02",
      "deadline": "2026-05-26",
      "description": "Analyze real-world datasets and generate actionable business insights.",
      "requirements": [
        "Excel knowledge",
        "Python basics",
        "Data visualization understanding"
      ],
      "responsibilities": [
        "Analyze datasets",
        "Build dashboards",
        "Prepare reports"
      ],
      "benefits": [
        "Flexible schedule",
        "Data workshops"
      ],
      "skills": [
        "Python",
        "Pandas",
        "Matplotlib",
        "SQL"
      ]
    },
    {
      "id": "job_010",
      "title": "Game Developer Intern",
      "company": "PlayForge",
      "location": "Izmir, Türkiye",
      "category": "Game Development",
      "workType": "On-site",
      "employmentType": "Internship",
      "duration": "3 Months",
      "salary": "15.500₺ / month",
      "experienceLevel": "Entry Level",
      "postedDate": "2026-05-02",
      "deadline": "2026-05-29",
      "description": "Create engaging mobile games and learn professional game development workflows.",
      "requirements": [
        "Unity or Unreal basics",
        "C# knowledge",
        "Passion for games"
      ],
      "responsibilities": [
        "Develop gameplay mechanics",
        "Fix bugs",
        "Optimize game performance"
      ],
      "benefits": [
        "Game jams",
        "Mentorship",
        "Startup culture"
      ],
      "skills": [
        "Unity",
        "C#",
        "Game Design"
      ]
    },
    {
      "id": "job_011",
      "title": "Cloud Engineer Intern",
      "company": "SkyCloud",
      "location": "Ankara, Türkiye",
      "category": "Cloud Computing",
      "workType": "Remote",
      "employmentType": "Internship",
      "duration": "6 Months",
      "salary": "21.000₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-05-01",
      "deadline": "2026-05-31",
      "description": "Support cloud infrastructure and deployment automation projects.",
      "requirements": [
        "Basic AWS or Azure knowledge",
        "Linux familiarity",
        "Networking basics"
      ],
      "responsibilities": [
        "Monitor cloud services",
        "Deploy applications",
        "Assist infrastructure management"
      ],
      "benefits": [
        "Cloud certifications",
        "Remote work"
      ],
      "skills": [
        "AWS",
        "Linux",
        "Docker"
      ]
    },
    {
      "id": "job_012",
      "title": "Blockchain Developer Intern",
      "company": "ChainBase",
      "location": "Istanbul, Türkiye",
      "category": "Blockchain",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "4 Months",
      "salary": "24.000₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-04-30",
      "deadline": "2026-05-25",
      "description": "Develop decentralized applications and smart contracts with blockchain engineers.",
      "requirements": [
        "Solidity basics",
        "Blockchain understanding",
        "JavaScript familiarity"
      ],
      "responsibilities": [
        "Write smart contracts",
        "Test blockchain systems",
        "Research Web3 technologies"
      ],
      "benefits": [
        "Web3 mentorship",
        "Conference access"
      ],
      "skills": [
        "Solidity",
        "Ethereum",
        "Web3"
      ]
    },
    {
      "id": "job_013",
      "title": "AR/VR Developer Intern",
      "company": "VisionXR",
      "location": "Antalya, Türkiye",
      "category": "AR/VR",
      "workType": "On-site",
      "employmentType": "Internship",
      "duration": "5 Months",
      "salary": "19.000₺ / month",
      "experienceLevel": "Entry Level",
      "postedDate": "2026-04-29",
      "deadline": "2026-05-27",
      "description": "Build immersive AR/VR experiences for next-generation applications.",
      "requirements": [
        "Unity basics",
        "3D math understanding",
        "Creative thinking"
      ],
      "responsibilities": [
        "Develop AR interactions",
        "Optimize 3D experiences"
      ],
      "benefits": [
        "XR lab access",
        "Hardware support"
      ],
      "skills": [
        "Unity",
        "ARKit",
        "3D"
      ]
    },
    {
      "id": "job_014",
      "title": "Embedded Systems Intern",
      "company": "MicroTech",
      "location": "Konya, Türkiye",
      "category": "Embedded Systems",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "3 Months",
      "salary": "18.500₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-04-28",
      "deadline": "2026-05-22",
      "description": "Work on embedded software and IoT hardware systems.",
      "requirements": [
        "C programming basics",
        "Microcontroller understanding",
        "Electronics fundamentals"
      ],
      "responsibilities": [
        "Write firmware",
        "Test hardware modules"
      ],
      "benefits": [
        "Hardware lab",
        "Mentorship"
      ],
      "skills": [
        "C",
        "Arduino",
        "Embedded C"
      ]
    },
    {
      "id": "job_015",
      "title": "Product Manager Intern",
      "company": "LaunchUp",
      "location": "Izmir, Türkiye",
      "category": "Product Management",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "4 Months",
      "salary": "17.500₺ / month",
      "experienceLevel": "Entry Level",
      "postedDate": "2026-04-27",
      "deadline": "2026-05-26",
      "description": "Assist product teams in roadmap planning and feature analysis.",
      "requirements": [
        "Communication skills",
        "Analytical thinking",
        "Product interest"
      ],
      "responsibilities": [
        "Prepare product reports",
        "Analyze user feedback"
      ],
      "benefits": [
        "Mentorship",
        "Networking opportunities"
      ],
      "skills": [
        "Product Management",
        "Analytics",
        "Agile"
      ]
    },
    {
      "id": "job_016",
      "title": "NLP Engineer Intern",
      "company": "LinguaAI",
      "location": "Istanbul, Türkiye",
      "category": "Natural Language Processing",
      "workType": "Remote",
      "employmentType": "Internship",
      "duration": "5 Months",
      "salary": "23.000₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-04-26",
      "deadline": "2026-05-24",
      "description": "Develop language models and text-processing pipelines.",
      "requirements": [
        "Python knowledge",
        "NLP fundamentals",
        "Machine learning basics"
      ],
      "responsibilities": [
        "Train NLP models",
        "Analyze text datasets"
      ],
      "benefits": [
        "Research opportunities",
        "Remote flexibility"
      ],
      "skills": [
        "Python",
        "Transformers",
        "NLP"
      ]
    },
    {
      "id": "job_017",
      "title": "Big Data Intern",
      "company": "DataStorm",
      "location": "Eskisehir, Türkiye",
      "category": "Big Data",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "6 Months",
      "salary": "20.500₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-04-25",
      "deadline": "2026-05-30",
      "description": "Process large-scale datasets and support data engineering operations.",
      "requirements": [
        "SQL basics",
        "Python understanding",
        "Analytical skills"
      ],
      "responsibilities": [
        "Data processing",
        "Pipeline monitoring"
      ],
      "benefits": [
        "Data workshops",
        "Flexible work model"
      ],
      "skills": [
        "Hadoop",
        "Spark",
        "SQL"
      ]
    },
    {
      "id": "job_018",
      "title": "FinTech Intern",
      "company": "PayFlow",
      "location": "Istanbul, Türkiye",
      "category": "Finance Technology",
      "workType": "Hybrid",
      "employmentType": "Internship",
      "duration": "4 Months",
      "salary": "22.500₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-04-24",
      "deadline": "2026-05-21",
      "description": "Work on digital payment systems and financial APIs.",
      "requirements": [
        "Backend basics",
        "Interest in finance",
        "API understanding"
      ],
      "responsibilities": [
        "Support payment integrations",
        "Monitor fintech systems"
      ],
      "benefits": [
        "Fintech mentorship",
        "Hybrid work"
      ],
      "skills": [
        "FinTech",
        "REST API",
        "Node.js"
      ]
    },
    {
      "id": "job_019",
      "title": "Computer Vision Intern",
      "company": "VisionTech",
      "location": "Ankara, Türkiye",
      "category": "Computer Vision",
      "workType": "On-site",
      "employmentType": "Internship",
      "duration": "5 Months",
      "salary": "24.500₺ / month",
      "experienceLevel": "Junior",
      "postedDate": "2026-04-23",
      "deadline": "2026-05-25",
      "description": "Develop image processing and computer vision systems for AI products.",
      "requirements": [
        "Python basics",
        "OpenCV familiarity",
        "Machine learning understanding"
      ],
      "responsibilities": [
        "Image processing",
        "Dataset preparation"
      ],
      "benefits": [
        "AI mentorship",
        "Research projects"
      ],
      "skills": [
        "OpenCV",
        "Python",
        "Computer Vision"
      ]
    },
    {
      "id": "job_020",
      "title": "Startup Operations Intern",
      "company": "VentureX",
      "location": "Istanbul, Türkiye",
      "category": "Startup",
      "workType": "Remote",
      "employmentType": "Internship",
      "duration": "3 Months",
      "salary": "14.500₺ / month",
      "experienceLevel": "Entry Level",
      "postedDate": "2026-04-22",
      "deadline": "2026-05-20",
      "description": "Support startup operations, community management, and growth strategies.",
      "requirements": [
        "Communication skills",
        "Organizational skills",
        "Startup interest"
      ],
      "responsibilities": [
        "Support daily operations",
        "Community engagement",
        "Prepare reports"
      ],
      "benefits": [
        "Startup culture",
        "Remote flexibility"
      ],
      "skills": [
        "Operations",
        "Communication",
        "Growth"
      ]
    }
]

class CVRequest(BaseModel):
    userCV: str

class SkillMatch(BaseModel):
    skillName: str
    isMatched: bool

class AIJobMatch(BaseModel):
    id: str  
    matchScore: int
    strengths: List[str]
    gapDescription: str
    gapSteps: List[str]
    strategy: str
    skillsEvaluation: List[SkillMatch]

class AIAnalysisResponse(BaseModel):
    matches: List[AIJobMatch]

class JobApplyRequest(BaseModel):
    job_id: str
applied_jobs_database = set()


@app.post("/api/apply")
def apply_to_job(request_data: JobApplyRequest):
    job_id = request_data.job_id
    
    applied_jobs_database.add(job_id)
    
    print("\n" + "="*40)
    print(f" CANLI BAŞVURU GELDİ!")
    print(f" Başvurulan İlan ID: {job_id}")
    print(f"Güncel Başvuru Havuzumuz: {list(applied_jobs_database)}")
    print("="*40 + "\n")
    
    return {
        "status": "success",
        "message": f"Successfully applied to job {job_id}"
    }
@app.get("/api/applied-jobs")
def get_applied_jobs():
    applied_details = []
    
    for job_id in applied_jobs_database:
        for job in mock_jobs:
            if job["id"] == job_id:
                applied_details.append(job)
                break 
                
    return applied_details

@app.get("/api/jobs")
def get_jobs():
    return mock_jobs

@app.get("/api/jobs/{job_id}")
def get_job_detail(job_id: str):
    for job in mock_jobs:
        if job["id"] == job_id:
            return job
    return {"error": "İlan bulunamadı"}

@app.post("/api/analyze", response_model=AIAnalysisResponse)
def analyze_cv(request: CVRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt = f"""
    You are an expert AI Career Assistant. Your job is to analyze the provided user's CV text and compare it against the JSON list of available internship jobs.
    For each job, calculate a realistic matching score (0-100) and provide structured feedback.
    
    --- START OF USER CV ---
    {request.userCV}
    --- END OF USER CV ---
    
    --- START OF AVAILABLE JOBS ---
    {mock_jobs}
    --- END OF AVAILABLE JOBS ---
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AIAnalysisResponse,
            ),
        )
        return json.loads(response.text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini Hatası: {str(e)}")