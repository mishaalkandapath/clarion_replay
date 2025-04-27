import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Rectangle

class SimulationVisualizer:
    def __init__(self):
        # 1) One figure, 2×2 layout:
        #    [ input_grid | work_grid ]
        #    [   target   |  reference ]
        self.fig, ((self.ax_in,    self.ax_work),
                  (self.ax_tgt,   self.ax_ref)) = plt.subplots(2, 2, figsize=(8,8))

        # 2) Colormap for 0=empty,1=half-T,2=mirror-L,3=vertical,4=horizontal
        self.cmap = colors.ListedColormap(
            ['white','red','blue','green','orange']
        )
        self.norm = colors.BoundaryNorm([0,1,2,3,4,5], self.cmap.N)

        # 3) Configure top‐row (trial) axes
        for ax in (self.ax_in, self.ax_work):
            ax.set_xlim(0,6); ax.set_ylim(6,0)
            ax.set_xticks(np.arange(7)); ax.set_yticks(np.arange(7))
            ax.set_xticklabels([]); ax.set_yticklabels([])
            ax.grid(False)
        empty = np.zeros((6,6), int)
        self.inmesh  = self.ax_in .pcolormesh(
            empty, cmap=self.cmap, norm=self.norm,
            edgecolors='gray', linewidth=0.5, antialiased=False
        )
        self.workmesh = self.ax_work.pcolormesh(
            empty, cmap=self.cmap, norm=self.norm,
            edgecolors='gray', linewidth=0.5, antialiased=False
        )

        # 4) Configure bottom‐row (response) axes, hide box lines
        for ax in (self.ax_tgt, self.ax_ref):
            ax.set_xlim(0, 3)
            ax.set_ylim(3, 0)
            ax.set_xticks([])            # no tick marks
            ax.set_yticks([])
            ax.set_xticklabels([])       # no tick labels
            ax.set_yticklabels([])
            for spine in ax.spines.values():
                spine.set_visible(False) # hide box lines
            ax.set_visible(False)        # stay hidden until response


        # 5) Status + reward text (in figure coords)
        self.status_text = self.fig.text(0.5, 0.95, "", ha='center')
        self.reward_text = self.fig.text(0.5, 0.45, "", ha='center')  # lowered

        # 6) Response question + choices (hidden initially)
        self.question_text = self.fig.text(
            0.5, 0.28, "", ha='center', visible=False
        )
        self.yes_text = self.fig.text(
            0.45, 0.18, "Yes", ha='center', visible=False
        )
        self.no_text  = self.fig.text(
            0.55, 0.18, "No",  ha='center', visible=False
        )

        # 7) Brick‐shape definitions
        self.brick_coords = {
            1: [(0,0),(0,1),(1,0)],  # half-T
            2: [(0,1),(1,1),(1,0)],  # mirror-L
            3: [(0,0),(0,1),(0,2)],  # horizontal
            4: [(0,1),(1,1),(2,1)],  # vertical
        }

    def start_trial(self, lag=0.5):
        """Show empty trial screen, with optional lag."""
        empty = np.zeros((6,6), int)
        self.inmesh .set_array(empty.ravel())
        self.workmesh.set_array(empty.ravel())
        self.status_text.set_text("Relation:    Reference:    Target:")
        self.reward_text.set_text("Reward:")
        # show trial axes, hide response
        self.ax_in .set_visible(True)
        self.ax_work.set_visible(True)
        self.ax_tgt.set_visible(False)
        self.ax_ref.set_visible(False)
        self.question_text.set_visible(False)
        self.yes_text.set_visible(False)
        self.no_text.set_visible(False)
        self.fig.canvas.draw(); plt.pause(lag)

    def update_input(self, grid6x6, lag=0.5):
        """Update the left-hand input grid (6×6 int array)."""
        self.inmesh.set_array(grid6x6.ravel())
        self.fig.canvas.draw(); plt.pause(lag)

    def update_work(self, grid6x6, lag=0.5):
        """Update the right-hand working grid."""
        self.workmesh.set_array(grid6x6.ravel())
        self.fig.canvas.draw(); plt.pause(lag)

    def update_status(self, relation, reference, target, reward, lag=0.5):
        """Update top text and reward text below."""
        self.status_text.set_text(
            f"Relation: {relation}    Reference: {reference}    Target: {target}"
        )
        self.reward_text.set_text(f"Reward: {reward}")
        self.fig.canvas.draw(); plt.pause(lag)
        
    def _draw_brick(self, ax, shape_id, scale=0.8):
        ax.clear()
        # 3×3 data coords
        ax.set_xlim(0, 3)
        ax.set_ylim(3, 0)
        ax.set_xticks([]); ax.set_yticks([])

        # hide the box lines
        for spine in ax.spines.values():
            spine.set_visible(False)

        coords = self.brick_coords[shape_id]
        # figure out how many cells wide / tall this brick is
        w_cells = max(c for r,c in coords) + 1
        h_cells = max(r for r,c in coords) + 1

        # compute margins to center it in a 3×3 square
        margin_x = (3 - w_cells * scale) / 2
        margin_y = (3 - h_cells * scale) / 2

        for (r, c) in coords:
            x0 = margin_x + c * scale
            y0 = margin_y + r * scale
            rect = Rectangle(
                (x0, y0), scale, scale,
                facecolor=self.cmap(shape_id),
                edgecolor='black'
            )
            ax.add_patch(rect)

    def start_response(self, target_id, reference_id, relation, display_lag=0.5):
        """
        Reveal the response panel (bottom row) *without* hiding the trial grids,
        draw the bricks, and display “relation?”.
        """
        # draw the two bricks
        self._draw_brick(self.ax_tgt, target_id)
        self._draw_brick(self.ax_ref, reference_id)
        # reveal bottom axes
        self.ax_tgt.set_visible(True)
        self.ax_ref.set_visible(True)
        # show question, choices un-bolded
        self.question_text.set_text(f"{relation}?")
        self.question_text.set_visible(True)
        self.yes_text .set_visible(True); self.yes_text .set_fontweight('normal')
        self.no_text  .set_visible(True); self.no_text  .set_fontweight('normal')
        self.fig.canvas.draw(); plt.pause(display_lag)
    
    def choose_response(self, choice, choice_lag=0.5):
        """
        After the model “deliberates,” bold either Yes or No.
        """
        if choice.lower() == 'yes':
            self.yes_text.set_fontweight('bold')
        else:
            self.no_text.set_fontweight('bold')
        self.fig.canvas.draw(); plt.pause(choice_lag)


if __name__ == "__main__":
    # --- Example Usage ---
    viz = SimulationVisualizer()

        # ─── Trial 1 arrays ────────────────────────────────────────────────────────────
    # Input grid: half-T @ (1,1) and horizontal @ (3,3)
    inp1 = np.zeros((6,6), dtype=int)
    # half-T shape (1)
    inp1[1,1] = inp1[1,2] = inp1[2,1] = 1
    # horizontal shape (4)
    inp1[3,3] = inp1[3,4] = inp1[3,5] = 4

    # Working‐space after building just the half-T
    wrk1a = np.zeros_like(inp1)
    wrk1a[1,1] = wrk1a[1,2] = wrk1a[2,1] = 1

    # Working‐space after adding the horizontal
    wrk1b = wrk1a.copy()
    wrk1b[3,3] = wrk1b[3,4] = wrk1b[3,5] = 4


    # ─── Trial 2 arrays ────────────────────────────────────────────────────────────
    # Input grid: mirror-L @ (0,4) and vertical @ (2,2)
    inp2 = np.zeros((6,6), dtype=int)
    # mirror-L shape (2)
    for (r,c) in [(0,4),(1,4),(1,3)]:
        inp2[r,c] = 2
    # vertical shape (3)
    for (r,c) in [(2,2),(3,2),(4,2)]:
        inp2[r,c] = 3

    # Working‐space after building just the mirror-L
    wrk2a = np.zeros_like(inp2)
    for (r,c) in [(0,4),(1,4),(1,3)]:
        wrk2a[r,c] = 2

    # Working‐space after adding the vertical
    wrk2b = wrk2a.copy()
    for (r,c) in [(2,2),(3,2),(4,2)]:
        wrk2b[r,c] = 3

    # --- TRIAL 1 ---
    viz.start_trial(lag=1.0)
    viz.update_input(inp1, lag=1.0)
    viz.update_work(wrk1a, lag=1.0)
    viz.update_status('right','half-T','horizontal',0.3, lag=1.0)
    viz.update_work(wrk1b, lag=1.0)
    viz.update_status('right','half-T','horizontal',0.8, lag=1.0)

    # RESPONSE 1
    viz.start_response(4, 1, 'right', display_lag=1.0)
    viz.choose_response('yes', choice_lag=1.0)

    # --- TRIAL 2 ---
    viz.start_trial(lag=1.0)
    viz.update_input(inp2, lag=1.0)
    viz.update_work(wrk2a, lag=1.0)
    viz.update_status('above','mirror-L','vertical',0.2, lag=1.0)
    viz.update_work(wrk2b, lag=1.0)
    viz.update_status('above','mirror-L','vertical',1.0, lag=1.0)

    # RESPONSE 2
    viz.start_response(3, 2, 'above', display_lag=1.0)
    viz.choose_response('no', choice_lag=1.0)
