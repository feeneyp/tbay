from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

#this is the class for individual items sold on tbay
#contrary to appearances it is not the class for the table that lists the items
#the properties (id, name etc) are properties of Item objects
class Item(Base):  
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    bidsOnItem = relationship("Bid", backref="targetItem") 

    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    items_selling = relationship("Item", backref="seller")
    UserBids = relationship("Bid", backref="bidder")

    
class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    item_id = Column(Integer, ForeignKey("items.id"), nullable = False)
    

Base.metadata.create_all(engine)     
    
    
    
user1 = User(username="User One", password="123")
user2 = User(username="User Two", password="123")
user3 = User(username="User Three", password="123")
baseBall = Item(name="baseball", description="Dwight Gooden Autographed Baseball", seller=user1 )
bid1From1 = Bid(price=10, bidder=user1, targetItem=baseBall)
bid2From1 = Bid(price=11, bidder=user1, targetItem=baseBall)
bid1From2 = Bid(price=8, bidder=user2, targetItem=baseBall)
bid2From2 = Bid(price=9, bidder=user2, targetItem=baseBall)
bid1From3 = Bid(price=12, bidder=user3, targetItem=baseBall)
bid2From3 = Bid(price=13, bidder=user3, targetItem=baseBall)
session.add_all([user1,user2,user3,baseBall,bid1From1,bid2From1,bid1From2,bid2From2,bid1From3,bid2From3])
bids_list = session.query(Bid.price).order_by(Bid.price.desc()).all()
print bids_list[0]
session.commit()

   
    
   