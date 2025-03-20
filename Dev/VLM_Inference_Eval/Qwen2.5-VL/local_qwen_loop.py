from transformers import AutoProcessor
from vllm import LLM, SamplingParams
from qwen_vl_utils import process_vision_info

# MODEL_PATH = "Qwen/Qwen2.5-VL-7B-Instruct"
# MODEL_PATH = "/storage/qwen2.5_vl_lora_sft_1770steps"
MODEL_PATH = "/storage/qwen2.5_vl_lora_sft_1000steps"

# Initialize model once
llm = LLM(
    model=MODEL_PATH,
    limit_mm_per_prompt={"image": 10, "video": 10},
)

# Set sampling parameters once
sampling_params = SamplingParams(
    temperature=0.1,
    top_p=0.001,
    repetition_penalty=1.05,
    max_tokens=256,
    stop_token_ids=[],
)

# Initialize processor once
processor = AutoProcessor.from_pretrained(MODEL_PATH)

def process_input(media_url):
    """Process image input with fixed question"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": []}
    ]
    
    # # Add image
    # if not media_url.startswith("http"):
    #     media_url = f"file://{media_url}"
    # print(f"media_url: {media_url}")    
    media_dict = {
        "type": "image",
        "image": media_url,
        "min_pixels": 224 * 224,
        "max_pixels": 1280 * 28 * 28,
    }
    messages[1]["content"].append(media_dict)
    
    # Add fixed text
    fixed_text = "what is the name of this dish?"
    messages[1]["content"].append({"type": "text", "text": fixed_text})
    
    # Process the input
    prompt = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    
    image_inputs, video_inputs, video_kwargs = process_vision_info(messages, return_video_kwargs=True)
    
    mm_data = {}
    if image_inputs is not None:
        mm_data["image"] = image_inputs
    
    llm_inputs = {
        "prompt": prompt,
        "multi_modal_data": mm_data,
        "mm_processor_kwargs": video_kwargs if video_inputs else {},
    }
    
    outputs = llm.generate([llm_inputs], sampling_params=sampling_params)
    return outputs[0].outputs[0].text

def main():
    print("Welcome! Enter an image path (or 'quit' to exit)")
    print("Example: '/path/to/img.jpg'")
    
    while True:
        user_input = input("> ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        try:
            # Process the image path with fixed question
            response = process_input(user_input)
            print("\nResponse:", response, "\n")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()