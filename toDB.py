import pandas as pd 
from sqlalchemy import create_engine

DATABASE = create_engine('sqlite:////Users/kevinkoh/Desktop/CrossCheck/cc.db')

def add_to_db(schedule):

	df = pd.DataFrame(schedule)
	df.to_sql('assignments', DATABASE, if_exists = 'append', index = False)
	print("done")
