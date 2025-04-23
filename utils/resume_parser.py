import re
import pymupdf



def extract_section(text, section_names):
    """Generic section extractor"""
    for name in section_names:
        pattern = re.compile(
            rf'{name}[^:\n]*[:]?\s*([\s\S]*?)(?=\n{{2,}}|\n[A-Z][a-zA-Z]+:|$)',
            re.IGNORECASE
        )
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return None

def extract_skills(text):
    section = extract_section(text, [
        'skills', 'technical skills', 
        'technologies', 'skills & expertise'
    ])
    return process_list(section) if section else []

def extract_technologies(text):
    section = extract_section(text, [
        'technologies learned', 'technologies',
        'technical skills', 'tools', 'programming languages'
    ])
    return process_list(section) if section else []

def extract_experience(text):
    section = extract_section(text, [
        'experience', 'work experience',
        'employment history', 'professional experience'
    ])
    return process_list(section) if section else []

def extract_hobbies(text):
    section = extract_section(text, [
        'hobbies', 'interests',
        'personal interests', 'activities'
    ])
    return process_list(section) if section else []

def process_list(section_text):
    """Process any list-type section"""
    if not section_text:
        return []
    
    cleaned = re.sub(
        r'[^\w\s,+.#\/\-]|(\s{2,}|\t+)', 
        lambda m: ',' if m.group(1) else '', 
        section_text
    )
    
    items = re.split(r'[\n•*,\-\u2022·‑\/]+', cleaned)
    
    FORMAT_MAP = {
        'aws': 'AWS', 'c#': 'C#', 'c++': 'C++', 
        'sql': 'SQL', 'js': 'JavaScript', 'ts': 'TypeScript',
        'ai': 'AI', 'ml': 'Machine Learning'
    }
    
    def format_item(item):
        item = item.strip()
        return FORMAT_MAP.get(item.lower(), item.title())
    
    return [format_item(i) for i in items if i.strip()]

def parse_resume(pdf_path):
    """Main function to extract all sections"""
    try:
        doc = pymupdf.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        
        return {
            'skills': extract_skills(text),
            'technologies': extract_technologies(text),
            'experience': extract_experience(text),
            'hobbies': extract_hobbies(text),
            'raw_text': text 
        }
        
    except Exception as e:
        print(f"Error processing resume: {e}")
        return None