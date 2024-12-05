$$
\begin{aligned}
\text{Maximize} & \quad \sum_{c \in C} \sum_{t \in T} \sum_{r \in R} \sum_{p \in P} x_{c, t, r, p} \\[1em]
\text{Subject to:} & \\[1em]
(1) & \quad \sum_{p \in P} x_{c, t, r, p} = f[c][t][r], \quad \forall c \in C, \forall t \in T, \forall r \in R \\[1em]
(2) & \quad \sum_{c \in C} \sum_{r \in R} x_{c, t, r, p} \leq 1, \quad \forall t \in T, \forall p \in P \\[1em]
(3) & \quad \sum_{t \in T} \sum_{r \in R} x_{c, t, r, p} \leq 1, \quad \forall c \in C, \forall p \in P \\[1em]
(4) & \quad x_{c, t, r, p} \in \{0, 1\}, \quad \forall c \in C, \forall t \in T, \forall r \in R, \forall p \in P \\[1em]
\end{aligned}
$$