prob = 0.0

if prob > 0.7:

    st.error(
        "High Risk Customer"
    )

    st.write(
        """
        Recommended Action:
        - Loyalty Discount
        - Free Tech Support
        - Annual Contract Offer
        """
    )