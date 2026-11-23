"""
Executes every code cell in the generated notebook, captures stdout and matplotlib plots,
and saves the notebook with full execution outputs pre-rendered.
"""

import sys
import os
import io
import contextlib
import base64
import nbformat as nbf
import matplotlib
matplotlib.use('Agg') # Non-interactive backend to prevent GUI popups
import matplotlib.pyplot as plt

nb_path = os.path.join(os.path.dirname(__file__), "BDSMA_Extra_Experiment_Startup_Problem_Discovery_Agent_Reddit.ipynb")

print(f"Loading notebook from: {nb_path}")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbf.read(f, as_version=4)

global_scope = {}

# Intercept plt.show to capture active figures
captured_figs = []
def custom_show(*args, **kwargs):
    figs = [plt.figure(n) for n in plt.get_fignums()]
    for f in figs:
        if f not in captured_figs:
            captured_figs.append(f)

plt.show = custom_show

execution_count = 1
for cell_idx, cell in enumerate(nb.cells):
    if cell.cell_type == "code":
        print(f"Executing Code Cell #{execution_count} (index {cell_idx})...")
        cell.outputs = []
        cell.execution_count = execution_count
        
        # Intercept stdout
        stdout_buf = io.StringIO()
        captured_figs.clear()
        plt.close('all') # Clear prior plots
        
        # Clean magic lines for pure python execution
        source_lines = []
        for line in cell.source.splitlines():
            if line.strip().startswith(('!', '%')):
                continue
            source_lines.append(line)
        clean_source = "\n".join(source_lines)
        
        try:
            with contextlib.redirect_stdout(stdout_buf):
                exec(clean_source, global_scope)
                
            # Check for printed output
            stdout_text = stdout_buf.getvalue()
            if stdout_text:
                cell.outputs.append(nbf.v4.new_output(
                    output_type="stream",
                    name="stdout",
                    text=stdout_text
                ))
                
            # Check for captured figures
            all_figs = [plt.figure(n) for n in plt.get_fignums()] + captured_figs
            seen = set()
            for fig in all_figs:
                if fig in seen:
                    continue
                seen.add(fig)
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight", dpi=160)
                img_buf.seek(0)
                img_b64 = base64.b64encode(img_buf.read()).decode("utf-8")
                
                cell.outputs.append(nbf.v4.new_output(
                    output_type="display_data",
                    data={
                        "image/png": img_b64,
                        "text/plain": "<Figure size ...>"
                    }
                ))
            plt.close('all')
            print(f" -> Cell #{execution_count} executed successfully.")
        except Exception as e:
            print(f" ❌ ERROR in Cell #{execution_count}: {e}")
            import traceback
            traceback.print_exc()
            cell.outputs.append(nbf.v4.new_output(
                output_type="error",
                ename=type(e).__name__,
                evalue=str(e),
                traceback=traceback.format_exc().splitlines()
            ))
            
        execution_count += 1

with open(nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"\nSuccessfully executed and populated all notebook cells at: {nb_path}")
