// API endpoint configuration
const API_ENDPOINTS = {
    'text-generation': '/api/generate-text',
    'image-generation': '/api/generate-image',
    'audio-generation': '/api/generate-audio',
    'multimodal': '/api/generate-multimodal'
};

// Model interface templates
const MODEL_INTERFACES = {
    'text-generation': {
        title: 'Text Generation',
        input: `
            <textarea id="text-input" placeholder="Enter your text here..." rows="5"></textarea>
            <button onclick="generateText()" class="button">Generate</button>
        `,
        output: `<div id="text-output"></div>`
    },
    'image-generation': {
        title: 'Image Generation',
        input: `
            <textarea id="image-prompt" placeholder="Describe the image you want to generate..." rows="3"></textarea>
            <input type="file" id="image-input" accept="image/*">
            <button onclick="generateImage()" class="button">Generate</button>
        `,
        output: `<div id="image-output"></div>`
    },
    'audio-generation': {
        title: 'Audio Generation',
        input: `
            <textarea id="audio-prompt" placeholder="Enter text or describe the audio you want to generate..." rows="3"></textarea>
            <input type="file" id="audio-input" accept="audio/*">
            <button onclick="generateAudio()" class="button">Generate</button>
        `,
        output: `<div id="audio-output"></div>`
    },
    'multimodal': {
        title: 'Multimodal Generation',
        input: `
            <textarea id="multimodal-prompt" placeholder="Describe what you want to generate..." rows="3"></textarea>
            <input type="file" id="multimodal-input" accept="image/*,audio/*,video/*">
            <select id="output-type">
                <option value="text">Text</option>
                <option value="image">Image</option>
                <option value="audio">Audio</option>
            </select>
            <button onclick="generateMultimodal()" class="button">Generate</button>
        `,
        output: `<div id="multimodal-output"></div>`
    }
};

// Mock model responses
const MOCK_RESPONSES = {
    text: [
        "Here's a sample text generation response...",
        "Another creative text output...",
        "Generated text content based on your input..."
    ],
    image: [
        "https://picsum.photos/400/300",
        "https://picsum.photos/400/301",
        "https://picsum.photos/400/302"
    ],
    audio: [
        "Sample audio response 1",
        "Sample audio response 2",
        "Sample audio response 3"
    ],
    multimodal: [
        "Combined text and image response...",
        "Multimodal generation result...",
        "Complex output combining multiple formats..."
    ]
};

// Current model type
let currentModel = null;

// Open model interface
function openModelInterface(modelType) {
    currentModel = modelType;
    const modelInterface = document.querySelector('.model-interface');
    const modelInput = document.getElementById('model-input-text');
    const modelInputFile = document.getElementById('model-input-file');
    const modelOutput = document.getElementById('model-output-content');

    // Show/hide file input based on model type
    if (modelType === 'image' || modelType === 'audio') {
        modelInputFile.style.display = 'block';
        modelInput.placeholder = 'Enter a description or upload a file...';
    } else {
        modelInputFile.style.display = 'none';
        modelInput.placeholder = 'Enter your prompt...';
    }

    // Clear previous content
    modelInput.value = '';
    modelOutput.innerHTML = '';
    modelInterface.style.display = 'block';
}

// Close model interface
function closeModelInterface() {
    const modelInterface = document.querySelector('.model-interface');
    modelInterface.style.display = 'none';
    currentModel = null;
}

// Generate content (mock)
function generateContent() {
    const modelInput = document.getElementById('model-input-text').value;
    const modelOutput = document.getElementById('model-output-content');
    const userCredits = document.getElementById('user-credits');
    const currentUser = JSON.parse(localStorage.getItem('current_user'));

    // Check if user has credits
    if (currentUser.tier === 'Free' && currentUser.credits <= 0) {
        alert('You have no credits left. Please upgrade to Premium or wait for credit refresh.');
        return;
    }

    // Show loading state
    modelOutput.innerHTML = '<div class="loading">Generating content...</div>';

    // Simulate API delay
    setTimeout(() => {
        // Get random mock response
        const responses = MOCK_RESPONSES[currentModel];
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];

        // Update UI based on model type
        switch (currentModel) {
            case 'text':
                modelOutput.innerHTML = `<p>${randomResponse}</p>`;
                break;
            case 'image':
                modelOutput.innerHTML = `<img src="${randomResponse}" alt="Generated image">`;
                break;
            case 'audio':
                modelOutput.innerHTML = `
                    <p>${randomResponse}</p>
                    <audio controls>
                        <source src="https://example.com/sample-audio.mp3" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>`;
                break;
            case 'multimodal':
                modelOutput.innerHTML = `
                    <p>${randomResponse}</p>
                    <img src="https://picsum.photos/400/300" alt="Generated image">
                    <audio controls>
                        <source src="https://example.com/sample-audio.mp3" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>`;
                break;
        }

        // Update credits for free tier users
        if (currentUser.tier === 'Free') {
            currentUser.credits -= 1;
            localStorage.setItem('current_user', JSON.stringify(currentUser));
            userCredits.textContent = `Credits: ${currentUser.credits}`;
        }
    }, 2000);
}

// Add event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Add file input change handler
    const modelInputFile = document.getElementById('model-input-file');
    if (modelInputFile) {
        modelInputFile.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                // In a real implementation, you would handle the file upload here
                console.log('File selected:', file.name);
            }
        });
    }
});

// API call helper function
async function callAPI(endpoint, data) {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
        alert('Please sign in to use the models');
        return;
    }

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        alert('Error calling the API. Please try again.');
    }
}

// Model-specific generation functions
async function generateText() {
    const input = document.getElementById('text-input').value;
    const output = document.getElementById('text-output');
    
    output.innerHTML = 'Generating...';
    const result = await callAPI(API_ENDPOINTS['text-generation'], { text: input });
    
    if (result) {
        output.innerHTML = result.generated_text;
    }
}

async function generateImage() {
    const prompt = document.getElementById('image-prompt').value;
    const fileInput = document.getElementById('image-input');
    const output = document.getElementById('image-output');
    
    output.innerHTML = 'Generating...';
    
    const formData = new FormData();
    formData.append('prompt', prompt);
    if (fileInput.files.length > 0) {
        formData.append('image', fileInput.files[0]);
    }
    
    const result = await callAPI(API_ENDPOINTS['image-generation'], formData);
    
    if (result) {
        output.innerHTML = `<img src="${result.image_url}" alt="Generated image">`;
    }
}

async function generateAudio() {
    const prompt = document.getElementById('audio-prompt').value;
    const fileInput = document.getElementById('audio-input');
    const output = document.getElementById('audio-output');
    
    output.innerHTML = 'Generating...';
    
    const formData = new FormData();
    formData.append('prompt', prompt);
    if (fileInput.files.length > 0) {
        formData.append('audio', fileInput.files[0]);
    }
    
    const result = await callAPI(API_ENDPOINTS['audio-generation'], formData);
    
    if (result) {
        output.innerHTML = `
            <audio controls>
                <source src="${result.audio_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        `;
    }
}

async function generateMultimodal() {
    const prompt = document.getElementById('multimodal-prompt').value;
    const fileInput = document.getElementById('multimodal-input');
    const outputType = document.getElementById('output-type').value;
    const output = document.getElementById('multimodal-output');
    
    output.innerHTML = 'Generating...';
    
    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('output_type', outputType);
    if (fileInput.files.length > 0) {
        formData.append('input_file', fileInput.files[0]);
    }
    
    const result = await callAPI(API_ENDPOINTS['multimodal'], formData);
    
    if (result) {
        switch (outputType) {
            case 'text':
                output.innerHTML = result.text;
                break;
            case 'image':
                output.innerHTML = `<img src="${result.image_url}" alt="Generated image">`;
                break;
            case 'audio':
                output.innerHTML = `
                    <audio controls>
                        <source src="${result.audio_url}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                `;
                break;
        }
    }
} 