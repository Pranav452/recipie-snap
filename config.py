import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Model settings
    MODELS = {
        'caption': 'nlpconnect/vit-gpt2-image-captioning',
        'detection': 'facebook/detr-resnet-50', 
        'recipe': 'microsoft/DialoGPT-medium'
    }
    
    # Detection thresholds
    DETECTION_THRESHOLD = 0.7
    CAPTION_MAX_LENGTH = 50
    RECIPE_MAX_LENGTH = 150
    
    # Food keywords for filtering
    FOOD_KEYWORDS = [
        'apple', 'banana', 'carrot', 'tomato', 'onion', 'potato', 'bread', 
        'egg', 'milk', 'cheese', 'meat', 'chicken', 'beef', 'fish', 'rice', 
        'pasta', 'lettuce', 'pepper', 'garlic', 'lemon', 'orange', 'broccoli', 
        'spinach', 'mushroom', 'corn', 'bean', 'pea', 'avocado', 'cucumber',
        'bell pepper', 'cauliflower', 'cabbage', 'celery', 'ginger', 'herbs'
    ] 