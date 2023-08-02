import subprocess
import os

class RunCode(object):
    def __init__(self, typecode, template, code=None):
        self.code = code
        self.typecode=typecode
        self.template = template
        self.stderr = None
        self.output_list = []
        if not os.path.exists('static/code'):
            os.mkdir('static/code')

    def executeC(self):    
        
        s = subprocess.check_output("gcc HelloWorld.c -o out1", shell = True,cwd="static/code", stderr=subprocess.PIPE)
        s = subprocess.check_output("out1", shell = True,cwd="static/code", stderr=subprocess.PIPE)
        print("return code", s)
    
    def executeCpp(self,input):
    
        try:
            output = subprocess.check_output("g++ code.cpp -o out2", shell = True,cwd="static/code", stderr=subprocess.STDOUT)

            lines = input.split("\n")
            for line in lines:
                data, temp = os.pipe()
                os.write(temp, bytes(line, "utf-8"));
                os.close(temp)
    
                p = subprocess.check_output('out2', timeout=5.5, stdin = data,cwd="static/code",shell=True, stderr=subprocess.PIPE)
                self.output_list.append(p.decode("utf-8"))
            self.stderr=None
        except subprocess.CalledProcessError as e:
             self.stderr= e.output.decode()
        except subprocess.TimeoutExpired as e:
            self.stderr = e.output.decode()
        except Exception as e:
            # check_call can raise other exceptions, such as FileNotFoundError
            self.stderr = str(e)
    
    def executeJava(self,input):
        try:
            output = subprocess.check_output("javac Code.java", shell = True,cwd="static/code", stderr=subprocess.STDOUT).decode()

            lines = input.split("\n")
            for line in lines:
                data, temp = os.pipe()
                os.write(temp, bytes(line, "utf-8"));
                os.close(temp)
    
                p = subprocess.check_output("java Code", timeout=5.5, stdin = data,shell = True,cwd="static/code", stderr=subprocess.PIPE)
                self.output_list.append(p.decode("utf-8"))
            self.stderr=None
        except subprocess.CalledProcessError as e:
             self.stderr= e.output.decode()
        except subprocess.TimeoutExpired as e:
            self.stderr = e.output.decode()
        except Exception as e:
            # check_call can raise other exceptions, such as FileNotFoundError
            self.stderr = str(e)

    def executePython(self,input):
        try:
            lines = input.split("\n")
            for line in lines:
                data, temp = os.pipe()
                os.write(temp, bytes(line, "utf-8"));
                os.close(temp)
    
                p = subprocess.check_output("python code.py", timeout=5.5, stdin=data, shell = True,cwd="static/code", stderr=subprocess.STDOUT)
                self.output_list.append(p.decode("utf-8"))
            self.stderr=None
        except subprocess.CalledProcessError as e:
             self.stderr= e.output.decode()
        except subprocess.TimeoutExpired as e:
            self.stderr = e.output.decode()
        except Exception as e:
            # check_call can raise other exceptions, such as FileNotFoundError
            self.stderr = str(e)

    def writecode(self, filename, code=None):
        if not code:
            code = self.code
        open(filename,"w").close()
        with open(filename, "a") as f,open(self.template,'r') as temp:
            lines = temp.readlines()
            for line in lines:
                if "Write your function here" in line:
                    f.write(code)
                else:
                    f.write(line)
            
    def run_code(self, input):
        
        if self.typecode == "C++":
            filename = "static/code/code.cpp"
            self.writecode(filename,self.code)
            self.executeCpp(input)
        elif self.typecode == "Java":
            filename = "static/code/Code.java"
            self.writecode(filename,self.code)
            self.executeJava(input)
        elif self.typecode == "Python":
            filename = "static/code/code.py"
            self.writecode(filename,self.code)
            self.executePython(input)
        return self.stderr, self.output_list