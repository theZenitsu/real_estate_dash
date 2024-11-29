from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

# Load database URL (use st.secrets for Streamlit Cloud)
DATABASE_URL = st.secrets["real_estate"]["url"]  # Use this for Streamlit secrets
# DATABASE_URL = "postgresql://postgres:anass@localhost:5432/real_estate"  # Hardcoded alternative

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
