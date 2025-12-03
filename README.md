# TOEIC-LM: Personalized English Tutoring Assistant via Fine-tuning and Knowledge Distillation

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Model](https://img.shields.io/badge/Model-Qwen2.5--7B--Instruct-blue)
![Technique](https://img.shields.io/badge/Technique-QLoRA_Fine--tuning-orange)
![Framework](https://img.shields.io/badge/Framework-Unsloth-red)
![Status](https://img.shields.io/badge/Status-Research_&_Development-yellow)

## Project Resources
* **Fine-tuned Model (Hugging Face):** [https://huggingface.co/nggiabao19/toeic-lm-v0]
* **Distilled Dataset (Hugging Face):** [https://huggingface.co/datasets/nggiabao19/toeic-tutor-v1]

## 1. Project Overview
TOEIC-LM is a specialized Large Language Model (LLM) project designed to function as a personalized AI tutor for Vietnamese students preparing for the TOEIC exam (Part 5).

Unlike general-purpose models, TOEIC-LM is fine-tuned to:
1.  **Detect and explain specific errors** caused by Vietnamese language interference (L1 interference).
2.  **Provide detailed, empathetic explanations** analyzing both correct and incorrect options.
3.  **Ensure structured JSON output**, facilitating seamless integration into educational software applications.

## 2. Project Status
The project has successfully completed the Data Engineering and Model Training phases. The Deployment phase is currently under active research and development.

| Phase | Component | Status | Description |
| :--- | :--- | :--- | :--- |
| **1** | **Data** | **Completed** | Successfully generated a synthetic dataset via Knowledge Distillation. |
| **2** | **Fine-tuning** | **Completed** | Model fine-tuned using QLoRA; Training loss converged; Adapters uploaded to Hugging Face. |
| **3** | **Evaluation** | **Completed** | Model generates valid JSON and accurate linguistic explanations. |
| **4** | **Deployment** | **In Progress** | Optimization for CPU inference (GGUF Quantization) and backend API integration are currently being developed to overcome hardware constraints on consumer-grade devices. |

## 3. Technical Architecture

### 3.1. Data (Knowledge Distillation)
High-quality training data was generated using a **Knowledge Distillation** pipeline.
* **Teacher Models:** GPT-4o.
* **Methodology:** System prompts were designed to simulate a "Humorous Tutor" persona, enforcing strict JSON output formats.
* **Outcome:** A proprietary dataset of 1,000+ instruction-response pairs covering diverse TOEIC grammar topics.

### 3.2. Fine-tuning Pipeline
* **Base Model:** `Qwen/Qwen2.5-7B-Instruct`. Chosen for its superior performance in multilingual contexts, specifically Vietnamese.
* **Optimization Library:** **Unsloth** was utilized to accelerate training speed by 2x and reduce memory usage.
* **Technique:** **QLoRA** (Quantized Low-Rank Adaptation). The model was trained in 4-bit precision to maximize efficiency on limited GPU resources (Tesla T4).
* **Hyperparameters:**
    * Rank (r): 16
    * LoRA Alpha: 16
    * Optimizer: AdamW 8-bit
    * Learning Rate: 2e-4

## 4. Training Results and Inference
The model demonstrates a strong ability to follow instructions and generate structured JSON.

**Sample Input:**
"Generate a TOEIC question regarding Relative Clauses."

**Model Output (JSON):**
```json
{
    "question": "The man _______ works in the marketing department is my brother.",
    "options": {
        "A": "which",
        "B": "who",
        "C": "whom",
        "D": "whose"
    },
    "correct_answer": "B",
    "analysis": {
        "correct_explanation": "Chúng ta sử dụng 'who' như một đại từ quan hệ để thay thế danh từ chỉ người (The man) khi nó đóng vai trò là chủ ngữ.",
        "wrong_analysis": "A sai vì 'which' dùng cho vật. C sai vì 'whom' dùng cho vật. D sai vì 'whose' dùng cho sự sở hữu.",
        "tutor_comment": "Hãy nhớ, nếu từ này đề cập đến một người và đứng trước một động từ, hãy chọn ngay 'who'!"
    }
}
```
# 5. Repository Structure
``` bash
toeic-lm/
├── assets/                 # Training logs and images
├── data/                   # JSON datasets
├── notebooks/              # Jupyter notebooks for Training and Data Generation
├── src/                    # Source code for Data Pipeline
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```
# 6. How to Reproduce
To reproduce the training process:

## Clone the repository:
``` bash
git clone https://github.com/nggiabao19/toeic-lm.git
```

## Install dependencies:
``` bash
pip install unsloth "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes
``` 
### Run the Training Notebook: 
Navigate to notebooks/TOEIC_LM_Training_Pipeline.ipynb and execute the cells in a GPU-enabled environment (Kaggle or Google Colab).

# 7. Future Roadmap
* Edge Deployment: Resolve current memory constraints during GGUF conversion to enable efficient CPU inference via llama.cpp.
* RAG Integration: Implement Retrieval-Augmented Generation with standardized grammar textbooks to minimize hallucinations.
