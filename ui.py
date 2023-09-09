import streamlit as st
import requests
import datetime
BASE_URL = "http://localhost:8000/api/v1"


def login(username: str, password: str) -> str:
    """Log in to the API and return the access token."""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password},
    )
    response.raise_for_status()
    data = response.json()
    return data["access_token"], data["exp"]


def create_license_plate(token: str, license_plate: dict):
    """Create a new license plate record."""
    response = requests.post(
        f"{BASE_URL}/license-plate/create-license-plate",
        headers={"Authorization": f"Bearer {token}"},
        json=license_plate,
    )
    response.raise_for_status()
    return response.json()


def read_license_plate(token: str, image_file):
    """Read a license plate from an uploaded image."""
    response = requests.post(
        f"{BASE_URL}/license-plate/read-license-plate",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": image_file},
    )
    response.raise_for_status()
    return response.json()


st.title("License Plate Manager")

if (st.session_state.get(
        "token",
        None,
    ) is None
    or datetime.datetime.utcnow() >= datetime.datetime.fromisoformat(
        st.session_state.get(
        "token_expiration",
        datetime.datetime.utcnow(),
        ).replace("Z", "+00:00"))):

    # Login form
    login_form = st.empty()

    with login_form.container():
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Log in")

    if login_button:
        (
            st.session_state["token"],
            st.session_state["token_expiration"]
        ) = login(
            username,
            password,
        )
        st.success("Logged in successfully")
        login_form.empty()

        create_plate_tab, read_plate_tab = st.tabs(
            ["Create License Plate", "Read License Plate"])

        with create_plate_tab:
            st.header("Create License Plate")
            license_plate_number = st.text_input("License Plate Number")
            license_plate_wanted = st.checkbox("Wanted")
            if st.button("Create License Plate"):
                if len(license_plate_number) <= 0:
                    st.error("License plate number must not empty")
                else:
                    license_plate = create_license_plate(
                        st.session_state["token"],
                        {
                            "number": license_plate_number,
                            "wanted": license_plate_wanted,
                        },
                    )
                    st.success(
                        f"Created license plate {license_plate['number']}",
                    )

        with read_plate_tab:
            st.header("Read License Plate")
            image_file = st.file_uploader("Upload an image of a license plate")

            if st.button("Read License Plate"):
                result = read_license_plate(
                    st.session_state["token"], image_file.getvalue())
                if result == "Wanted license plate detected":
                    st.error(result)
                else:
                    st.success(f"Read license plate {result['number']}")

else:
    create_plate_tab, read_plate_tab = st.tabs(
        ["Create License Plate", "Read License Plate"])

    with create_plate_tab:
        st.header("Create License Plate")
        license_plate_number = st.text_input("License Plate Number")
        license_plate_wanted = st.checkbox("Wanted")
        if st.button("Create License Plate"):
            if len(license_plate_number) <= 0:
                st.error("License plate number must not empty")
            else:
                license_plate = create_license_plate(
                    st.session_state["token"],
                    {
                        "number": license_plate_number,
                        "wanted": license_plate_wanted,
                    }
                )
                st.success(
                    f"Created license plate {license_plate['number']}",
                )

    with read_plate_tab:
        st.header("Read License Plate")
        image_file = st.file_uploader("Upload an image of a license plate")

        if st.button("Read License Plate"):
            results = read_license_plate(
                st.session_state["token"], image_file.getvalue())
            for result in results:
                if result["wanted"]:
                    st.error(f"Wanted license plate detected {result['number']}")
                else:
                    st.success(f"Read license plate {result['number']}")
