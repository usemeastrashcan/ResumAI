from utils.resume_parser import parse_resume
from utils.ai_enhancement import get_resume_improvements
from utils.formatting_helper import analyze_cv_formatting
from utils.enhanced_new_image import generate_new_cv_design

if __name__ == "__main__":
    resume_data = parse_resume("hasnat.pdf")
    if resume_data:
        # print("Extracted Data:")
        # print(resume_data)
        # suggestions = get_resume_improvements(resume_data)
        # print("\nAI Suggestions:")
        # print(suggestions)
        # print("\nCV Formatting Analysis:")
        formatting_analysis = analyze_cv_formatting("image.png")
        # print(formatting_analysis)
        newCVurl = generate_new_cv_design(formatting_analysis)
