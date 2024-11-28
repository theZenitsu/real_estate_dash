from faker import Faker
from database import SessionLocal
from models import Ville, Equipement, Annonce

def populate_data():
    fake = Faker()
    session = SessionLocal()

    # Add unique cities
    cities = ["Casablanca", "Rabat", "Marrakech", "Tangier", "Agadir"]
    for city_name in cities:
        if not session.query(Ville).filter_by(name=city_name).first():
            session.add(Ville(name=city_name))
    session.commit()

    # Add unique equipment
    equipments = ["Balcony", "Elevator", "Garage", "Swimming Pool", "Garden"]
    for equipment_name in equipments:
        if not session.query(Equipement).filter_by(name=equipment_name).first():
            session.add(Equipement(name=equipment_name))
    session.commit()

    # Add announcements
    for _ in range(100):
        annonce = Annonce(
            title=fake.sentence(),
            price=fake.random_int(100000, 1000000),
            datetime=fake.date_time_this_year(),
            nb_rooms=fake.random_int(1, 10),
            nb_baths=fake.random_int(1, 5),
            surface_area=fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=50, max_value=500),
            link=fake.url(),
            city_id=fake.random_int(1, len(cities))
        )
        session.add(annonce)

    session.commit()
    session.close()

if __name__ == "__main__":
    populate_data()
