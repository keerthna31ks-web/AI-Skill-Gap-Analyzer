# 🚀 AI Skill Gap Analyzer

### AI-Powered Career Recommendation & Personalized Skill Roadmap Platform

An intelligent web application that analyzes a student's existing technical skills, identifies skill gaps, recommends suitable career paths, and generates a personalized learning roadmap based on their target career.

The platform helps students understand:

* Which career best matches their current skills
* What skills are required for a particular career
* Which skills they are missing
* What proficiency level they currently have
* What they should learn next
* How to track their learning progress

**Current Skills → Skill Gap → Career Recommendation → Target Career → AI Roadmap → Learning Progress**

---

## 🌐 Live Demo

🔗 **Deployed Application:**
https://ai-skill-gap-analyzer-knavamhk39ywahrin4bavx.streamlit.app/

🔗 **GitHub Repository:**
https://github.com/keerthna31ks-web/ai-skill-gap-analyzer

---

## 🎯 Objectives

1. Analyze the user's existing technical skills.
2. Compare user skills with career-specific requirements.
3. Identify missing and weak skills.
4. Consider the user's skill proficiency level.
5. Recommend suitable career roles.
6. Rank careers based on skill compatibility.
7. Provide career-specific skill requirements.
8. Generate personalized learning roadmaps.
9. Track learning progress.
10. Help students make informed career decisions.

---

## ✨ Key Features

### 👤 User Registration & Login

* User registration
* Secure password hashing
* Login authentication
* Session management
* Personalized user account

### 📝 Profile Management

Users can provide:

* Full Name
* College Name
* Department
* Current Year
* CGPA
* Career Domain
* Target Career

### 💻 Skill Management

Users can add technical or domain-specific skills and specify their proficiency level.

**Proficiency Levels:**

* Beginner
* Intermediate
* Advanced

### 🧠 Skill Gap Analysis

The system compares the user's existing skills with the skills required for a selected career.

It identifies:

* Matched skills
* Missing skills
* Weak or partial skills
* Required proficiency
* Skill gaps
* Career readiness

### 🏆 Career Recommendation & Ranking

The system analyzes the user's skills against multiple career roles and ranks careers according to skill compatibility and readiness.

Example:

| Career                    | Readiness |
| ------------------------- | --------: |
| Data Analyst              |       82% |
| Data Scientist            |       74% |
| Data Engineer             |       68% |
| Machine Learning Engineer |       51% |

### 🎯 Target Career Selection

Users can select their preferred target career.

The selected career becomes the basis for the personalized learning roadmap.

The target career is explicitly passed to the AI roadmap generator so that the generated roadmap remains career-specific.

### 🗺️ Personalized Learning Roadmap

The roadmap is generated based on:

* Current skills
* Skill proficiency
* Missing skills
* Skill priorities
* Target career
* Required career skills

The roadmap contains progressive learning phases, topics, practice tasks, mini projects, and a final career-specific project.

### 🤖 AI-Powered Roadmap Generation

The project uses the **Groq API** and a large language model to generate personalized learning roadmaps.

The AI considers the user's:

* Current skills
* Partial skills
* Skill gaps
* Learning priorities
* Readiness score
* Target career

The generated response is returned as structured JSON and stored in the database.

### ✅ Learning Progress Tracking

Users can track their progress through roadmap activities and learning tasks.

---

## 🎯 Supported Career Domains

### 🤖 Artificial Intelligence & Machine Learning

* AI Engineer
* Machine Learning Engineer
* Deep Learning Engineer
* Generative AI Engineer
* LLM Engineer
* Computer Vision Engineer
* NLP Engineer

### 📊 Data Science & Analytics

* Data Scientist
* Data Analyst
* Data Engineer
* Business Analyst
* Analytics Engineer
* Big Data Engineer

### 💻 Software Development

* Software Engineer
* Backend Developer
* Frontend Developer
* Full Stack Developer
* Mobile App Developer

### ☁️ Cloud & DevOps

* Cloud Engineer
* Cloud Architect
* DevOps Engineer
* Site Reliability Engineer (SRE)

### 🔐 Cyber Security

* Cyber Security Analyst
* Security Engineer
* Ethical Hacker
* Penetration Tester

### 🗄️ Database

* Database Administrator (DBA)
* Database Developer

### 🤖 IoT & Robotics

* IoT Engineer
* Robotics Engineer
* Embedded Systems Engineer

### 🧪 Testing & Quality Assurance

* QA Engineer
* Automation Test Engineer

### 📋 Management

* Product Manager
* Project Manager
* Technical Program Manager

### 🚀 Emerging Technologies

* MLOps Engineer
* AI Product Manager
* Prompt Engineer
* AI Research Engineer
* Blockchain Developer
* AR/VR Developer

### 🏗️ Civil Engineering

* Structural Engineer
* BIM Engineer
* Construction Engineer
* Transportation Engineer
* Environmental Engineer

### ⚙️ Mechanical Engineering

* Mechanical Design Engineer
* Manufacturing Engineer
* Automotive Engineer
* Thermal Engineer
* CAD Engineer

### 📡 Electronics & Communication Engineering

ECE-related career paths are supported through the career and skill mapping system.

---

## 🧠 Skill Gap Analysis

The Skill Gap Analyzer follows this process:

```text
Required Career Skills
          ↓
Career-Skill Mapping
          ↓
User's Existing Skills
          ↓
Skill & Proficiency Comparison
          ↓
Matched Skills + Missing Skills
          ↓
Skill Gap Calculation
          ↓
Career Readiness
```

The system considers both **skill matching and proficiency levels**, allowing the application to distinguish between users who completely know a skill and users who only have partial proficiency.

---

## 🎯 Target Career Selection

Example:

```text
Career Domain:
Data Science & Analytics

Target Career:
Data Engineer
```

The selected target career determines:

* Required skills
* Missing skills
* Skill priorities
* Learning topics
* Practice tasks
* Projects
* AI-generated roadmap

The AI roadmap generator is designed to preserve the user's selected target career instead of replacing it with another role.

---

## 🗺️ Personalized Learning Roadmap

### Roadmap Structure

```text
Foundation Skills
        ↓
Core Technical Skills
        ↓
Advanced Skills
        ↓
Practice
        ↓
Mini Project
        ↓
Final Career Project
        ↓
Career Preparation
```

The AI-generated roadmap includes:

* Progressive learning phases
* Skills to learn
* Learning topics
* Topic descriptions
* Practice tasks
* Mini project
* Final project
* Skills used in projects
* Expected project outcome

---

## 🤖 AI-Powered Roadmap Generation

The roadmap generation pipeline follows:

```text
User Profile
     +
Current Skills
     +
Skill Gaps
     +
Learning Priorities
     +
Target Career
     ↓
Groq API
     ↓
Structured JSON Roadmap
     ↓
Roadmap Validation
     ↓
MySQL Storage
     ↓
Personalized Learning Roadmap
```

The AI receives a compact representation of the user's skills and career requirements.

The application requests a structured JSON response so that the generated roadmap can be processed and stored programmatically.

The generated roadmap is specifically tied to the user's selected target career.

---

## ✅ Learning Progress Tracking

```text
Learning Activity
        ↓
User Completes Activity
        ↓
Progress Updated
        ↓
Skill Development
        ↓
Improved Career Readiness
```

**Analyze → Learn → Practice → Track → Improve**

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         │                     │
                         │ Registration/Login  │
                         │ Profile             │
                         │ Skills              │
                         │ Dashboard           │
                         │ Skill Gap Analyzer  │
                         │ Career Ranking      │
                         │ AI Roadmap          │
                         │ Progress Tracking   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Application Logic  │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌───────────────────┐          ┌───────────────────┐
          │   Aiven MySQL     │          │     Groq API      │
          │     Database      │          │   AI Roadmap      │
          │                   │          │    Generation     │
          └───────────────────┘          └───────────────────┘
```

---

## 🔄 Application Workflow

```text
Register
   ↓
Login
   ↓
Complete Profile
   ↓
Select Department & Career Domain
   ↓
Select Target Career
   ↓
Add Skills & Proficiency
   ↓
Analyze Skill Gap
   ↓
View Career Recommendations
   ↓
Select Target Career
   ↓
Generate AI Roadmap
   ↓
Learn & Practice
   ↓
Track Progress
```

---

## 🛠️ Technology Stack

### Programming Language

* Python

### Frontend / User Interface

* Streamlit
* HTML
* CSS

### Data Processing & Analysis

* Pandas
* NumPy

### Machine Learning

* Scikit-learn

### Database

* MySQL
* Aiven Cloud MySQL

### AI / Generative AI

* Groq API
* `openai/gpt-oss-120b`
* Structured JSON generation

### Authentication & Security

* bcrypt
* Streamlit Secrets

### Development Tools

* Visual Studio Code
* Jupyter Notebook
* MySQL Workbench
* Git
* GitHub

### Deployment

* Streamlit Community Cloud

---

## 🗄️ Database Design

The production application uses **Aiven Cloud MySQL** to store user accounts, profiles, skills, career mappings, AI-generated roadmaps, and learning progress.

### Main Database Entities

```text
USERS
  │
  ▼
USER_PROFILE
  │
  ├──────────────► USER_SKILLS
  │                     │
  │                     ▼
  │                   SKILLS
  │                     │
  │                     ▼
  │               CAREER_SKILLS
  │                     │
  │                     ▼
  │                  CAREERS
  │
  ▼
AI_ROADMAPS
  │
  ▼
USER_PROGRESS
```

### Main Tables

| Table           | Purpose                                            |
| --------------- | -------------------------------------------------- |
| `users`         | User account and authentication                    |
| `user_profile`  | Profile, department, career domain and target role |
| `skills`        | Available technical and engineering skills         |
| `user_skills`   | User skills and proficiency                        |
| `careers`       | Available career roles                             |
| `career_skills` | Career-to-skill mappings                           |
| `skill_trends`  | Skill trend information                            |
| `ai_roadmaps`   | Generated AI roadmaps                              |
| `user_progress` | Learning progress                                  |

---

## ☁️ Production Database

The deployed application uses **Aiven Cloud MySQL** instead of a local MySQL server.

### Architecture

```text
Local MySQL
     │
     │ Database Export
     ▼
Aiven Cloud MySQL
     │
     │ Secure Connection
     ▼
Streamlit Cloud Application
```

Database credentials are stored securely using **Streamlit Cloud Secrets** and are not committed to the GitHub repository.

---

## 📁 Project Structure

```text
AI_Skill_Gap_Analyzer/
│
├── app.py
│
├── pages/
│   ├── login.py
│   ├── register.py
│   ├── profile.py
│   ├── skills.py
│   ├── dashboard.py
│   ├── skill_gap_analyser.py
│   └── ai_roadmap.py
│
├── models/
│   ├── profile.py
│   └── skill.py
│
├── utils/
│   ├── auth.py
│   ├── ai_roadmp.py
│   ├── roadmap_storage.py
│   └── roadmap_progress.py
│
├── database/
│   └── db.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/keerthna31ks-web/ai-skill-gap-analyzer.git
cd ai-skill-gap-analyzer
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

For local development, configure the required MySQL connection values.

For the deployed application, the connection is configured through Streamlit Cloud Secrets and points to Aiven Cloud MySQL.

Required database configuration:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME
DB_SSL_CA
```

### 5. Configure Groq API

For Streamlit Cloud, add the Groq API key through **Streamlit Secrets**:

```toml
GROQ_API_KEY = "your_api_key"
```

For local development, use an appropriate local secret/environment configuration.

**Never commit API keys, database passwords, or SSL certificates to GitHub.**

### 6. Run the Application

```bash
streamlit run app.py
```

---

## 🔐 Security

Sensitive credentials are not stored directly in the application source code.

The deployed application uses:

* Streamlit Secrets for database credentials
* Streamlit Secrets for the Groq API key
* bcrypt for password hashing
* SSL-secured connection to Aiven MySQL

Sensitive values such as:

```text
DB_PASSWORD
GROQ_API_KEY
DB_SSL_CA
```

should never be committed to GitHub.

---

## 🔮 Future Enhancements

* Resume-based automatic skill extraction
* Job-market trend analysis
* Real-time job recommendations
* Internship recommendations
* Course recommendations
* Advanced career prediction
* Skill demand forecasting
* Automated resume generation
* Interview preparation
* Personalized project recommendations
* Additional engineering career paths
* Job description-based skill gap analysis
* Learning resource personalization

---

## ⚠️ Limitations

* Career recommendations depend on the quality of career-skill mappings.
* AI-generated roadmaps may require user verification.
* Skill proficiency is based on user-provided information.
* Career readiness scores are indicative rather than professional career assessments.
* Some career domains may have limited skill mappings.
* AI-generated content may vary between generations.

---

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test the application.
5. Commit your changes.
6. Push the branch.
7. Create a Pull Request.

---

## 📄 License

This project is currently developed as an academic and portfolio project.

---

## 👩‍💻 Author

### Keerthana

**B.Tech – Artificial Intelligence and Data Science**
**K.L.N. College of Engineering, Madurai, Tamil Nadu**

🎓 3rd Year Undergraduate

🔗 **GitHub:**
https://github.com/keerthna31ks-web

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ star on GitHub.

**AI Skill Gap Analyzer — Analyze → Learn → Practice → Track → Improve**
