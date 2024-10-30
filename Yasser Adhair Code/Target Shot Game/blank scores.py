import pickle
scores = []
for i in range(0,10):
    temp = []
    temp.append('N/A')
    temp.append('0')
    scores.append(temp)

with open('high_scores.pkl', 'wb') as file:
    pickle.dump(scores,file)

print('Done')