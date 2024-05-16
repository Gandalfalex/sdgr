import numpy as np
from matplotlib import pyplot as plt


def plot_data(data):
    ages = [person['age'] for person in data]
    affinities = [person['affinity'] for person in data]
    sus_scores = [person['sus'] for person in data]
    tlx_scores = [person['tlx'] for person in data]

    fig = plt.figure(figsize=(14, 6))

    # 3D plot for SUS scores
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.scatter(ages, affinities, sus_scores, c='blue', marker='o')
    ax1.set_title("3D Plot for SUS Scores")
    ax1.set_xlabel("Age")
    ax1.set_ylabel("Tech Affinity")
    ax1.set_zlabel("SUS Score")

    # 3D plot for TLX scores
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.scatter(ages, affinities, tlx_scores, c='red', marker='o')
    ax2.set_title("3D Plot for TLX Scores")
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Tech Affinity")
    ax2.set_zlabel("TLX Score")

    plt.show()

def plot_tlx_sus_values(data):
    sus_scores = [person['sus'] for person in data]
    tlx_scores = [person['tlx'] for person in data]

    plt.figure(figsize=(12, 6))

    # Plot for SUS scores
    plt.subplot(1, 2, 1)
    plt.plot(sus_scores, marker='o', linestyle='-', color='blue')
    plt.title("SUS Scores Over Participants")
    plt.xlabel("Participant")
    plt.ylabel("SUS Score")

    # Plot for TLX scores
    plt.subplot(1, 2, 2)
    plt.plot(tlx_scores, marker='o', linestyle='-', color='red')
    plt.title("TLX Scores Over Participants")
    plt.xlabel("Participant")
    plt.ylabel("TLX Score")

    plt.tight_layout()
    plt.show()


def plot_each_result(data):
    plt.boxplot(data)
    plt.show()
