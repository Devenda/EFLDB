from datetime import date, datetime, timedelta
import mysql.connector
import pyxhook

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='ecofablab')
cursor = cnx.cursor(buffered=True)

while True: 
	member_id = str(input("Enter member_id: "))
	arrival_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
	qy_find_presence = "SELECT row_id FROM ecofablab.presence WHERE date(arrival_time) = '{}' AND departure_time IS NULL AND member_id = '{}'".format(datetime.now().strftime('%Y-%m-%d'), member_id)
	print(qy_find_presence)
	cursor.execute(qy_find_presence) 

	#set departure time when badging a second time on the same day
	qy_update_presence = ""
	if cursor.rowcount > 0:
		row_ids = cursor.fetchall()
		for row_id in row_ids:
			qy_update_presence = "UPDATE presence SET departure_time = '{}' where row_id = {};".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),row_id[0])
			print(qy_update_presence)
			cursor.execute(qy_update_presence)

		# Make sure data is committed to the database
		cnx.commit()
	else:
		qy_add_presence = "INSERT INTO presence (member_id, arrival_time) VALUES ('{}', '{}')".format(member_id, arrival_time)
		print(qy_add_presence)

		# Insert new presence
		cursor.execute(qy_add_presence)
		print(cursor.lastrowid)
	
		# Make sure data is committed to the database
		cnx.commit()
hookman.cancel()
cursor.close()
cnx.close()
