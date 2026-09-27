import numpy as np 
import matplotlib.pyplot as plt 
from pathlib import Path


#first by cards 
#data (will fill in)
data = np.zeros((8,8)) #empty data 

#heatmap 
fig, ax = plt.subplots() 
ax.imshow(data, cmap = "Blues")
n_rows, n_cols = data.shape

#will add stuff about labels + title 

#sets grid lines and ticks 
x_tick_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
y_tick_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

ax.set_xticks(np.arange(-0.5, n_cols, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n_rows, 1), minor=True)
ax.set_xticks(range(len(x_tick_labels)), labels=x_tick_labels)
ax.set_yticks(range(len(y_tick_labels)), labels=y_tick_labels)

ax.grid(which='minor', color='steelblue', linestyle='-', linewidth=1.5)
ax.tick_params(which='minor', bottom=False, left=False)
ax.set_xticks(np.arange(n_cols))
ax.set_yticks(np.arange(n_rows))

ax.set_title("Score by Cards", fontsize=16, fontweight='bold')

ax.set_xlabel("My Choice", fontsize=12)
ax.set_ylabel("OpponentChoice", fontsize=12)

#save to figure folder 
output_dir = Path('./figures')
output_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(output_dir/"cards_viz.png")


#another by tricks 

#data (will fill in)
data = np.zeros((8,8)) #empty data 

#heatmap 
fig, ax = plt.subplots() 
ax.imshow(data, cmap = "Blues")
n_rows, n_cols = data.shape

#will add stuff about labels + title 

#sets grid lines and ticks 
x_tick_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
y_tick_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

ax.set_xticks(np.arange(-0.5, n_cols, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n_rows, 1), minor=True)
ax.set_xticks(range(len(x_tick_labels)), labels=x_tick_labels)
ax.set_yticks(range(len(y_tick_labels)), labels=y_tick_labels)

ax.grid(which='minor', color='steelblue', linestyle='-', linewidth=1.5)
ax.tick_params(which='minor', bottom=False, left=False)
ax.set_xticks(np.arange(n_cols))
ax.set_yticks(np.arange(n_rows))

ax.set_title("Score by Tricks", fontsize=16, fontweight='bold')

ax.set_xlabel("My Choice", fontsize=12)
ax.set_ylabel("OpponentChoice", fontsize=12)

#save to figure folder 
output_dir = Path('./figures')
output_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(output_dir/"tricks_viz.png")







