import openai
from typing import List, Dict
import json
from resume_parser import parse_resume
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENIAI_API_KEY")
MAX_CVS = 10
AI_MODEL = "gpt-4-turbo"


def analyze_with_ai(cv_data: Dict, requirements: str) -> Dict:
    """
    Get AI assessment of a single CV using structured prompts
    Returns: {
        'technical_fit': 0-10,
        'culture_fit': 0-10,
        'overall_score': 0-10,
        'strengths': [str],
        'weaknesses': [str],
        'fit_analysis': str
    }
    """
    system_prompt = """
    You are an expert HR analyst specializing in technical recruitment. 
    Evaluate CVs strictly against provided job requirements.
    
    Output JSON format with these keys:
    - technical_fit (0-10): Skills/technologies match
    - culture_fit (0-10): Hobbies/experience alignment
    - overall_score (0-10): Weighted average (70% technical, 30% culture)
    - strengths: Top 3 positive aspects (bullet points)
    - weaknesses: Top 3 improvement areas (bullet points)
    - fit_analysis: 2-3 sentence explanation
    
    Scoring Guidelines:
    - 9-10: Exceptional match
    - 7-8: Strong match with minor gaps
    - 5-6: Partial match
    - Below 5: Poor match
    """
    
    user_prompt = f"""
    JOB REQUIREMENTS:
    {requirements}
    
    CANDIDATE DATA:
    {json.dumps({
        'skills': cv_data.get('skills', []),
        'technologies': cv_data.get('technologies', []),
        'experience': cv_data.get('experience', []),
        'hobbies': cv_data.get('hobbies', [])
    }, indent=2)}
    
    Analyze both technical qualifications and cultural fit.
    """
    
    response = openai.ChatCompletion.create(
        model=AI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2  # Lower for more consistent scoring
    )
    
    return json.loads(response.choices[0].message.content)

def process_cvs(cv_paths: List[str], requirements: str) -> List[Dict]:

    if len(cv_paths) > MAX_CVS:
        print(f"Processing first {MAX_CVS} of {len(cv_paths)} CVs")
        cv_paths = cv_paths[:MAX_CVS]
    
    results = []
    
    for path in cv_paths:
        try:
            print(f"Processing {path}...")
            cv_data = parse_resume(path)
            if not cv_data:
                continue
                
            ai_analysis = analyze_with_ai(cv_data, requirements)
            
            results.append({
                'file': path,
                **ai_analysis,
                'extracted_data': { 
                    'skills': cv_data['skills'],
                    'technologies': cv_data['technologies'],
                    'hobbies': cv_data['hobbies']
                }
            })
            
        except Exception as e:
            print(f"Failed to process {path}: {str(e)}")
    
    return sorted(results, key=lambda x: x['overall_score'], reverse=True)

def print_results(ranked_cvs: List[Dict]):
    """Pretty print AI evaluation results"""
    print("\nCV Ranking Results:")
    print("=" * 80)
    for i, cv in enumerate(ranked_cvs, 1):
        print(f"{i}. {cv['file']}")
        print(f"   Overall Score: {cv['overall_score']}/10")
        print(f"   Technical Fit: {cv['technical_fit']}/10")
        print(f"   Culture Fit: {cv['culture_fit']}/10")
        print(f"   Strengths: {', '.join(cv['strengths'][:3])}")
        print(f"   Weaknesses: {', '.join(cv['weaknesses'][:3])}")
        print(f"   Analysis: {cv['fit_analysis']}")
        print("-" * 80)

if __name__ == "__main__":
    cv_files = ["hasnat.pdf"] 
    job_requirements = """
    We need a full-stack developer with:
    - Core skills: JavaScript, Python, React
    - Nice-to-have: AWS, Docker
    - Culture: Team players who enjoy collaborative coding
    - Bonus: Open source contributions or tech hobbies
    """
    
    ranked_cvs = process_cvs(cv_files, job_requirements)
    print_results(ranked_cvs)