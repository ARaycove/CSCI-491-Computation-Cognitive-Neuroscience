# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# a. Load the data and plot the wave forms on one plot
# Read the CSV file and assign to data as a pandas dataframe / With error handling
try:
    data = pd.read_csv('wave_form.csv')
    print("Data loaded with headers.")
except:
    try:
        data = pd.read_csv('wave_form.csv', header=None)
        print("Data loaded without headers.")
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

# Plot the waveforms for every piece of data
plt.figure(figsize=(12, 6))
for i in range(len(data)):
    plt.plot(range(data.shape[1]), data.iloc[i].values, color='blue', alpha=0.05)
plt.title('All Waveforms')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.grid(True)
plt.savefig('all_waveforms.png')

# b. Normalize data and perform PCA
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data) # Scale data
pca = PCA(n_components=12) # Initialize PCA with 12 components
pca_result = pca.fit_transform(scaled_data) # Apply PCA on scaled data
print("\nPCA Results:")
print("Explained variance ratio     :", pca.explained_variance_ratio_)
print("Cumulative explained variance:", np.sum(pca.explained_variance_ratio_))
# Plot the things!
plt.figure(figsize=(10, 6))
plt.bar(range(1, 13), pca.explained_variance_ratio_)
plt.plot(range(1, 13), np.cumsum(pca.explained_variance_ratio_), 'ro-')
plt.title('PCA Explained Variance')
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.grid(True)
plt.savefig('pca_variance.png')

# c. Run KMeans with different numbers of clusters and plot inertia
inertia_values = []
for n_clusters in range(1, 9):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(pca_result)
    inertia_values.append(kmeans.inertia_)
# Plot THE ELBOW!
plt.figure(figsize=(10, 6))
plt.plot(range(1, 9), inertia_values, 'bo-')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.grid(True)
plt.savefig('elbow_method.png')
# Elbow is around cluster 3

# d. Plot the wave forms for n_clusters=3
kmeans = KMeans(n_clusters=3, random_state=42)
cluster_labels = kmeans.fit_predict(pca_result)
# Plot waveforms by cluster
plt.figure(figsize=(15, 15))
colors = ['blue', 'green', 'red']
labels = ['Cluster 1', 'Cluster 2', 'Cluster 3']
for cluster in range(3):
    cluster_indices = np.where(cluster_labels == cluster)[0]
    plt.subplot(3, 1, cluster+1)
    for idx in cluster_indices[:]:
        plt.plot(range(data.shape[1]), data.iloc[idx].values, color=colors[cluster], alpha=0.1)
    # Calculate and plot the mean waveform for this cluster
    mean_waveform = data.iloc[cluster_indices].mean()
    plt.plot(range(data.shape[1]), mean_waveform, color=colors[cluster], linewidth=2, label=f'Mean {labels[cluster]}')
    plt.title(f'{labels[cluster]} Waveforms (n={len(cluster_indices)})')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
plt.tight_layout()
plt.savefig('cluster_waveforms.png')
# Plot all mean waveforms together for comparison
plt.figure(figsize=(12, 8))
for cluster in range(3):
    cluster_indices = np.where(cluster_labels == cluster)[0]
    mean_waveform = data.iloc[cluster_indices].mean()
    plt.plot(range(data.shape[1]), mean_waveform, color=colors[cluster], linewidth=2, label=labels[cluster])
plt.title('Mean Waveforms for Each Cluster')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.savefig('mean_waveforms.png')
print("\nCluster sizes:")
for cluster in range(3):
    cluster_size = np.sum(cluster_labels == cluster)
    print(f"{labels[cluster]} size: {cluster_size}")
# Plot first two principal components colored by cluster, YAY MORE PLOTS
plt.figure(figsize=(10, 8))
for cluster in range(3):
    cluster_indices = np.where(cluster_labels == cluster)[0]
    plt.scatter(
        pca_result[cluster_indices, 0],
        pca_result[cluster_indices, 1],
        color=colors[cluster],
        label=labels[cluster],
        alpha=0.7
    )
plt.title('First Two Principal Components by Cluster')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.savefig('pca_clusters.png')
plt.show()

# e. Interpretation of what these waveforms look like
# Interpretation:
# The wave forms very much look like action potentials
# Depolarization followed by repolarization, single action potentials
# The plots seem to exaggerate the hyperpolarization phase, 
# cluster 3 seems off, but there are some outliers plotted that change the scale of the graph, notice the 600 amplitude spike. This is likely erroneous data, as most neurons fire roughly the same way.
#
# 