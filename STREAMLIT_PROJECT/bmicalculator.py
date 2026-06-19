import streamlit as st

# 1. Title
st.title("BMI Calculator")
st.write("Enter your details to calculate your BMI.")

# 2. Get inputs from the user
weight = st.number_input("Enter your weight (kg):", min_value=1.0)
height = st.number_input("Enter your height (meters):", min_value=0.1)

# 3. Button to calculate
if st.button("Calculate BMI"):
    bmi = weight / (height * height)
    st.write("Your BMI is:", round(bmi, 2))

    # 4. Give a message based on the result
    if bmi < 18.5:
        st.warning("You are underweight.")
    elif bmi < 25:
        st.success("You have a normal weight. 👍")
    else:
        st.error("You are overweight.")