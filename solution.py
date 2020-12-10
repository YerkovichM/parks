from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        text = self.read_input()
        partSize = len(text) / len(self.workers) + 1

        # map
        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(text[i * partSize:i * partSize + partSize]))

        print('Map finished: ', mapped)

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + reduced)

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(text):
        res = [(char, chr(ord(char) + 3))[48 <= ord(char) <= 122] for char in list(text)]
        return ''.join(res)

    @staticmethod
    @expose
    def myreduce(mapped):
        output = ''
        for x in mapped:
            output += x.value
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        input = f.read()
        f.close()
        return input

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(output)
        f.write('\n')
        f.close()
