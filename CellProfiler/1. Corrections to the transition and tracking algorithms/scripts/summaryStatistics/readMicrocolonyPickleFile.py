import pickle

fname = "output/pickle/step-50.pickle"
data = pickle.load(open(fname, "rb"))

microcolony = data["microcolonyStates"]
print("StepNum:" + str(data["stepNum"]))
print("numMicrocolonies:" + str(data["numMicrocolonies"]))
print("microcolonies: ")
print(microcolony)
