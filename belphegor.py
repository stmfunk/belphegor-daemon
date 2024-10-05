# Standard Python modules.
import os               # Miscellaneous OS interfaces.
import sys              # System-specific parameters and functions.
import time

# Watchdog
from watchdog.observers     import Observer
from watchdog.events        import FileSystemEventHandler

# The standard I/O file descriptors are redirected to /dev/null by default.
if (hasattr(os, "devnull")):
   REDIRECT_TO = os.devnull
else:
   REDIRECT_TO = "/dev/null"


class ObsidianHandler(FileSystemEventHandler):
   pass

class Belphegord:
   def task(self):
      log = open("log.txt","w") 
      while True:
         log.write("Executed\n")
         log.flush()
         time.sleep(2)
         continue

def createDaemon():
   try:
      pid = os.fork()
   except OSError as e:
      raise Exception("%s [%d]" % (e.strerror, e.errno))

   if (pid == 0):   # The first child.
      os.setsid()

      try:
         pid = os.fork()    # Fork a second child.
      except OSError as e:
         raise Exception("%s [%d]" % (e.strerror, e.errno))

      if (pid != 0):    # The second child.
         os._exit(0)    # Exit parent (the first child) of the second child.
   else:
      os._exit(0)   # Exit parent of the first child.

   belphegord = Belphegord()
   belphegord.task()

if __name__ == "__main__":

   retCode = createDaemon()

   sys.exit(retCode)
