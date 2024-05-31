import json
from Lock import Lock

class LockController:
    def __init__(self, lock_array):
        self.locks = lock_array

    def openAll(self):
        for lock in self.locks:
            lock.open()

        json_data = json.dumps(
            [{'doorLock_Id': lock.lock_id, 'system_Id': "1", 'isOn': lock.isOpen} for lock in self.locks])

        return json_data

    def closeAll(self):
        for lock in self.locks:
            lock.close()

        json_data = json.dumps(
            [{'doorLock_Id': lock.lock_id, 'system_Id': "1", 'isOn': lock.isOpen} for lock in self.locks])

        return json_data

    def open(self, lock_id):
        lock = self.locks[lock_id]
        lock.open()

        json_data = json.dumps({'doorLock_Id': lock.lock_id, 'system_Id': "1", 'isOn': lock.isOpen})

        return json_data

    def close(self, lock_id):
        lock = self.locks[lock_id]
        lock.close()

        json_data = json.dumps({'doorLock_Id': lock.lock_id, 'system_Id': "1", 'isOn': lock.isOpen})

        return json_data

    def getStates(self):
        json_data = json.dumps(
            [{'doorLock_Id': str(lock.lock_id), 'system_Id': "1", 'isOn': lock.isOpen} for lock in self.locks])

        return json_data

    def getState(self, lock_id):
        global isServoOn
        if lock_id >= len(self.locks) or lock_id < 0:
            return json.dumps({'message': "Record not found"}), 400
        lock = self.locks[lock_id]
        json_data = json.dumps({'doorLock_Id': str(lock_id), 'system_Id': "1", 'isOn': lock.isOpen})

        return json_data
