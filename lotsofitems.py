from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalogitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Nico Ianosi", email="nicoianosi@home.com",
             picture='https://pixabay.com/static/uploads/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')
session.add(User1)
session.commit()

# Items for Soccer
category1 = Category(user_id=1, name="Soccer", description="Soccer description")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Two shinguards", description="Two shinguards description",
                      category=category1)

session.add(item1)
session.commit()


item2 = Item(user_id=1, name="Jersey", description="Jersey description",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Soccer Cleats", description="Soccer Cleats description",
                     category=category1)

session.add(item3)
session.commit()



# Items for Basketball
category2 = Category(user_id=1, name="Basketball", description="Basketball Description")

session.add(category2)
session.commit()


item1 = Item(user_id=1, name="Slam Dunk", description="Slam Dunk description",
                      category=category2)

session.add(item1)
session.commit()


item2 = Item(user_id=1, name="Free Throw", description="Free throw description",
                     category=category2)

session.add(item2)
session.commit()


# Items for Snowboarding
category3 = Category(user_id=1, name="Snowboarding", description="Snowboarding Description")

session.add(category3)
session.commit()


item1 = Item(user_id=1, name="Googles", description="Googles description",
                      category=category3)

session.add(item1)
session.commit()


item2 = Item(user_id=1, name="Snowboard", description="Snowboard description",
                     category=category3)

session.add(item2)
session.commit()


# Items for Tennis
category4 = Category(user_id=1, name="Tennis", description="Tennis Description")

session.add(category4)
session.commit()


item1 = Item(user_id=1, name="Break", description="Break description",
                      category=category4)

session.add(item1)
session.commit()


item2 = Item(user_id=1, name="Ball boy", description="Ball boy description",
                     category=category4)

session.add(item2)
session.commit()




print "added catalog items!"