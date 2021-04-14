address = ["alpha", "beta", "gamma", "delta"]
password = ["1234", "1234", "1234"]
salary = [10000, 20000]
role = ["student", "student", "faculty"]
unpaid_fines = [0.00,100.00]
data = []
if __name__ =="__main__":
  for i in range(0,6):
    query = "INSERT INTO user (user_id, name, role, password, unpaid_fines, address) VALUES "
    payload = "('%s', '%s', '%s', '%s', %0.2f, '%s');"%(str(i+1), "User"+str(i+1), role[i%3], password[i%3], unpaid_fines[i%2], address[i%4])
    query += (payload)
    print(query)