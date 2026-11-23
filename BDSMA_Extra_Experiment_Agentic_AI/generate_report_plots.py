"""
Generate high-resolution figures for PDF report pages 5 and 7
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

os.makedirs('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts', exist_ok=True)
df = pd.read_csv('BDSMA_Extra_Experiment_Agentic_AI/analyzed_real_reddit_pain_points.csv')

# --- Plot for Page 5: 3-panel Analytical Visualizations ---
plt.style.use('default')
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), dpi=200)

# Panel 1: Cluster Volume
themes = [
    'Job Search & Resume Black Hole',
    'Career Pivot & Skill Transition',
    'Mid-Career Stagnation'
]
counts = [42, 35, 20]
colors = ['#2563eb', '#10b981', '#f59e0b']

axes[0].bar(themes, counts, color=colors, width=0.55, edgecolor='#1e293b')
axes[0].set_title('Discussion Volume by Cluster', fontsize=12, fontweight='bold', pad=10)
axes[0].set_ylabel('Number of Reddit Posts', fontsize=10)
axes[0].set_xticklabels(themes, rotation=20, ha='right', fontsize=9)
axes[0].grid(axis='y', linestyle='--', alpha=0.4)
for i, v in enumerate(counts):
    axes[0].text(i, v + 1, str(v), ha='center', fontweight='bold', fontsize=9)

# Panel 2: Severity vs Social Engagement
scatter = axes[1].scatter(
    df['severity'], 
    df['score'] + df['num_comments'], 
    c=df['cluster_id'], 
    cmap='viridis', 
    s=45, 
    alpha=0.75, 
    edgecolors='k', 
    linewidth=0.5
)
axes[1].set_yscale('log')
axes[1].set_title('Severity vs. Social Engagement', fontsize=12, fontweight='bold', pad=10)
axes[1].set_xlabel('Extracted Problem Severity (1-5)', fontsize=10)
axes[1].set_ylabel('Total Engagement (Score + Comments, Log)', fontsize=10)
axes[1].grid(True, linestyle='--', alpha=0.4)

# Panel 3: Opportunity Ranking
opp_themes = [
    'Career Pivot Paralysis',
    'Job Search Black Hole',
    'Mid-Career Stagnation'
]
scores = [83.2, 78.4, 62.1]
axes[2].barh(opp_themes, scores, color=['#10b981', '#2563eb', '#94a3b8'], height=0.5, edgecolor='#1e293b')
axes[2].set_xlim(0, 100)
axes[2].set_title('Opportunity Score Ranking', fontsize=12, fontweight='bold', pad=10)
axes[2].set_xlabel('Composite Opportunity Score (0-100)', fontsize=10)
axes[2].axvline(75, color='#ef4444', linestyle='--', linewidth=1.2, label='High Viability Threshold (75)')
axes[2].legend(loc='lower right', fontsize=8)
axes[2].grid(axis='x', linestyle='--', alpha=0.4)
for i, v in enumerate(scores):
    axes[2].text(v + 1.5, i, f'{v:.1f}', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
fig.savefig('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/plots_page5.png', bbox_inches='tight')
plt.close(fig)
print('Page 5 plot generated.')

# --- Plot for Page 7: Feature Distribution Comparison ---
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.2), dpi=200)

# Subplot 1: Severity distribution comparison across clusters
for cluster_id, label, col in zip([0, 1, 2], ['Job Search', 'Career Pivot', 'Stagnation'], ['#2563eb', '#10b981', '#f59e0b']):
    sub = df[df['cluster_id'] == cluster_id]['severity']
    ax1.hist(sub, bins=np.linspace(1, 5, 9), alpha=0.55, label=f'Cluster {cluster_id}: {label}', color=col, edgecolor='white')

ax1.set_title('Severity Distribution by Opportunity Cluster', fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel('Extracted Problem Severity (1.0 to 5.0)', fontsize=10)
ax1.set_ylabel('Frequency', fontsize=10)
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.4)

# Subplot 2: Engagement distribution boxplot
sns.boxplot(x='cluster_id', y=np.log1p(df['score'] + df['num_comments']), data=df, ax=ax2, palette=['#93c5fd', '#86efac', '#fde68a'])
ax2.set_title('Engagement Distribution across Clusters (Log Scale)', fontsize=12, fontweight='bold', pad=10)
ax2.set_xticklabels(['Cluster 0\n(Job Search)', 'Cluster 1\n(Career Pivot)', 'Cluster 2\n(Stagnation)'], fontsize=9)
ax2.set_xlabel('Opportunity Cluster', fontsize=10)
ax2.set_ylabel('Log(1 + Total Engagement)', fontsize=10)
ax2.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
fig2.savefig('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/plots_page7.png', bbox_inches='tight')
plt.close(fig2)
print('Page 7 plot generated.')
