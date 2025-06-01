import os
import io
import base64
from PIL import Image
import torch
from transformers import (
    VitGPT2LMHeadModel, 
    ViTImageProcessor, 
    AutoTokenizer,
    DetrImageProcessor, 
    DetrForObjectDetection,
    AutoModelForCausalLM
)
from flask import Flask, render_template, request, jsonify
import warnings
warnings.filterwarnings("ignore")

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize models
print("Loading models...")

# Image captioning model
caption_processor = ViTImageProcessor.from_pretrained(Config.MODELS['caption'])
caption_model = VitGPT2LMHeadModel.from_pretrained(Config.MODELS['caption'])
caption_tokenizer = AutoTokenizer.from_pretrained(Config.MODELS['caption'])

# Object detection model
detection_processor = DetrImageProcessor.from_pretrained(Config.MODELS['detection'])
detection_model = DetrForObjectDetection.from_pretrained(Config.MODELS['detection'])

# Recipe generation model (using a smaller model for simplicity)
recipe_tokenizer = AutoTokenizer.from_pretrained(Config.MODELS['recipe'])
recipe_model = AutoModelForCausalLM.from_pretrained(Config.MODELS['recipe'])
recipe_tokenizer.pad_token = recipe_tokenizer.eos_token

print("Models loaded successfully!")

def generate_caption(image):
    """Generate caption for the image"""
    inputs = caption_processor(image, return_tensors="pt")
    with torch.no_grad():
        output = caption_model.generate(**inputs, max_length=Config.CAPTION_MAX_LENGTH, num_beams=5)
    caption = caption_tokenizer.decode(output[0], skip_special_tokens=True)
    return caption

def detect_objects(image):
    """Detect objects in the image"""
    inputs = detection_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = detection_model(**inputs)
    
    # Convert outputs to COCO api format
    target_sizes = torch.tensor([image.size[::-1]])
    results = detection_processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.5)
    
    detected_objects = []
    for result in results:
        for score, label in zip(result["scores"], result["labels"]):
            if score > Config.DETECTION_THRESHOLD:  # Higher confidence threshold
                object_name = detection_model.config.id2label[label.item()]
                detected_objects.append(object_name)
    
    return list(set(detected_objects))  # Remove duplicates

def generate_recipe(ingredients):
    """Generate recipe suggestions based on ingredients"""
    prompt = f"Create a simple recipe using these ingredients: {', '.join(ingredients)}. Recipe:"
    
    # Encode the prompt
    input_ids = recipe_tokenizer.encode(prompt + recipe_tokenizer.eos_token, return_tensors='pt')
    
    # Generate response
    with torch.no_grad():
        output = recipe_model.generate(
            input_ids, 
            max_length=input_ids.shape[1] + Config.RECIPE_MAX_LENGTH,
            num_beams=3,
            temperature=0.7,
            do_sample=True,
            pad_token_id=recipe_tokenizer.eos_token_id
        )
    
    # Decode the response
    response = recipe_tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    # Clean up the response
    recipe_text = response.strip()
    if not recipe_text:
        # Fallback simple recipe generation
        recipe_text = f"""
Simple Recipe with {', '.join(ingredients[:3])}:

1. Wash and prepare your ingredients: {', '.join(ingredients[:3])}
2. Heat a pan with a little oil
3. Add the main ingredients and cook for 5-10 minutes
4. Season with salt, pepper, and your favorite spices
5. Cook until tender and serve hot

Enjoy your homemade dish!
        """
    
    return recipe_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Process the image
        image = Image.open(file.stream).convert('RGB')
        
        # Generate caption
        caption = generate_caption(image)
        
        # Detect objects/ingredients
        detected_objects = detect_objects(image)
        
        # Filter for food-related items using config
        ingredients = []
        for obj in detected_objects:
            obj_lower = obj.lower()
            if any(keyword in obj_lower for keyword in Config.FOOD_KEYWORDS):
                ingredients.append(obj)
        
        # If no specific ingredients detected, extract from caption
        if not ingredients:
            caption_words = caption.lower().split()
            for keyword in Config.FOOD_KEYWORDS:
                if keyword in caption_words:
                    ingredients.append(keyword.title())
        
        # Ensure we have some ingredients
        if not ingredients:
            ingredients = ['vegetables', 'basic pantry items']
        
        # Generate recipe
        recipe = generate_recipe(ingredients)
        
        return jsonify({
            'caption': caption,
            'ingredients': ingredients,
            'recipe': recipe
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 