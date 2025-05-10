# Load model directly
from transformers import AutoTokenizer, AutoModelForPreTraining
import torch

tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")
model = AutoModelForPreTraining.from_pretrained("law-ai/InLegalBERT")

def generate_response(input_text, max_length=100):
    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    
    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True
        )
    
    # Decode and return the generated text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def chat():
    print("Welcome to InLegalBERT Chat! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            response = generate_response(user_input)
            print("InLegalBERT:", response)
        except Exception as e:
            print("Error generating response:", str(e))

# If you want to run the chat loop directly
if __name__ == "__main__":
    try:
        import torch
    except ImportError:
        print("Please install torch to run this script.")
    else:
        chat()
