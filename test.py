import streamlit as st

# Set the title of the app
st.title("Streamlit Empty Component Example")

# Initialize session state to track the existence of the empty component
if "show_placeholder" not in st.session_state:
    st.session_state["show_placeholder"] = False

# Create a button that, when clicked, will toggle the empty component
if st.button("Toggle Empty Component"):
    st.session_state["show_placeholder"] = not st.session_state["show_placeholder"]

# Create an empty component if the toggle is true
if st.session_state["show_placeholder"]:
    placeholder = st.empty()  # Create the empty component
    # Add content to the empty component
    with placeholder.container():
        st.write("This is an empty component!")
        st.text_input(
            "Enter some text"
        )  # Example of a component inside the placeholder

# Display a message indicating whether the component is shown or not
if not st.session_state["show_placeholder"]:
    st.write("The empty component is hidden.")
