# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="varma007ut/Indian_Legal_Assitant")
def main():
    print("Welcome to the Indian Legal Assistant Chat!")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        # Generate response using the pipeline
        responses = pipe(user_input, max_new_tokens=100, do_sample=True, top_p=0.95, temperature=0.8)
        # The pipeline returns a list of dicts with 'generated_text'
        print("Model:", responses[0]['generated_text'])

if __name__ == "__main__":
    main()
