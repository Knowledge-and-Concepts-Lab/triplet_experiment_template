import pandas as pd
import numpy as np
import random
from salmon.triplets.offline import OfflineEmbedding
import os


def train_embedding_model(X_train, X_test, d=5, max_epochs=50_000):
    """
    Train embedding model with early stopping based on test loss.

    Parameters:
    X_train: numpy array of training triplets (head, winner, loser)
    X_test: numpy array of test triplets (head, winner, loser)
    d: embedding dimensions
    max_epochs: maximum training epochs

    Returns:
    best_embedding, lowest_loss, epoch_stopped, counter
    """
    n = int(max(X_train.max(), X_test.max()) + 1)  # number of targets

    model = OfflineEmbedding(n=n, d=d, max_epochs=max_epochs, verbose=100)
    model.partial_fit(X_train)

    current_lowest_loss = 1
    current_best_embedding = model.embedding_
    counter_since_update = 0

    for epoch in range(max_epochs):
        print(epoch)
        model.partial_fit(X_train)
        loss_score = model.score(X_test)

        if loss_score < current_lowest_loss:
            current_lowest_loss = loss_score
            current_best_embedding = model.embedding_
            counter_since_update = 0
        elif abs(loss_score - current_lowest_loss) < 1e-4 and counter_since_update > 10000: #means it will stop if the loss is within 0.0001 of the best loss and hasn't meaningfully improved in 10,000 epochs
            break
        else:
            counter_since_update += 1

    return current_best_embedding, current_lowest_loss, epoch, counter_since_update


def process_all_workers(input_file, additional_data_file, output_dir):
    """
    Process triplets for all workers from a single CSV file and append additional data.

    Parameters:
    input_file: path to input CSV containing all triplets
    additional_data_file: path to CSV containing additional data to append (image file names in alphabetical order)
    output_dir: directory to save consolidated embeddings and model history
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the full datasets
    df = pd.read_csv(input_file)
    additional_data = pd.read_csv(additional_data_file)

    # Initialize list for model history and all embeddings
    model_history = []
    all_embeddings = []

    # Process each worker's data
    for worker_id in df['worker_id'].unique():
        print(f"Processing worker_id: {worker_id}")

        # Get this worker's triplets
        worker_df = df[df['worker_id'] == worker_id]

        # Sample if needed (adjust sample size as necessary)
        n_sample_size = 100
        worker_sample = worker_df.head(int(len(worker_df) * (n_sample_size / 100)))

        # Split data into train and test based on labels
        train_data = worker_sample[worker_sample['sampleSet'] == 'train']
        test_data = worker_sample[worker_sample['sampleSet'] == 'test']

        # Skip if either train or test is empty
        if len(train_data) == 0 or len(test_data) == 0:
            print(f"Skipping worker_id {worker_id} - insufficient train/test data")
            continue

        # Prepare triplet data
        X_train = train_data[["head", "winner", "loser"]].to_numpy()
        X_test = test_data[["head", "winner", "loser"]].to_numpy()

        # Train model and get results
        embedding, loss, epoch, counter = train_embedding_model(X_train, X_test)

        # Create DataFrame from embedding and add worker_id
        emb_df = pd.DataFrame(embedding, columns=[f'dim_{i}' for i in range(embedding.shape[1])])
        emb_df['worker_id'] = worker_id

        # Add the additional data columns by repeating them
        for column in additional_data.columns:
            emb_df[column] = additional_data[column].values[:len(emb_df)]

        # Add to list of all embeddings
        all_embeddings.append(emb_df)

        # Record history
        history_entry = {
            "worker_id": worker_id,
            "lowest_loss": loss,
            "epoch": epoch,
            "counter_from_last_update": counter,
            "n_train_triplets": len(train_data),
            "n_test_triplets": len(test_data)
        }
        model_history.append(history_entry)

        # Save updated history after each worker
        history_df = pd.DataFrame(model_history)
        history_df.to_csv(os.path.join(output_dir, "nf_fpo_face_model_hist.csv"), index=False)

    # ---------------- Group-level embedding across all workers ----------------
    print("Processing group-level embedding across all workers...")
    group_train = df[df['sampleSet'] == 'train'] if 'sampleSet' in df.columns else df
    group_test = df[df['sampleSet'] == 'test'] if 'sampleSet' in df.columns else pd.DataFrame()

    # Fallback split if train/test not present
    if len(group_train) == 0 or len(group_test) == 0:
        shuffled = df.sample(frac=1.0, random_state=42)
        split_idx = int(0.7 * len(shuffled)) if len(shuffled) > 0 else 0
        group_train = shuffled.iloc[:split_idx]
        group_test = shuffled.iloc[split_idx:]

    if len(group_train) > 0 and len(group_test) > 0:
        X_train_group = group_train[["head", "winner", "loser"]].to_numpy()
        X_test_group = group_test[["head", "winner", "loser"]].to_numpy()

        emb_group, loss_group, epoch_group, counter_group = train_embedding_model(X_train_group, X_test_group)

        emb_group_df = pd.DataFrame(emb_group, columns=[f'dim_{i}' for i in range(emb_group.shape[1])])
        emb_group_df['worker_id'] = 'group'

        # Add the additional data columns by repeating them
        for column in additional_data.columns:
            emb_group_df[column] = additional_data[column].values[:len(emb_group_df)]

        # Add to embeddings list
        all_embeddings.append(emb_group_df)

        # Record group history
        history_entry = {
            "worker_id": 'group',
            "lowest_loss": loss_group,
            "epoch": epoch_group,
            "counter_from_last_update": counter_group,
            "n_train_triplets": len(group_train),
            "n_test_triplets": len(group_test)
        }
        model_history.append(history_entry)

        # Save group embeddings separately
        emb_group_df.to_csv(os.path.join(output_dir, "nf_fpo_face_embeddings_group_50kep.csv"), index=False)

    # Update and save history after group-level
    history_df = pd.DataFrame(model_history)
    history_df.to_csv(os.path.join(output_dir, "nf_fpo_face_model_hist.csv"), index=False)

    # Concatenate all embeddings (including group) and save to single CSV
    consolidated_embeddings = pd.concat(all_embeddings, ignore_index=True)
    consolidated_embeddings.to_csv(os.path.join(output_dir, "nf_fpo_face_embeddings_50kep.csv"), index=False)

    return history_df, consolidated_embeddings


# Usage
if __name__ == "__main__":
    random.seed(222)

    # Configure paths
    input_file = "nf_fpo_face_triplets.csv"  # Your input file containing all triplets
    additional_data_file = "nf_fpo_face_levels.csv"  # Your additional data file (in our case, the embedded items in alphabetical order)
    output_dir = "nf_fpo_embeddings"  # Directory for outputs

    # Process all workers
    history, embeddings = process_all_workers(input_file, additional_data_file, output_dir)
    print("Processing complete!")