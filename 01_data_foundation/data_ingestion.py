"""
Data Ingestion Script for LaDe Dataset
=======================================

Purpose:
    This script demonstrates how to load the LaDe (Last-mile Delivery) dataset
    from Hugging Face in streaming mode for initial schema exploration and
    understanding.

Dataset Source:
    - Repository: Cainiao-AI/LaDe
    - Platform: Hugging Face Datasets
    - Nature: Large-scale, real-world, event-based delivery data

Why Streaming Mode?
    1. Memory Efficiency: The LaDe dataset is large-scale. Loading the entire
       dataset into memory would be impractical and resource-intensive.
    
    2. Schema Exploration: For initial data understanding, we only need to
       inspect sample records, not process the entire dataset.
    
    3. Scalability: Streaming allows us to work with datasets that exceed
       available RAM, which is critical for enterprise-grade analytics.
    
    4. Iterative Development: Enables quick iteration during the exploration
       phase without waiting for full data downloads.

Usage:
    This script is intended for:
    - Initial schema understanding
    - Data structure exploration
    - Field type verification
    - Sample data inspection
    
    NOT intended for:
    - Full data processing
    - Feature engineering
    - Model training
    - Production data pipelines

Author: Data Engineering Team
Stage: STAGE 1 - Data Foundation & Problem Definition
"""

from datasets import load_dataset
import sys


def load_lade_dataset_streaming():
    """
    Load the LaDe dataset in streaming mode from Hugging Face.
    
    Returns:
        IterableDataset: Streaming dataset object that yields records on-demand
    
    Raises:
        Exception: If dataset loading fails (network issues, authentication, etc.)
    """
    try:
        print("=" * 70)
        print("Loading LaDe Dataset from Hugging Face (Streaming Mode)")
        print("=" * 70)
        print()
        
        # Load dataset in streaming mode
        # streaming=True ensures data is fetched incrementally, not all at once
        dataset = load_dataset(
            "Cainiao-AI/LaDe",
            streaming=True,
            trust_remote_code=True  # Required for some HuggingFace datasets
        )
        
        print("✓ Dataset loaded successfully in streaming mode")
        print()
        
        return dataset
        
    except Exception as e:
        print(f"✗ Error loading dataset: {str(e)}", file=sys.stderr)
        print("\nTroubleshooting tips:")
        print("1. Ensure you have internet connectivity")
        print("2. Verify Hugging Face datasets library is installed: pip install datasets")
        print("3. Check if the dataset repository is accessible")
        raise


def inspect_dataset_structure(dataset):
    """
    Inspect the structure of the LaDe dataset.
    
    Args:
        dataset: Streaming dataset object from Hugging Face
    """
    print("Dataset Structure:")
    print("-" * 70)
    
    # Display available splits (train, validation, test, etc.)
    print(f"Available splits: {list(dataset.keys())}")
    print()
    
    # Get the training split for inspection
    train_data = dataset['train']
    
    print("Inspecting first record from training split...")
    print()
    
    # Fetch and display the first record
    # In streaming mode, we use iter() and next() to get records one at a time
    first_record = next(iter(train_data))
    
    print("Field Names and Sample Values:")
    print("-" * 70)
    
    for field_name, field_value in first_record.items():
        # Display field name and type
        field_type = type(field_value).__name__
        
        # Truncate long values for readability
        if isinstance(field_value, (list, dict)):
            display_value = str(field_value)[:100] + "..." if len(str(field_value)) > 100 else str(field_value)
        else:
            display_value = field_value
            
        print(f"  {field_name:25} ({field_type:10}): {display_value}")
    
    print()
    print("=" * 70)


def sample_multiple_records(dataset, n_samples=5):
    """
    Sample multiple records to understand data variability.
    
    Args:
        dataset: Streaming dataset object
        n_samples (int): Number of records to sample
    """
    print(f"\nSampling {n_samples} records for variability analysis...")
    print("=" * 70)
    
    train_data = dataset['train']
    
    for idx, record in enumerate(iter(train_data)):
        if idx >= n_samples:
            break
            
        print(f"\nRecord {idx + 1}:")
        print("-" * 70)
        
        # Display key fields only for brevity
        # Adjust these field names based on actual LaDe schema
        key_fields = ['courier_id', 'city', 'task_id', 'timestamp', 'event_type']
        
        for field in key_fields:
            if field in record:
                print(f"  {field}: {record[field]}")
            else:
                # If expected field doesn't exist, show what fields are available
                if idx == 0:
                    print(f"  Note: '{field}' not found. Available fields: {list(record.keys())[:5]}...")
                    break
    
    print()
    print("=" * 70)


def main():
    """
    Main execution function for dataset exploration.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  LaDe Dataset Ingestion & Schema Exploration".center(68) + "║")
    print("║" + "  STAGE 1: Data Foundation & Problem Definition".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Step 1: Load dataset in streaming mode
    dataset = load_lade_dataset_streaming()
    
    # Step 2: Inspect dataset structure
    inspect_dataset_structure(dataset)
    
    # Step 3: Sample multiple records
    sample_multiple_records(dataset, n_samples=5)
    
    print("\n✓ Schema exploration completed successfully")
    print("\nNext Steps:")
    print("  1. Review data_schema.md for detailed field descriptions")
    print("  2. Review sla_definition.md for SLA labeling strategy")
    print("  3. Review data_dictionary.md for complete field reference")
    print()


if __name__ == "__main__":
    main()
