from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import streamlit as st

DATABASE_URL = "postgresql://postgres:anass@localhost:5432/real_estate"

load_dotenv()  # Load .env file
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = st.secrets["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

import streamlit as st

"""from sqlalchemy import create_engine

# Use Streamlit Secrets
DATABASE_URL = st.secrets["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
"""