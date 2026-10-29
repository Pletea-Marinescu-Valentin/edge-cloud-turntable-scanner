"""Fig. 2: acquisition geometry of the dual-camera turntable rig and the interleaving rule.

(a) Top view in the object (turntable) frame: the AprilTag ring drawn from data/turntable_tag_layout.json,
    the two cameras at azimuths 180 deg +/- beta/2 and distance d from the axis, and the 40 viewing azimuths
    of one level (20 stops of alpha = 18 deg per camera).
(b) Largest azimuthal gap between consecutive views of a level, and the pairwise depth precision
    sigma_Z = GSD * sigma_px / (2 sin(beta/2)), both as functions of the camera separation beta.

Inputs are the fixed design values of the paper: B = 164.3 mm (calibrated), beta = 27 deg, alpha = 18 deg,
turntable diameter 260 mm, f = 3.9 mm, pixel pitch 1.55 um, sigma_px = 0.5 px.
"""

import json
import math

import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, Polygon, Rectangle
from matplotlib.transforms import Affine2D
import matplotlib.pyplot as plt

import style

B_MM = 164.3            # calibrated distance between the projection centres
BETA_DEG = 27.0         # angular separation of the cameras about the turntable axis
ALPHA_DEG = 18.0        # turntable step
N_STOPS = 20            # stops per revolution
R_DISC_MM = 130.0       # turntable radius (diameter 260 mm)
F_MM, PIXEL_UM, SIGMA_PX = 3.9, 1.55, 0.5

D_MM = B_MM / (2.0 * math.sin(math.radians(BETA_DEG) / 2.0))   # distance of the cameras from the axis
F_PX = F_MM / (PIXEL_UM * 1e-3)
GSD = D_MM / F_PX


def largest_gap(beta_deg, alpha_deg=ALPHA_DEG):
    """Largest angle between consecutive viewing azimuths of one level (two cameras, same stops)."""
    r = np.mod(beta_deg, alpha_deg)
    return alpha_deg - np.minimum(r, alpha_deg - r)


def sigma_z(beta_deg):
    return GSD * SIGMA_PX / (2.0 * np.sin(np.radians(beta_deg) / 2.0))


def top_view(ax):
    layout = json.loads((style.DATA / "turntable_tag_layout.json").read_text(encoding="utf-8"))
    ax.add_patch(Circle((0, 0), R_DISC_MM, facecolor=style.DISC, edgecolor=style.AXIS, linewidth=0.6, zorder=1))
    for tag in layout["tags"]:
        corners = np.array(tag["corners"]) * 1000.0
        xy = np.column_stack([corners[:, 0], -corners[:, 2]])      # top view: x = X, y = -Z (Y out of page)
        ax.add_patch(Polygon(xy, closed=True, facecolor=style.TAG, edgecolor="none", zorder=2))
    ax.plot(0, 0, marker="+", color=style.INK, markersize=5, markeredgewidth=0.8, zorder=3)

    half = BETA_DEG / 2.0
    cams = {1: 180.0 + half, 2: 180.0 - half}
    marks = {1: dict(marker="o", color=style.CAM1), 2: dict(marker="^", color=style.CAM2)}
    centres = {}
    for c, az in cams.items():
        a = math.radians(az)
        cx, cy = D_MM * math.cos(a), D_MM * math.sin(a)
        centres[c] = (cx, cy)
        ax.plot([cx, 0], [cy, 0], color=style.MUTED, linewidth=0.5, zorder=1.5)
        body = Rectangle((-14, -9), 28, 18, facecolor=marks[c]["color"], edgecolor="white", linewidth=0.6,
                         zorder=4, transform=Affine2D().rotate_deg(az).translate(cx, cy) + ax.transData)
        ax.add_patch(body)
        ax.text(cx - 4, cy + (24 if c == 1 else -24), f"camera {c}", ha="center",
                va="bottom" if c == 1 else "top", color=style.INK, fontsize=7)

    # viewing azimuths of one level in the object frame: camera c at stop k sits at az_c - k*alpha
    r_mark = R_DISC_MM + 17.0
    for c, az in cams.items():
        ang = np.radians(az - ALPHA_DEG * np.arange(N_STOPS))
        ax.plot(r_mark * np.cos(ang), r_mark * np.sin(ang), linestyle="none", markersize=3.6,
                markeredgecolor="white", markeredgewidth=0.4, zorder=3, **marks[c])

    # beta at the axis, baseline B and distance d
    arc = np.radians(np.linspace(180.0 - half, 180.0 + half, 30))
    ax.plot(48 * np.cos(arc), 48 * np.sin(arc), color=style.INK, linewidth=0.6, zorder=3)
    ax.text(-54, 0, r"$\beta$", ha="right", va="center", color=style.INK, fontsize=8, zorder=3)
    (x1, y1), (x2, y2) = centres[1], centres[2]
    ax.plot([x1 + 20, x2 + 20], [y1, y2], color=style.INK, linewidth=0.6)
    ax.text((x1 + x2) / 2 + 26, 0, f"$B$ = {B_MM:.1f} mm", ha="left", va="center", fontsize=7, color=style.INK)
    ax.text(-0.52 * D_MM, 0.5 * D_MM * math.sin(math.radians(half)) + 26, rf"$d\approx$ {D_MM:.0f} mm",
            ha="center", va="bottom", fontsize=7, color=style.INK, rotation=-half)

    # 9 deg spacing callout on the rim, scale bar
    ax.annotate(r"$\alpha/2 = 9^\circ$", xy=(r_mark * math.cos(math.radians(40.5)), r_mark * math.sin(math.radians(40.5))),
                xytext=(150, 175), fontsize=7, color=style.INK, ha="left",
                arrowprops=dict(arrowstyle="-", color=style.MUTED, linewidth=0.5))
    ax.plot([60, 160], [-178, -178], color=style.INK, linewidth=1.0)
    ax.text(110, -186, "100 mm", ha="center", va="top", fontsize=7, color=style.INK)

    ax.plot([], [], linestyle="none", markersize=4, label="camera 1 views (20 stops)", **marks[1])
    ax.plot([], [], linestyle="none", markersize=4, label="camera 2 views (20 stops)", **marks[2])
    ax.legend(loc="lower left", bbox_to_anchor=(-0.02, -0.04), handletextpad=0.3, borderaxespad=0.0)

    ax.set_xlim(-D_MM - 40, R_DISC_MM + 105)
    ax.set_ylim(-205, 205)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.0, 1.0, "(a)", transform=ax.transAxes, ha="left", va="top", fontsize=8, color=style.INK)


def interleaving(ax_gap, ax_sig):
    beta = np.linspace(0.0, 50.0, 1001)
    ax_gap.plot(beta, largest_gap(beta), color=style.CAM1)
    ax_sig.plot(beta[beta >= 4.0], sigma_z(beta[beta >= 4.0]), color=style.CAM1)

    for b in (9.0, 27.0, 45.0):
        ax_gap.plot(b, largest_gap(b), marker="o", markersize=3.5, color=style.CAM1, markeredgecolor="white",
                    markeredgewidth=0.5, zorder=3)
    ax_gap.plot(20.0, largest_gap(20.0), marker="o", markersize=3.5, markerfacecolor="white",
                markeredgecolor=style.INK2, markeredgewidth=0.7, zorder=3)
    ax_gap.text(27.0, 19.4, r"this rig, $\beta = 27^\circ$: 40 views $9^\circ$ apart", fontsize=7, color=style.INK,
                ha="center", va="bottom")
    ax_gap.text(21.2, 16.3, r"$\beta = 20^\circ$", fontsize=7, color=style.INK2, ha="left", va="center")
    ax_gap.set_ylabel("largest gap (°)")
    ax_gap.set_ylim(7.0, 21.5)
    ax_gap.set_yticks([9, 12, 15, 18])

    s27 = sigma_z(27.0)
    ax_sig.plot(27.0, s27, marker="o", markersize=3.5, color=style.CAM1, markeredgecolor="white",
                markeredgewidth=0.5, zorder=3)
    ax_sig.annotate(rf"$\sigma_Z\approx$ {s27:.2f} mm", xy=(27.0, s27), xytext=(29.5, 0.27), fontsize=7,
                    color=style.INK, ha="left", va="bottom")
    ax_sig.set_ylabel(r"$\sigma_Z$ (mm)")
    ax_sig.set_ylim(0.0, 0.85)
    ax_sig.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8])
    ax_sig.set_xlabel(r"camera separation $\beta$ (°)")

    for ax in (ax_gap, ax_sig):
        ax.set_xlim(0.0, 50.0)
        ax.set_xticks([0, 9, 18, 27, 36, 45])
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        top = 18.9 if ax is ax_gap else ax.get_ylim()[1]
        ax.plot([27.0, 27.0], [ax.get_ylim()[0], top], color=style.GRID, linewidth=0.8, zorder=0)
    plt.setp(ax_gap.get_xticklabels(), visible=False)
    ax_gap.text(-0.16, 1.02, "(b)", transform=ax_gap.transAxes, ha="left", va="bottom", fontsize=8, color=style.INK)


def main():
    style.apply()
    fig = plt.figure(figsize=(style.TEXT_IN, 2.45))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.25, 1.0], height_ratios=[1.0, 1.0], wspace=0.22, hspace=0.12)
    top_view(fig.add_subplot(gs[:, 0]))
    ax_gap = fig.add_subplot(gs[0, 1])
    interleaving(ax_gap, fig.add_subplot(gs[1, 1], sharex=ax_gap))
    style.save(fig, "fig_geometry.pdf")
    print(f"d = {D_MM:.1f} mm, f_px = {F_PX:.0f} px, GSD = {GSD:.3f} mm/px, sigma_Z(27) = {sigma_z(27.0):.3f} mm, "
          f"largest gap(27) = {largest_gap(27.0):.1f} deg, gap(20) = {largest_gap(20.0):.1f} deg")


if __name__ == "__main__":
    main()
