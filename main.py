from flask import Flask,request
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import pymssql
import json
from flask import Response


import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)

class Schedule(Resource):
    
    #sch_list.append({'time': "sdf"})

    def get(self):
        group_name = request.args.get('group')
        #group_name = request.args.get('group', default='ИСТР-ИП-21')
        
        sch_list = self.load_data(group_name)  # Загружаем данные только для текущего запроса
        return sch_list

    def load_data(self,g):
        sch_list = [] 
        try:
            conn = pymssql.connect(server="localhost", user="levin", password="123", database="institut", charset='utf8')
            print(g.encode('cp1251'))
            cursor = conn.cursor(as_dict=True)
            
            cursor.execute("""SELECT g."name" as "group", t.tiime as "time", d."name"as "day", r."name"as room, par.num as para, p."name" as prep 
FROM schedule as s 
JOIN GROOUP as g ON s.GROOUP_id=g.id 

JOIN tiimes as t ON s.time_id=t.id 
JOIN rooms as r ON s.room_id=r.id 
JOIN prepodi as p ON s.prepod_id=p.id 
JOIN subjects as par ON s.para_id=par.id 
JOIN "days" as d ON s.day_id=d.id 

WHERE g."name" = '"""+g+"'")
            
            

        # Если данные есть в курсоре, выведите их для проверки
            results = list(cursor)
            if results:
                
                for row in results:
                    time = row['time'].encode('latin1').decode('windows-1251')
                    day = row['day'].encode('latin1').decode('windows-1251')
                    room = row['room'].encode('latin1').decode('windows-1251')
                    para = row['para'].encode('latin1').decode('windows-1251')
                    prep = row['prep'].encode('latin1').decode('windows-1251')
                    #prep = row['name'].encode('latin1').decode('windows-1251')
                    sch_list.append({'time': time,'day': day,'room': room, 'para': para, 'prep': prep})
                    #self.sch_list.append({'time': prep})
                return sch_list
            else:
                print("Нет данных для вывода")
        except Exception as e:
            print(f"\nERROR: {str(e)}")
        finally:
            conn.close()
        
                





class Group(Resource):
    
    #sch_list.append({'time': "sdf"})

    def get(self):
        #group_name = request.args.get('group')
        #group_name = request.args.get('group', default='ИСТР-ИП-21')
        
        gr_list = self.load_data()  # Загружаем данные только для текущего запроса
        return gr_list

    def load_data(self):
        gr_list = [] 
        try:
            conn = pymssql.connect(server="localhost", user="levin", password="123", database="institut", charset='utf8')
     
            cursor = conn.cursor(as_dict=True)
            
            cursor.execute("""SELECT * FROM  GROOUP ORDER BY "name";""")
            
            

        # Если данные есть в курсоре, выведите их для проверки
            results = list(cursor)
            if results:
                
                for row in results:
                    id = row['id']
                    gr = row['name'].encode('latin1').decode('windows-1251')
 
                    #prep = row['name'].encode('latin1').decode('windows-1251')
                    gr_list.append({'id': id,'name': gr})
                    #self.sch_list.append({'time': prep})
                return gr_list
            else:
                print("Нет данных для вывода")
        except Exception as e:
            print(f"\nERROR: {str(e)}")
        finally:
            conn.close()



class Prep(Resource):
    
    #sch_list.append({'time': "sdf"})

    def get(self):
        #group_name = request.args.get('group')
        #group_name = request.args.get('group', default='ИСТР-ИП-21')
        
        pr_list = self.load_data()  # Загружаем данные только для текущего запроса
        return pr_list

    def load_data(self):
        pr_list = [] 
        try:
            conn = pymssql.connect(server="localhost", user="levin", password="123", database="institut", charset='utf8')
     
            cursor = conn.cursor(as_dict=True)
            
            cursor.execute("""SELECT * FROM  prepodi ORDER BY "name" ;""")
            
            

        # Если данные есть в курсоре, выведите их для проверки
            results = list(cursor)
            if results:
                
                for row in results:
                    id = row['id']
                    gr = row['name'].encode('latin1').decode('windows-1251')
 
                    #prep = row['name'].encode('latin1').decode('windows-1251')
                    pr_list.append({'id': id,'name': gr})
                    #self.sch_list.append({'time': prep})
                return pr_list
            else:
                print("Нет данных для вывода")
        except Exception as e:
            print(f"\nERROR: {str(e)}")
        finally:
            conn.close()


api.add_resource(Schedule, '/schedule')
api.add_resource(Prep, '/prep')
api.add_resource(Group, '/group')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
