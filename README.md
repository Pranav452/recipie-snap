# RecipeSnap - AI Cooking Assistant from Your Fridge 🍳

RecipeSnap is a simple AI-powered cooking assistant that analyzes photos of ingredients in your fridge and suggests delicious recipes you can make with them.

## Features

- 📸 **Image Upload**: Easy drag-and-drop or click-to-upload interface
- 🔍 **Image Analysis**: AI-powered ingredient detection and image captioning
- 🥕 **Smart Ingredient Detection**: Identifies food items from your fridge photos
- 👨‍🍳 **Recipe Generation**: Creates custom recipes based on detected ingredients
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Models Used

This application uses several state-of-the-art AI models:

1. **Image Captioning**: `nlpconnect/vit-gpt2-image-captioning`
   - Vision Transformer + GPT-2 for describing images
   - Helps understand the overall context of the fridge contents

2. **Object Detection**: `facebook/detr-resnet-50`
   - DETR (Detection Transformer) for identifying objects in images
   - Specifically detects ingredients and food items

3. **Recipe Generation**: `microsoft/DialoGPT-medium`
   - Conversational AI model adapted for recipe suggestions
   - Generates cooking instructions based on available ingredients

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager
- At least 4GB of free RAM (for model loading)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd recipiesnap
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

### First Run Notes

- The first time you run the application, it will download the AI models (~2-3GB total)
- This may take several minutes depending on your internet connection
- Subsequent runs will be much faster as models are cached locally

## How to Use

1. **Take a Photo**: Capture a clear photo of your fridge contents or ingredients
2. **Upload Image**: Drag and drop the image or click to browse and select
3. **Analyze**: Click the "Analyze Image & Get Recipe" button
4. **Get Recipe**: View the detected ingredients and generated recipe suggestions

## Tips for Best Results

- 📷 Take well-lit, clear photos of your ingredients
- 🥗 Arrange ingredients visibly in the photo
- 🔍 Include common cooking staples for better recipe suggestions
- 📱 Works with various image formats (JPG, PNG, WEBP)

## Technical Architecture

```
Frontend (HTML/CSS/JS) → Flask Backend → AI Models
                                      ├── Image Captioning
                                      ├── Object Detection  
                                      └── Recipe Generation
```

## System Requirements

- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: ~3GB for models and dependencies
- **Internet**: Required for initial model download
- **Browser**: Modern web browser with JavaScript enabled

## Troubleshooting

### Common Issues

1. **Out of Memory Error**:
   - Reduce image size before uploading
   - Close other applications to free up RAM
   - Use CPU-only mode if GPU memory is limited

2. **Slow Performance**:
   - First run is always slower (model downloading)
   - Consider using a GPU for faster inference
   - Restart the application if memory usage is high

3. **Model Loading Errors**:
   - Ensure stable internet connection for initial download
   - Check that you have sufficient disk space
   - Try deleting the Hugging Face cache and re-downloading

### Performance Optimization

For better performance on systems with limited resources:

1. **Use CPU-only mode** by setting in `app.py`:
   ```python
   torch.device('cpu')
   ```

2. **Reduce image size** before processing by adding image resizing in the upload handler

## Contributing

Feel free to contribute to this project by:
- Adding new AI models for better accuracy
- Improving the UI/UX design
- Adding more recipe templates
- Optimizing performance
- Adding new features

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Hugging Face for providing the pre-trained models
- Flask for the web framework
- The open source AI community for the model implementations

---

**Note**: This is a demonstration project. For production use, consider implementing additional features like user authentication, recipe saving, and more sophisticated ingredient detection algorithms. 