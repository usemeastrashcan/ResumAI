import openai
import webbrowser

def generate_new_cv_design(recommendations):
    prompt = f"Generate a professional CV image based on these recommendations: {recommendations}"
    
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    
    enhanced_image_url = response['data'][0]['url']
    try:
        webbrowser.open(enhanced_image_url)  # Open in a new tab, if possible
    except Exception as e:
        print(f"Failed to open URL: {e}\nManually visit: {enhanced_image_url}")
    return enhanced_image_url 