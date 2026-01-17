
from datasets import get_dataset_config_names
try:
    configs = get_dataset_config_names("Cainiao-AI/LaDe", trust_remote_code=True)
    print("Configs:", configs)
except Exception as e:
    print("Error:", e)
