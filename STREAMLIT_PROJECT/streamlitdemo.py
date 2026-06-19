import streamlit as st

import streamlit as st

# Text input
name = st.text_input("Enter your name:")
st.write("Hello,", name)

# Number input
age = st.number_input("Enter your age:")
st.write("Your age is", age)

import streamlit as st

if st.button("Click Me"):
    st.write("You clicked the button! 🎉")

    import streamlit as st

# Dropdown
city = st.selectbox("Choose your city", ["Chennai", "Delhi", "Mumbai"])
st.write("You selected:", city)

# Checkbox
agree = st.checkbox("I agree to the terms")
if agree:
    st.write("Thank you for agreeing!")

    import streamlit as st

# slider(label, min, max)
number = st.slider("Pick a number", 0, 100)
st.write("You picked:", number)

import streamlit as st

st.success("This is a success message (green).")
st.info("This is an info message (blue).")
st.warning("This is a warning message (yellow).")
st.error("This is an error message (red).")