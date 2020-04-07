import persistqueue
q = persistqueue.SQLiteQueue('run-switch', auto_commit=True)
q.put("ID=1234,switch off\r\n")
q.put("ID=1235,switch off\r\n")
q.put("ID=1236,switch on\r\n")
q.put("ID=1237,switch off\r\n")

