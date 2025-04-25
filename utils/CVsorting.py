import re
from typing import List, Dict
import PyPDF2

# Configuration
MAX_CVS = 10

def extract_section(text: str, section_names: List[str]) -> str:
    for name in section_names:
        pattern = re.compile(
            rf'{name}[^:\n]*[:]?\s*([\s\S]*?)(?=\n{{2,}}|\n[A-Z][a-zA-Z]+:|$)',
            re.IGNORECASE
        )
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return None

def process_skill_list(section_text: str) -> List[str]:
    if not section_text:
        return []

    cleaned = re.sub(r'[\n•\-]+', ',', section_text)
    tokens = [t.strip().lower() for t in re.split(r'[,+]', cleaned) if t.strip()]

    normalization_map = {
        'js': 'javascript', 'ts': 'typescript', 'ts.': 'typescript',
        'node': 'node.js', 'nodejs': 'node.js',
        'c++ programming': 'c++', 'c programming': 'c',
        'next js': 'next.js', 'expressjs': 'express', 'express.js': 'express',
        'py': 'python', 'mongo': 'mongodb',
    }

    normalized_skills = []
    for token in tokens:
        normalized = normalization_map.get(token, token)
        normalized_skills.append(normalized)

    return normalized_skills


def extract_skills(text: str) -> List[str]:
    section = extract_section(text, [
        'skills', 'technical skills', 
        'technologies', 'skills & expertise'
    ])
    return process_skill_list(section) if section else []

def pdf_to_text(pdf_path: str) -> str:
    """Extract text from PDF file"""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return ' '.join(page.extract_text() or '' for page in reader.pages)

def score_cvs(cv_paths: List[str], required_skills: str) -> List[Dict]:
    if len(cv_paths) > MAX_CVS:
        print(f"Warning: Only processing first {MAX_CVS} CVs")
        cv_paths = cv_paths[:MAX_CVS]
    
    required = [s.strip().lower() for s in required_skills.split(',') if s.strip()]

    results = []
    
    for path in cv_paths:
        try:
            text = pdf_to_text(path)
            cv_skills = [s.lower() for s in extract_skills(text)]
            
            matches = [s for s in required if s in cv_skills]
            score = len(matches)
            
            results.append({
                'file': path,
                'score': score,
                'matched': matches,
                'match_percent': int((score / len(required)) * 100) if required else 0
            })
            
        except Exception as e:
            print(f"Skipping {path} - Error: {str(e)}")
            results.append({
                'file': path,
                'score': 0,
                'matched': [],
                'match_percent': 0
            })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

if __name__ == "__main__":
    cvs = ["hasnat.pdf"]  
    skills_needed = "Python, AWS, JavaScript, React, Node.js, TypeScript, GCP, Docker, Kubernetes"
    
    ranked_cvs = score_cvs(cvs, skills_needed)
    
    print(f"\nCV Ranking based on: {skills_needed}")
    print("=" * 50)
    for i, cv in enumerate(ranked_cvs, 1):
        print(f"{i}. {cv['file']}")
        print(f"   Score: {cv['score']}/{len(skills_needed.split(','))} ({cv['match_percent']}%)")
        print(f"   Matches: {', '.join(cv['matched'])}\n")