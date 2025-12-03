import os
import json
import time
import random
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT_TOEIC, USER_PROMPT_TEMPLATE
from topics import TOEIC_TOPICS

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Khoi tao OpenAI Client
client = OpenAI(api_key=API_KEY)

# Cau hinh Model
MODEL_NAME = "gpt-4o-mini"

DATA_FILE = "data/raw/toeic_full_dataset.json"

def generate_batch(topic, difficulty, num_questions=5, retries=3):
    """Goi OpenAI API de sinh du lieu"""
    
    user_content = USER_PROMPT_TEMPLATE.format(
        num_questions=num_questions,
        topic=topic,
        difficulty=difficulty
    ) + "\n\n(Remember: Output strictly in JSON format inside a wrapper object if necessary)"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_TOEIC},
        {"role": "user", "content": user_content}
    ]
    
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.9,
                response_format={"type": "json_object"}, # BAT BUOC TRA VE JSON HOP LE
            )
            
            raw_content = response.choices[0].message.content
            data = json.loads(raw_content)
            
            # Xu ly truong hop OpenAI tra ve dict bao ngoai list (vi du: {"questions": [...]})
            if isinstance(data, dict):
                # Tim key nao chua list thi lay
                for key, value in data.items():
                    if isinstance(value, list):
                        data = value
                        break
                else:
                    # Neu khong tim thay list, co the data chinh la 1 object don le?
                    # Ep lai thanh list neu can, hoac bo qua
                    if isinstance(data, dict): # Van la dict
                         # Neu cau truc dung la 1 cau hoi don le
                         if "question" in data:
                             data = [data]
                         else:
                             print(f"Invalid JSON format (Attempt {attempt + 1})...")
                             continue

            if isinstance(data, list) and len(data) > 0:
                return data
            else:
                print(f"Empty data or invalid list format (Attempt {attempt + 1})...")
                
        except Exception as e:
            print(f"Error (Attempt {attempt + 1}): {e}")
            time.sleep(5) 
            
    return []

def save_data_append(new_data, filename):
    """Luu noi tiep vao file JSON"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []
    else:
        existing_data = []

    existing_data.extend(new_data)
    
    # Loai bo du lieu trung lap dua tren cau hoi
    unique_data = {}
    for item in existing_data:
        # Dung question lam key de loc trung
        if isinstance(item, dict) and "question" in item:
             unique_data[item['question']] = item
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(list(unique_data.values()), f, ensure_ascii=False, indent=4)

def main():
    print(f"Starting TOEIC-LM data generation process with {MODEL_NAME}...")
    
    QUESTIONS_PER_BATCH = 5
    BATCHES_PER_TOPIC = 6 
    
    total_steps = len(TOEIC_TOPICS) * BATCHES_PER_TOPIC
    pbar = tqdm(total=total_steps, desc="Generating Data")

    for topic in TOEIC_TOPICS:
        for _ in range(BATCHES_PER_TOPIC):
            difficulty = random.choice(["Dễ (350-500)", "Trung bình (500-700)", "Khó (700+)"])
            
            new_questions = generate_batch(topic, difficulty, num_questions=QUESTIONS_PER_BATCH)
            
            if new_questions:
                save_data_append(new_questions, DATA_FILE)
            
            pbar.update(1)
            time.sleep(1) 
            
    pbar.close()
    print(f"\nCompleted! Check file: {DATA_FILE}")

if __name__ == "__main__":
    main()