        def policy_iteration(P, R, gamma, n_iter):
            pi_prev = np.zeros(P.shape[0],dtype='i')
                        
            for i in range(n_iter):
                vpi = compute_vpi(pi_prev, P, R, gamma)
                qpi = compute_qpi(vpi, pi_prev, P, R, gamma)
                pi = qpi.argmax(axis=1)
                pi_prev = pi
                print pi
        
        policy_iteration(P, R, gamma, 10)

        def compute_vpi(pi, P, R, gamma):
            nS = P.shape[0]
            Ppi = P[np.arange(nS), pi]
            Rpi = R[np.arange(nS), pi]
            b = np.sum(Ppi * Rpi, axis=1)
            a = np.eye(nS) - gamma * Ppi
            vpi = np.linalg.solve(a, b)

            return vpi

        pi0 = np.zeros(nS,dtype='i')

        def compute_qpi(vpi, pi, P, R, gamma):
       
            nS = P.shape[0]
            nA = P.shape[1]
            qpi = np.sum(P * (R + gamma * vpi.reshape((1, 1, -1))), axis=2)
            assert qpi.shape == (nS, nA)
            return qpi

             qValuesTable = []

        nS = 64
        nA = 3

        P = np.random.rand(nS, nA, nS)
        R = np.random.rand(nS, nA, nS)
        P /= P.sum(axis = 2, keepdims = True)
        
        gamma = 0.90

        def vstar_backup(v_n, P_pan, R_pan, gamma):
  
            nS = P_pan.shape[0] # number of states
            q_sa = np.sum(P_pan * R_pan + gamma * (P_pan * np.reshape(v_n, (1, 1, -1))), axis=2)
            v_p = np.max(q_sa, axis=1)
            a_p = np.argmax(q_sa, axis=1)

            return (v_p, a_p)

        Vprev = np.zeros(nS)
        Aprev = None
        chg_actions_seq = []
    
        for i in range(10):
            V, A = vstar_backup(Vprev, P, R, gamma)
            chg_actions = "N/A" if Aprev is None else (A != Aprev).sum()
            chg_actions_seq.append(chg_actions)
            
            Vprev, Aprev = V, A
        # print chg_actions_seq



               def learnQ(self, state, action, reward, value):
            oldv = self.q.get((state, action), None)
            if oldv is None:
                self.q[(state, action)] = reward
            else:
                self.q[(state, action)] = oldv + self.alpha * (value - oldv)

        def learn(self, state1, action1, reward, state2):
            maxqnew = max([self.getQ(state2, a) for a in self.actions])
            self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)


        def chooseAction(self, state):
            if random.random() < self.epsilon:
                action = random.choice(self.actions)
            else:
                q = [self.q.get((state, action), 0.0) for a in self.actions]
                maxQ = max(q)
                count = q.count(maxQ)
                if count > 1:
                    best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                    i = random.choice(best)
                else:
                    i = q.index(maxQ)

                action = self.actions[i]
            return action
        
        chooseAction(self, self.random_start_state)