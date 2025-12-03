import json
import random
import os
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv
from huggingface_hub import login

# Load Env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Dinh nghia Template Prompt 
TRAINING_PROMPT_TEMPLATE = """Dưới đây là một câu hỏi TOEIC. Hãy đóng vai một gia sư vui tính, giải thích chi tiết đáp án và chỉ ra các bẫy ngữ pháp.

### Câu hỏi:
{question}

### Các lựa chọn:
A. {option_a}
B. {option_b}
C. {option_c}
D. {option_d}

### Yêu cầu:
Trả về định dạng JSON bao gồm: dịch nghĩa, giải thích đúng sai và cấu trúc ngữ pháp liên quan.
"""

def format_data(raw_item):
    """Chuyen doi 1 dong du lieu raw sang dinh dang Alpaca""" 
    
    # Tao noi dung cau hoi cho phan Instruction
    instruction = TRAINING_PROMPT_TEMPLATE.format(
        question=raw_item['question'],
        option_a=raw_item['options']['A'],
        option_b=raw_item['options']['B'],
        option_c=raw_item['options']['C'],
        option_d=raw_item['options']['D']
    )
    
    # Output mong muon chinh la toan bo cuc JSON analysis
    output_json = json.dumps(raw_item, ensure_ascii=False, indent=4)
    
    return {
        "instruction": instruction,
        "input": "", # Khong co input phu
        "output": output_json
    }

def main():
    print("Processing data...")
    
    input_file = "data/raw/toeic_full_dataset.json"
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f"Total raw samples: {len(raw_data)}")
    
    # Convert sang format training
    processed_data = []
    for item in raw_data:
        # Kiem tra du lieu hop le (phai co du truong)
        if "question" in item and "options" in item and "analysis" in item:
            processed_data.append(format_data(item))
            
    print(f"Valid samples after formatting: {len(processed_data)}")
    
    # Chuyen sang Hugging Face Dataset Object
    dataset = Dataset.from_list(processed_data)
    
    # Chia Train/Test (90/10)
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    
    print("Dataset split result:")
    print(dataset)
    
    # Luu local 
    dataset.save_to_disk("data/processed/toeic_dataset_hf")
    print("Saved processed data to data/processed/toeic_dataset_hf")

    # Upload Hugging Face
    if HF_TOKEN:
        try:
            print("Uploading to Hugging Face Hub...")
            login(token=HF_TOKEN)
            
            HF_USERNAME = input("Enter your Hugging Face Username: ")
            repo_id = f"{HF_USERNAME}/toeic-tutor-v1"
            
            dataset.push_to_hub(repo_id)
            print(f"Success! Dataset is online at: https://huggingface.co/{repo_id}")
        except Exception as e:
            print(f"Upload error: {e}")
    else:
        print("HF_TOKEN not found in .env. Skipping upload step.")

if __name__ == "__main__":
    main()