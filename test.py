# Load model directly
from transformers import AutoTokenizer, AutoModelForPreTraining

tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")
model = AutoModelForPreTraining.from_pretrained("law-ai/InLegalBERT")
def chat():
    print("Welcome to InLegalBERT Chat! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        # Tokenize input
        inputs = tokenizer(user_input, return_tensors="pt")
        # Get model outputs
        with torch.no_grad():
            outputs = model(**inputs)
        # For demonstration, we'll just echo the input as the model is for pretraining (not chat)
        # In a real chat model, you would generate a response here
        print("InLegalBERT: [Model is for pretraining; no chat response available]")

# If you want to run the chat loop directly
if __name__ == "__main__":
    try:
        import torch
    except ImportError:
        print("Please install torch to run this script.")
    else:
        chat()
