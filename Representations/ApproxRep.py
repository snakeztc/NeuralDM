import numpy as np
from Representation import Representation



class ApproxRep(Representation):

    state_feature_base = None

    def __init__(self, domain, seed=1):
        super(ApproxRep, self).__init__(domain, seed)
        # initialize the model
        self.model = None
        self.state_features_num = 0
        for idx, type in enumerate(self.domain.statespace_type):
            if type == self.domain.categorical:
                self.state_features_num += (self.domain.statespace_limits[idx, 1] - self.domain.statespace_limits[idx, 0])
            else:
                self.state_features_num += 1
        self.state_features_num += domain.actions_num
        self.state_features_num = int(self.state_features_num)

    def phi_sa(self, s, aID):
        """
        Get the feature vector for a subtask o at state s with action u
        :param s: the raw state vector
        :param aID: the action index
        :return: the feature vector
        """
        # feature vector
        #phi = self.phi_s(s)
        #phi_sa = np.column_stack((phi, aID))
        #return phi_sa

        """
        phi = self.phi_s(s)
        phi_sa = np.zeros((phi.shape[0], phi.shape[1] * self.actions_num))
        #phi_sa = np.column_stack((phi, aID))
        for idx in range(0, self.actions_num):
            mask = np.where(aID == idx)
            phi_sa[mask, idx*phi.shape[1]:(idx+1)*phi.shape[1]] = phi[mask, :]
        return phi_sa
        """
        phi_s = self.phi_s(s)
        phi_a = np.zeros((phi_s.shape[0], self.domain.actions_num))
        for idx in range(0, self.domain.actions_num):
            mask = np.where(aID == idx)
            phi_a[mask, idx] = 1
        phi_sa = np.column_stack((phi_s, phi_a))
        return phi_sa


    def phi_s(self, s):
        phi = np.copy(s)
        temp_phi = phi[:, 0:-2]
        temp_phi[temp_phi > 1] = 2
        phi[:, 0:-2] = temp_phi
        return self.expand_state_space(phi, self.domain.statespace_limits, self.domain.statespace_type)


    def Q(self, s, aID):
        phi_sa = self.phi_sa(s, aID)
        if self.model:
            q = self.model.predict(phi_sa).ravel()
        else:
            q = np.zeros(s.shape[0])
        return q

    def Qs(self, s):
        qs = np.zeros((s.shape[0], self.domain.actions_num))
        actions = self.domain.possible_actions()
        for idx, aID in enumerate(actions):
            temp_aIDs = np.ones((s.shape[0], 1)) * aID
            qs[:, idx] = self.Q(s, temp_aIDs)
        return qs




