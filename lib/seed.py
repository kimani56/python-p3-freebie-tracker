#!/usr/bin/env python3

#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()

    fake = Faker()

    years = [2000, 2001, 2002, 2003, 2004, 2005]

    companies = []
    for i in range(10):
        company = Company(
            name=fake.unique.name(),
            founding_year=random.choice(years),
        )

        # add and commit individually to get IDs back
        session.add(company)
        session.commit()

        companies.append(company)

    devs = []
    for i in range(10):
        dev = Dev(
            name=fake.unique.name(),
        )

        # add and commit individually to get IDs back
        session.add(dev)
        session.commit()

        devs.append(dev)

    freebies = []
    for company in companies:
        for i in range(random.randint(1,5)):
            
            freebie = Freebie(
                item_name= fake.unique.name(),
                value = random.randint(5, 100),
                company_id=company.id,
                dev_id = devs[i].id
            )

            freebies.append(freebie)

    session.bulk_save_objects(freebies)
    session.commit()
    session.close()