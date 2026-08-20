# 🚀 AI Skill Gap Analyzer

### AI-Powered Career Recommendation & Personalized Skill Roadmap Platform

An intelligent web application that analyzes a student's existing technical skills, identifies skill gaps, recommends suitable career paths, and generates a personalized learning roadmap based on their target career.

The system is designed to help students understand:

- Which career best matches their current skills
- What skills are required for a particular career
- Which skills they are missing
- What proficiency level they currently have
- What they should learn next
- How they can track their learning progress

The application provides a complete journey from:

**Current Skills → Skill Gap → Career Recommendation → Target Career → AI Roadmap → Learning Progress**

---

## 🌐 Live Demo

🔗 **Deployed Application:**  
[Open AI Skill Gap Analyzer](YOUR_DEPLOYED_PROJECT_LINK)

> Replace `YOUR_DEPLOYED_PROJECT_LINK` with your actual Streamlit deployment URL.

---

## 🎯 Objectives

The main objectives of the AI Skill Gap Analyzer are:

1. Analyze the user's existing technical skills.
2. Compare user skills with career-specific requirements.
3. Identify missing and weak skills.
4. Consider the user's skill proficiency level.
5. Recommend suitable career roles.
6. Rank careers based on skill compatibility.
7. Provide career-specific skill requirements.
8. Generate personalized learning roadmaps.
9. Track the user's learning progress.
10. Help students make informed career decisions.

---

## ✨ Key Features

### 👤 User Registration & Login

- User registration
- Login authentication
- Session management
- Personalized user account

### 📝 Profile Management

Users can provide:

- Full Name
- College Name
- Department
- Current Year
- CGPA
- Career Domain
- Target Career

### 💻 Skill Management

Users can add their technical skills and specify their proficiency level.

**Proficiency Levels:**

- Beginner
- Intermediate
- Advanced

### 🧠 Skill Gap Analysis

- Compares user skills with career requirements
- Identifies matched skills
- Identifies missing skills
- Calculates skill gaps
- Considers skill proficiency

### 🏆 Career Recommendation & Ranking

- Analyzes multiple career roles
- Calculates career readiness
- Ranks careers based on skill compatibility
- Helps users identify suitable career paths

### 🎯 Target Career Selection

Users can select their preferred career from the available career domains.

### 🗺️ Personalized Learning Roadmap

Generates a learning path based on:

- Current skills
- Skill gaps
- Target career
- Required skills
- Proficiency levels

### 🤖 AI-Powered Roadmap Generation

Uses an AI model to generate personalized learning roadmaps based on the user's career goal and skill gaps.

### ✅ Learning Progress Tracking

Users can track their learning progress and complete roadmap activities.

---

# 🎯 Supported Career Domains

The AI Skill Gap Analyzer supports multiple technology and engineering career domains.

## 🤖 Artificial Intelligence & Machine Learning

- AI Engineer
- Machine Learning Engineer
- Deep Learning Engineer
- Generative AI Engineer
- LLM Engineer
- Computer Vision Engineer
- NLP Engineer

## 📊 Data Science & Analytics

- Data Scientist
- Data Analyst
- Data Engineer
- Business Analyst
- Analytics Engineer
- Big Data Engineer

## 💻 Software Development

- Software Engineer
- Backend Developer
- Frontend Developer
- Full Stack Developer
- Mobile App Developer

## ☁️ Cloud & DevOps

- Cloud Engineer
- Cloud Architect
- DevOps Engineer
- Site Reliability Engineer (SRE)

## 🔐 Cyber Security

- Cyber Security Analyst
- Security Engineer
- Ethical Hacker
- Penetration Tester

## 🗄️ Database

- Database Administrator (DBA)
- Database Developer

## 🤖 IoT & Robotics

- IoT Engineer
- Robotics Engineer
- Embedded Systems Engineer

## 🧪 Testing & Quality Assurance

- QA Engineer
- Automation Test Engineer

## 📋 Management

- Product Manager
- Project Manager
- Technical Program Manager

## 🚀 Emerging Technologies

- MLOps Engineer
- AI Product Manager
- Prompt Engineer
- AI Research Engineer
- Blockchain Developer
- AR/VR Developer

## 🏗️ Civil Engineering

- Structural Engineer
- BIM Engineer
- Construction Engineer
- Transportation Engineer
- Environmental Engineer

## ⚙️ Mechanical Engineering

- Mechanical Design Engineer
- Manufacturing Engineer
- Automotive Engineer
- Thermal Engineer
- CAD Engineer

## 📡 Electronics & Communication Engineering

ECE-related career paths are supported through the career and skill mapping system.

---

# 🧠 Skill Gap Analysis

The Skill Gap Analyzer compares the user's existing skills with the skills required for a selected career.

### Working Process

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



---

# 🗺️ Personalized Learning Roadmap

The AI Skill Gap Analyzer generates a structured learning path based on the user's:

- Current skills
- Skill proficiency
- Missing skills
- Target career
- Required career skills

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
Projects
        ↓
Career Preparation


# 🏗️ System Architecture

```text
User
 ↓
Streamlit Interface
 ↓
Application Logic
 ↓
MySQL Database + AI Model
 ↓
Personalized Result
```



---

# 🛠️ Technology Stack

## Frontend / User Interface

- Streamlit
- HTML
- CSS

## Programming Language

- Python

## Data Processing & Analysis

- Pandas
- NumPy

## Machine Learning

- Scikit-learn

## Database

- MySQL

## AI / Generative AI

- Groq API
- Large Language Model (LLM)

## Authentication & Application Management

- Python Session State
- MySQL-based user authentication

## Development Tools

- Visual Studio Code
- Jupyter Notebook
- MySQL Workbench
- Git
- GitHub

## Deployment

- Streamlit Community Cloud

---

# 🗄️ Database Design

The application uses MySQL as the primary database for storing user information, skills, careers, career-skill mappings, learning roadmaps, and progress.

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


---

# 👩‍💻 Author

### Keerthana

**B.Tech – Artificial Intelligence and Data Science**  
**K.L.N. College of Engineering, Madurai, Tamil Nadu**

🎓 3rd Year Undergraduate

📌 GitHub: [keerthna31ks-web](https://github.com/keerthna31ks-web)

---

⭐ If you find this project useful, consider giving the repository a star!