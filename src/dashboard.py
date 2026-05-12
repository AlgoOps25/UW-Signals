"""Streamlit dashboard skeleton for UW-Signals.

Run later with:
    streamlit run src/dashboard.py
"""

from __future__ import annotations

import streamlit as st


def main() -> None:
    """Render MVP dashboard shell."""
    st.set_page_config(page_title="UW-Signals", layout="wide")
    st.title("UW-Signals")
    st.caption("Live options-flow decision dashboard — planning scaffold")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Regime", "Pending")
    col2.metric("Top Index Alert", "None")
    col3.metric("Top Stock Alert", "None")
    col4.metric("Risk State", "Pre-subscription")

    st.divider()
    st.subheader("System Status")
    st.write(
        "This dashboard is a placeholder until Unusual Whales API access is purchased "
        "and live endpoint mappings are confirmed."
    )

    st.subheader("Planned Panels")
    st.markdown(
        """
        - Current regime
        - Market Tide / ETF Tide / Net Flow
        - GEX wall map
        - Top 0DTE contracts
        - Single-stock momentum candidates
        - Risk flags
        - Alert outcome tracker
        """
    )


if __name__ == "__main__":
    main()
