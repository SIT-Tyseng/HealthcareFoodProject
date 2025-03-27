import os
import wandb
import subprocess

# Initialize W&B
wandb.init()

# Get hyperparameters from W&B config (these will override defaults if specified in sweep)
config = wandb.config

# Define the training command with your provided configuration
command = [
    "llamafactory-cli",
    "train",
    # Model settings
    "--model_name_or_path", "Qwen/Qwen2.5-VL-7B-Instruct",  
    "--image_max_pixels", "262144",
    "--video_max_pixels", "16384",
    "--trust_remote_code", "true",
    
    # Method settings
    "--stage", "sft",
    "--do_train", "true",
    "--finetuning_type", "lora",
    "--lora_rank", str(config.get("lora_rank", 8)),  
    "--lora_target", "all",
    
    # Dataset settings
    "--dataset", "foodsg233_sharegpt_train",         
    "--template", "qwen2_vl",
    "--cutoff_len", "2048",
    # "--max_samples", "1000",                 
    "--overwrite_cache", "true",
    "--preprocessing_num_workers", "16",
    
    # Output settings
    "--output_dir", f"output/{wandb.run.id}",
    "--logging_steps", "10",
    "--save_steps", "500",
    "--plot_loss", "true",
    "--overwrite_output_dir", "true",
    
    # Training settings
    "--per_device_train_batch_size", str(config.get("batch_size", 16)),  # Sweep override or default to 16
    "--gradient_accumulation_steps", "4",
    "--learning_rate", str(config.get("learning_rate", 1.0e-4)),  # Sweep override or default to 1.0e-4
    "--num_train_epochs", str(config.get("epochs", 5.0)),  # Sweep override or default to 5.0
    "--lr_scheduler_type", "cosine",
    "--warmup_ratio", "0.1",
    "--fp16", "true",
    "--ddp_timeout", "180000000",
    "--weight_decay", "0.01",
    "--label_smoothing_factor", "0.1",
    "--report_to", "wandb",
    
    # Evaluation settings
    "--val_size", "0.15",
    "--per_device_eval_batch_size", "8",
    "--evaluation_strategy", "steps",
    "--eval_steps", "50",
]

# Run the training command
process = subprocess.run(command, check=True, text=True, capture_output=True)

# Save logs to files
log_dir = f"output/{wandb.run.id}/logs"
os.makedirs(log_dir, exist_ok=True)
with open(f"{log_dir}/stdout.log", "w") as f:
    f.write(process.stdout)
with open(f"{log_dir}/stderr.log", "w") as f:
    f.write(process.stderr)

# Print a message to confirm
print(f"Logs saved to {log_dir}/stdout.log and {log_dir}/stderr.log")

# Extract cross-entropy loss from stdout (example pattern)
# Adjust the regex based on LLaMA Factory's log format, e.g., "loss: 1.234"
loss_pattern = re.compile(r"loss: (\d+\.\d+)")
matches = loss_pattern.findall(process.stdout)
if matches:
    final_loss = float(matches[-1])  # Take the last logged loss
else:
    final_loss = 1.0  # Fallback if no loss found
    print("Warning: Couldn’t extract loss from logs")

# Log to W&B
wandb.log({"cross_entropy_loss": final_loss})
print(f"Final Loss: {final_loss}")

# Log the cross-entropy loss to W&B
# Placeholder: Replace with actual logic to extract loss from logs or output
# final_loss = 1.0  # Example; parse from process.stdout or output_dir logs
# wandb.log({"cross_entropy_loss": final_loss})

# Finish the W&B run
wandb.finish()