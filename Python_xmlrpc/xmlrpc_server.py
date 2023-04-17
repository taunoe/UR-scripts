# main program
# Link: https://www.universal-robots.com/articles/ur/interface-communication/xml-rpc-communication/
# pip install pypi-xmlrpc
import sys
from xmlrpc.server import SimpleXMLRPCServer


# Returns dictionary
def list_to_pose(l):
  assert type(l) is list
  return {'x' : l[0], 'y' : l[1], 'z' : l[2], 'rx' : l[3], 'ry' : l[4], 'rz' : l[5]}

# Returns list
def pose_to_list(p):
  assert type(p) is dict
  return [p['x'], p['y'], p['z'], p['rx'], p['ry'], p['rz']]

def epsilonEquals(a, b):
  if(type(a) is dict):
    a = pose_to_list(a)
  elif(type(a) is int or type(a) is float):
    a = [a]
  if(type(b) is dict):
    b = pose_to_list(b)
  elif(type(b) is int or type(b) is float):
    b = [b]
  if(len(a) != len(b)):
    return False

  for i in range(0,len(a)):
    if(abs(a[i] - b[i]) > 1E-06):
      return False
  return True



# indexid
x  = 0
y  = 1
z  = 2
rx = 3
ry = 4
rz = 5

# Pose = [x, y, z, rx, ry, rz]
pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
edasi = True


def get_next_pose(p):
  assert type(p) is dict
  old_pose = pose_to_list(p)
  print("Roboti pose: " + str(old_pose))

  pose = old_pose
  global edasi

  if pose[x] <= -0.465:
    edasi = False
  
  if pose[x] >= 0.47:
    edasi = True

  if edasi == True:
    pose[x] -= 0.01
  else:
    pose[x] += 0.01

  print("Arvuti pose: " + str(pose))
  return list_to_pose(pose)


def main():
  server = SimpleXMLRPCServer(("", 50000), allow_none=True)
  server.RequestHandlerClass.protocol_version = "HTTP/1.1"
  print("Listening ...")

  server.register_function(get_next_pose, "get_next_pose")

  server.serve_forever()


if __name__ == "__main__":
    main()
    