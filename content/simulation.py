# Dies ist eine Datei mit Code zur Simulation von Übungsblatt 08
#
# Der Inhalt wird zum aktuellen Zeitpunkt NICHT erklärt. Teile davon sind Thema
# zukünftiger Vorlesungseinheiten, andere Teile sind sehr spezifisch für die
# Online-Jupyter-Umgebung und nicht Teil des Modulstoffs.
#
# Anders gesagt: Es gibt hier nichts zu sehen, bitte gehen Sie in eine andere Datei


# ============ VARIANTE (standard): Text-Animation ============
import time
from IPython.display import clear_output, display

def balken(wert, minimum, maximum, breite=26):
    """Zeichnet einen Balken für die Live-Visualisierung."""
    anteil = max(0.0, min(1.0, (wert - minimum) / (maximum - minimum)))
    n = int(breite * anteil)
    return "█" * n + "░" * (breite - n)

def text_animation(zyklus, zyklen, zustand, sensoren, motoren, pause=0.5):
    abstand = sensoren["abstand"].messen()
    licht   = sensoren["licht"].messen()
    clear_output(wait=True)
    print(f"🤖  Zyklus {zyklus}/{zyklen}   Zustand: {zustand}")
    print("─" * 60)
    print(f"Abstand ▸ {balken(abstand, 0, 300)}  {abstand:6.1f} cm")
    print(f"Licht   ▸ {balken(licht, 0, 1000)}  {licht:6.1f} lx")
    print("─" * 60)
    for m in motoren.values():
        print(f"{m.name:<22} {balken(m.aktuelle_drehzahl(), -100, 100)}  {m.aktuelle_drehzahl():+6.0f} U/min")
    for s in sensoren.values():
        print(f"{s.name:<22} {s.messen():+6.0f}")
    time.sleep(pause)


# ============ VARIANTE (optional): matplotlib-Draufsicht, async animiert ============
# Funktioniert nicht in jeder Jupyter-Umgebung

import asyncio
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
from IPython.display import clear_output, display

async def matplotlib_animation(sensoren, motoren, roboter_steuerung, zyklen=12, abstand_grenzwert=40.0, pause=0.25):
    """Async-Live-Animation einer Roboter-Draufsicht."""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-170, 170); ax.set_ylim(-170, 170)
    ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    ax.set_xlabel("x [cm]"); ax.set_ylabel("y [cm]")

    robot = Circle((0, 0), 15, fc="0.4", ec="black", zorder=3)
    ax.add_patch(robot)
    cone  = Wedge((0, 0), 60, -30, 30, fc="lightblue", alpha=0.35, ec="blue", lw=1)
    ax.add_patch(cone)
    info  = ax.text(0, -150, "", ha="center", fontsize=10)
    motxt = ax.text(0, -165, "", ha="center", fontsize=9, family="monospace")

    for zyklus in range(1, zyklen + 1):
        abstand = sensoren["abstand"].messen()
        licht   = sensoren["licht"].messen()
        gyro    = sensoren["gyro"].messen()

        zustand = roboter_steuerung(sensoren, motoren)

        cone.set_radius(abstand)
        cone.set_facecolor("lightblue" if zustand == "FAHREN" else "#ffcccc")
        cone.set_edgecolor("blue" if zustand == "FAHREN" else "red")
        info.set_text(f"Zyklus {zyklus}/{zyklen}  Zustand: {zustand}\n"
                      f"Abstand {abstand:.0f} cm · Licht {licht:.0f} lx · Gyro {gyro:+.0f} °/s")
        motxt.set_text("   ".join(f"{m.name.split()[0]}: {m.aktuelle_drehzahl():+.0f} U/min"
                                   for m in motoren.values()))

        clear_output(wait=True)
        display(fig)
        await asyncio.sleep(pause if pause > 0 else 0)   # an Browser-Event-Loop abgeben

    plt.close(fig)
    print("Fertig – Animation beendet.")
