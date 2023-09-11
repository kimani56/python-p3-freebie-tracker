from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from connect import session

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', backref=backref('company'))
    devs = relationship("Dev", secondary="freebies", back_populates="companies")

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(
            item_name=item_name, 
            value=value,
            company_id = self.id,
            dev_id = dev.id
        )
        session.add(freebie)
        session.commit()

    @classmethod
    def oldest_company(cls):
        company = session.query(cls).order_by(cls.founding_year).first()
        return company

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', backref=backref('dev'))
    companies = relationship("Company", secondary="freebies", back_populates="devs")

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev == dev
            session.commit()
        

    @classmethod
    def received_one(cls, item_name):
        dev = session.query(cls).filter_by(name=item_name).first()
        if dev:
            return True
        else:
            return False

    def __repr__(self):
        return f'<Dev {self.name}>'
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    # company = relationship('Company', back_populates='freebies')
    # dev = relationship('Dev', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):

        return f'Freebie(id={self.id})'