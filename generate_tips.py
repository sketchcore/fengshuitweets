import requests
import json

API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
headers = {"Authorization": "Bearer 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"}

def generate_feng_shui_tip():
    prompt = "Generate a short, engaging, and funny feng shui tip for home or office in 280 characters or less."
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.95,
            "do_sample": True,
        }
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for bad responses
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return "Error"
    return response_data[0]['generated_text'].strip()

def generate_and_save_tips(num_tips=100):
    print("Generating feng shui tips...")
    tips = [generate_feng_shui_tip() for _ in range(num_tips)]
    print("Tips generated.")
    with open('feng_shui_tips.json', 'w') as f:
        json.dump(tips, f)

if __name__ == "__main__":
    generate_and_save_tips()