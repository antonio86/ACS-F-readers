__author__ = 'antonioridi'

from sklearn import mixture
from reader_acsf import *

# Example using the readers and the GMM
# The reader is placed at the same level of the ACS-F database.
# in this case we used the 'ACS-F2'

directory = os.getcwd() + '/ACS-F2'
#(list_data, list_name, list_session, list_model, nModels) = reader_acsf_mat(directory)
(list_data, list_name, list_session, list_model, nModels) = reader_acsf_xml(directory)

list_data = np.array(list_data)
list_session = np.array(list_session)
list_model = np.array(list_model)

# Intersession protocol:
# session 1 in the train, session 2 in the test
list_data_train = list_data[list_session == 1]
list_model_train = list_model[list_session == 1]
Test_data = list_data[list_session == 2]
Test_label = list_model[list_session == 2]
Train_label = []
Train_data = np.vstack(list_data_train)
for i in range(0,len(list_data_train)):
    Train_label.append(np.repeat(list_model_train[i],len(list_data_train[i])))
Train_label = np.hstack(Train_label)

# Training: 40 Gaussians per model
n_comp = 40
Acc_rate = []
np.random.seed(n_comp)
gauss_vect = []
for j in range(0,nModels):
    g = mixture.GMM(n_components=n_comp)
    list_j = [i for i, cnt in enumerate(Train_label) if cnt == j]
    g.fit(Train_data[list_j],Train_label[list_j])
    gauss_vect.append(g)

# Testing: each time series is classified and the log-scores are added
Conf_mat = np.zeros([nModels,nModels])
for i in range(0,len(Test_data)):
    class_score = []
    for j in range(0,nModels):
        class_score.append(np.sum(gauss_vect[j].score(Test_data[i])))
    pos_win = class_score.index(max(class_score))
    Conf_mat[pos_win][Test_label[i]] += 1
Acc_rate = np.trace(Conf_mat)/np.sum(np.sum(Conf_mat))

# Print the confusion matrix and the accuracy rate
print(Conf_mat)
print(Acc_rate)