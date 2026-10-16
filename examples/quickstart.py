"""Smallest useful example: python examples/quickstart.py"""
import numpy as np
import pandas as pd
from plotnine import aes, geom_line, ggplot, labs

import roygbviz as rv

rv.use("light")  # or rv.use("dark")

x = np.arange(20)
df = pd.concat([pd.DataFrame({"epoch": x, "loss": np.exp(-x / (4 + k)) + 0.05 * k, "model": m})
                for k, m in enumerate(["Cascade", "Whisper", "Conformer"])])

p = (ggplot(df, aes("epoch", "loss", colour="model"))
     + geom_line(size=1.2)
     + rv.scale_colour_roygbviz_d()
     + labs(title="Training loss", x="Epoch", y="Loss", colour=""))
p.save("quickstart.png", width=6, height=4, dpi=150)
print("wrote quickstart.png")
