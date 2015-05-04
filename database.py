
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
#### class code #######
class Restaurant(Base):
	__tablename__ = 'restaurant' # names table
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
