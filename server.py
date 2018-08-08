from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'CDAP'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/CDAP'

mongo = PyMongo(app)
#doctor route start
@app.route('/arimaPost/', methods=['POST'])
def addArimaModelPost():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
#        result =  mongo.db.arimaPost.insert_one(data).inserted_id
        mongo.db.arimaPost.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'})
    else:
        return jsonify({'error': True, 'message': 'error'})

@app.route('/arima/', methods=['POST'])
def addArimaModel():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.arima.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'})


@app.route('/doctors/', methods=['GET'])
def getDoctor():
  doctors = mongo.db.doctors
  output = []
  for s in doctors.find():
    output.append({'id':s['id'],'NIC':s['NIC'],'name' : s['name'], 'ward' : s['ward'],'assingDate':s['assingDate'],'doctorType':s['doctorType']})
  return jsonify(output)

@app.route('/doctors/', methods=['POST'])
def addDoctor():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.doctors.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'})

@app.route('/doctors/', methods=['DELETE'])
def deleteDoctor():
    data = request.get_json()
    db_response = mongo.db.doctors.delete_one({'id': data['id']})
    if db_response.deleted_count == 1:
        response = {'ok': True, 'message': 'record deleted'}
    else:
        response = {'ok': True, 'message': 'no record found'}
    return jsonify(response), 200
@app.route('/doctors/', methods=['PATCH'])
def updateDoctor():
    data1 = request.get_json()
    data = mongo.db.doctors
    result = mongo.db.doctors.update({"id":data1['id']},{'$set':{'name':data1['name'],'ward':data1['ward'],'assingDate':data1['assingDate'],'doctorType':data1['doctorType']}})
    response = {'ok': True, 'message': 'record updated'}
#    print data.find_one({'ID':100})
    return jsonify(response), 200
#doctor route end

#patient route start
@app.route('/patients/', methods=['GET'])
def getPatient():
  patients = mongo.db.patients
  output = []
  for s in patients.find():
    output.append({'id':s['id'],'NIC':s['NIC'],'name' : s['name'], 'gender':s['gender'],'distric':s['distric'],'date':s['date'],'level':s['level'],'ward' : s['ward'],'wardChanges':s['wardChanges'], 'priority' : s['priority'],'comments':s['comments']})
  return jsonify(output)

@app.route('/patients/', methods=['POST'])
def addPatient():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.patients.insert_one(data)
        return jsonify({'ok': True, 'message': 'Patient created successfully!'})

@app.route('/patients/', methods=['DELETE'])
def deletePatient():
    data = request.get_json()
    db_response = mongo.db.patients.delete_one({'id': data['id']})
    if db_response.deleted_count == 1:
        response = {'ok': True, 'message': 'record deleted'}
    else:
        response = {'ok': True, 'message': 'no record found'}
    return jsonify(response), 200
@app.route('/patients/', methods=['PATCH'])
def updatePatient():
    data1 = request.get_json()
    result = mongo.db.patients.update({"id":data1['id']},{'$set':{'NIC':data1['NIC'],'name' : data1['name'], 'gender':data1['gender'],'distric':data1['distric'],'date':data1['date'],'level':data1['level'],'ward' : data1['ward'], 'wardChanges':data1['wardChanges'],'priority' : data1['priority'],'comments':data1['comments']}})
    response = {'ok': True, 'message': 'record updated'}
#    print data.find_one({'ID':100})
    return jsonify(response), 200
#patient route end



@app.route('/adminLogic/', methods=['PATCH'])
def updateAdminLogic():
    data1 = request.get_json()
    result = mongo.db.adminLogic.update({"name":data1['name']},{'$set':{'status':data1['status']}})
    response = {'ok': True, 'message': 'record updated'}
#    print data.find_one({'ID':100})
    return jsonify(response), 200

@app.route('/adminLogic/', methods=['POST'])
def updateAdminLogic2():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.adminLogic.insert_one(data)
        return jsonify({'ok': True, 'message': 'adminLogic updated successfully!'})

@app.route('/adminLogic/', methods=['GET'])
def getAdminLogic():
  records = mongo.db.adminLogic
  output = []
  for s in records.find():
    output.append({'name':s['name'],'type':s['type'],'status' : s['status']})
  return jsonify(output)

@app.route('/adminRecords/', methods=['POST'])
def updateAdminRecords():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.adminRecords.insert_one(data)
        return jsonify({'ok': True, 'message': 'adminRecords updated successfully!'})
    
@app.route('/adminRecords/', methods=['GET'])
def getAdminRecords():
  records = mongo.db.adminRecords
  print(records)
  output = []
  for s in records.find():
    output.append({'ward':s['ward'],'capacity':s['capacity'],'perNurse' : s['perNurse'],'shifts' : s['shifts'],'priority' : s['priority']})
  return jsonify(output)

@app.route('/leaveArray/', methods=['POST'])
def leavePost():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.leaveTable.insert_one(data)
        return jsonify({'ok': True, 'message': 'adminRecords updated successfully!'})
    
@app.route('/leaveArray/', methods=['GET'])
def leaveGet():
  records = mongo.db.leaveTable
  print(len(records))
  output = []
  for s in records.find():
      for a in s['leave']:
          for b in a:
              print(b)
              output.append({'leave':b})
  return jsonify(output)



if __name__ == '__main__':  
    app.run(host= '0.0.0.0')
    
