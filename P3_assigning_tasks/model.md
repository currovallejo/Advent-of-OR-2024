$$
\begin{aligned}
\text{Minimize} & \quad C \\[1em]
\text{Subject to} & \quad \sum_{j \in T} x_{ij} = 1, \quad \forall i \in E\\[1em]
& \quad \sum_{i \in E} x_{ij} = 1, \quad \forall j \in T \\[1em]
& \quad C = \sum_{i \in E} \sum_{j \in T} c_{ij} \cdot x_{ij} \\[1em]
& \quad c_{ij} = \text{Cost of assigning employee } i \text{ to task } j \\[1em]
& \quad x_{ij} \in \{0, 1\}, \quad \forall i \in \text{Employees}, \forall j \in \text{Tasks} \\[1em]
\end{aligned}
$$
