import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import json
import pandas as pd
from prettytable import PrettyTable
from sklearn.metrics import mean_absolute_percentage_error
import statistics
import os

def load_model(model_path, device='cuda', dtype=torch.bfloat16):
    print(f"Loading model from {model_path}...")
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True, torch_dtype=dtype)
    model = model.to(device=device, dtype=dtype)
    model.eval()
    print("Model loaded successfully.")
    
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    print("Tokenizer loaded successfully.")
    
    return model, tokenizer

def evaluate_model_classification(model, tokenizer, dataset, device='cuda'):
    correct = 0
    total = 0
    correct_pred = {}
    total_pred = {}
    results = []

    for item in dataset:
        image_path = item["image"]
        category = os.path.basename(os.path.dirname(image_path)).replace('_', ' ')
        if category not in correct_pred:
            correct_pred[category] = 0
            total_pred[category] = 0

    for item in dataset:
        image_path = item["image"]
        category = os.path.basename(os.path.dirname(image_path)).replace('_', ' ')
        image = Image.open(image_path).convert('RGB')
        conversations = item["conversations"]
        
        if len(conversations) > 1 and conversations[0]['role'] == 'user' and conversations[1]['role'] == 'assistant':
            user_conversation = conversations[0]
            assistant_conversation = conversations[1]

            question = user_conversation['content'].replace('<image>\n', '')
            msgs = [{'role': 'user', 'content': question}]
            
            with torch.no_grad():
                res, context, _ = model.chat(
                    image=image,
                    msgs=msgs,
                    context=None,
                    tokenizer=tokenizer,
                    sampling=True,
                    temperature=0.7
                )
            
            expected_response = assistant_conversation['content'].strip().lower()
            model_response = res.strip().lower()

            print(f'expected class response: {expected_response}')
            print(f'model class response: {model_response}')

            
            # Classification accuracy calculation
            if model_response == expected_response:
                correct += 1
                correct_pred[category] += 1
            total += 1
            total_pred[category] += 1
            
            results.append({
                "image": image_path,
                "question": question,
                "expected_response": expected_response,
                "model_response": model_response,
                "category": category
            })
    
    accuracy = (correct / total) * 100 if total > 0 else 0
    
    # Calculate accuracy for each class
    class_accuracies = {}
    for category in correct_pred:
        if total_pred[category] > 0:
            class_accuracies[category] = 100 * float(correct_pred[category]) / total_pred[category]
        else:
            class_accuracies[category] = 0.0

    return results, accuracy, class_accuracies, total_pred, correct_pred


def save_classification_results_to_csv(results_before, results_after_3, accuracy_before, accuracy_after_3, class_accuracies_before, class_accuracies_after_3, total_pred_before, total_pred_after_3, correct_pred_before, correct_pred_after_3, filename):
    combined_results = []
    for before, after_3, in zip(results_before, results_after_3):
        combined_results.append({
            "image": before["image"],
            "question": before["question"],
            "expected_response": before["expected_response"],
            "response_before_finetuning": before["model_response"],
            "response_after_finetuning_3_epochs": after_3["model_response"],
            "category": before["category"]
        })
    
    # Append accuracy information
    combined_results.append({
        "image": "",
        "question": "",
        "expected_response": "Metrics",
        "response_before_finetuning": f"Accuracy: {accuracy_before:.2f}%",
        "response_after_finetuning_3_epochs": f"Accuracy: {accuracy_after_3:.2f}%",
        "category": ""
    })
    
    df = pd.DataFrame(combined_results)
    df.to_csv(filename, index=False)
    print(f"Classification results saved to {filename}")
    
    # Print and save class-specific accuracies
    class_accuracy_df = pd.DataFrame({
        'Class': list(class_accuracies_before.keys()),
        'Accuracy Before Finetuning (%)': [class_accuracies_before[classname] for classname in class_accuracies_before],
        'Accuracy After Finetuning 3 Epochs (%)': [class_accuracies_after_3[classname] for classname in class_accuracies_after_3],
    })
    class_accuracy_df.to_csv('class_accuracies.csv', index=False)
    print(f"Class-specific accuracies saved to class_accuracies.csv")

    # Print class-specific accuracies in a table
    table = PrettyTable()
    table.field_names = ["Class", "Accuracy Before Finetuning (%)", "Accuracy After Finetuning 3 Epochs (%)"]
    for classname in class_accuracies_before:
        if total_pred_before[classname] > 0:
            accuracy_before_class = 100 * float(correct_pred_before[classname]) / total_pred_before[classname]
        else:
            accuracy_before_class = 0.0
        if total_pred_after_3[classname] > 0:
            accuracy_after_3_class = 100 * float(correct_pred_after_3[classname]) / total_pred_after_3[classname]
        else:
            accuracy_after_3_class = 0.0
        table.add_row([classname, f"{accuracy_before_class:.2f}", f"{accuracy_after_3_class:.2f}"])
    print(table)


def main():
    # Paths to the models
    model_path_before_finetune = 'openbmb/MiniCPM-V-2'
    model_path_after_finetune_3 = 'output/output_minicpmv2'
    
    # Load dataset splits
    with open('../training_datasets/test.json', 'r') as f:
        local_food_test = json.load(f)
    
    # Evaluate the model before finetuning
    print("Evaluating model before finetuning...")
    model_before, tokenizer_before = load_model(model_path_before_finetune)
    results_before_classification, accuracy_before, class_accuracies_before, total_pred_before, correct_pred_before = evaluate_model_classification(model_before, tokenizer_before, local_food_test)
    
    # Evaluate the model after finetuning for 3 epochs
    print("Evaluating model after finetuning with 3 epochs...")
    model_after_3, tokenizer_after_3 = load_model(model_path_after_finetune_3)
    results_after_classification_3, accuracy_after_3, class_accuracies_after_3, total_pred_after_3, correct_pred_after_3 = evaluate_model_classification(model_after_3, tokenizer_after_3, local_food_test)
    
    # Print overall results in table
    table = PrettyTable()
    table.field_names = ["Metric", "Value Before Finetuning", "Value After Finetuning 3 Epochs"]
    table.add_row(["Classification Accuracy (%)", f"{accuracy_before:.2f}", f"{accuracy_after_3:.2f}"])
    print(table)
    
    # Save classification results to CSV
    save_classification_results_to_csv(
        results_before_classification, 
        results_after_classification_3, 
        accuracy_before, 
        accuracy_after_3, 
        class_accuracies_before, 
        class_accuracies_after_3, 
        total_pred_before,
        total_pred_after_3,
        correct_pred_before,
        correct_pred_after_3,
        'classification_results.csv'
    )


if __name__ == "__main__":
    main()

