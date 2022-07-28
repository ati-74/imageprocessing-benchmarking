import pickle

fname = 'examples/SingleStrain/InputFile/step-8.pickle'
data = pickle.load(open(fname,'rb'))

cs = data['cellStates']
print(cs.iloc[10])
print(data["lineage"])
