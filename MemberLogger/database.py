from datetime import date, datetime, timedelta
import mysql.connector

class database():

     cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='ecofablab')
     cursor = cnx.cursor(buffered=True)

     def justCheckedIn(self, memberId):
         qy_present = "SELECT COUNT(*) FROM ecofablab.presence WHERE arrival_time > DATE_SUB(NOW(), INTERVAL 1 MINUTE) AND member_id = '{}'".format(memberId)
         self.cursor.execute(qy_present)
         presence = self.cursor.fetchone()
         if presence[0] > 0:
             print(str(memberId) + " has already checked in")
             return True
         else:
             print(str(memberId) + " has NOT checked in")
             return False            

     def isMember(self, memberId):
         qy_find_member = "SELECT COUNT(*) FROM ecofablab.member WHERE member_id = '{}'".format(memberId)
         self.cursor.execute(qy_find_member)
         member = self.cursor.fetchone()
         if member[0] > 0:
            print(str(memberId) + " is a member")
            return True
         else:
            print(str(memberId) + " is NOT a member")
            return False

     def writePresence(self, memberId):
         if self.justCheckedIn(memberId):
            print("Member " + str(memberId) + " has already checked in, will do nothing")
         else:
            arrival_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            qy_find_presence = "SELECT row_id FROM ecofablab.presence WHERE date(arrival_time) = '{}' AND departure_time IS NULL AND member_id = '{}'".format(datetime.now().strftime('%Y-%m-%d'), memberId)
            print("Searching for presence of: " + str(memberId))
            self.cursor.execute(qy_find_presence) 

            #set departure time when badging a second time on the
            #same day
            qy_update_presence = ""
            if self.cursor.rowcount > 0:
                row_ids = self.cursor.fetchall()
                for row_id in row_ids:
                    qy_update_presence = "UPDATE presence SET departure_time = '{}' where row_id = {};".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),row_id[0])
                    print("Presence found of: " + str(memberId))
                    self.cursor.execute(qy_update_presence)

                # Make sure data is committed to the database
                self.cnx.commit()
            #new presence
            elif self.isMember(memberId):
                qy_add_presence = "INSERT INTO presence (member_id, arrival_time) VALUES ('{}', '{}')".format(memberId, arrival_time)
                print("Adding presence for: " + str(memberId))

                # Insert new presence
                self.cursor.execute(qy_add_presence)
         
                # Make sure data is committed to the database
                self.cnx.commit()
                print("Insert done with row_id: " + str(self.cursor.lastrowid))
                #self.cursor.close()
                #self.cnx.close()
            else:
                print(str(memberId) + " is NOT a member and will not be added to the presence tabel")