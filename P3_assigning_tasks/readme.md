# Assigning Tasks

## Problem

Hey, ORville here 👋

I'm a logistics manager overseeing the allocation of tasks to employees in our company, FurnitORe.

Right now we have 100 tasks that need to be completed, and we also have 100 employees available to handle them.

The catch is that assigning a task to an employee has a cost 💸.

These costs vary depending on the difficulty of the task, the expertise of the employee, and other factors.

I need your help to figure out the most cost-effective way to assign these tasks to employees.

You can assume that each task is done by just one employee, and one employee is assigned to just one task.

## Objective Function

Min Total Cost

## Constraints

- One worker per task.
- One task per worker.
- Total cost is the sum of all costs relative to each employee and task.


## Optimization method: Mathematical Model (MILP) 

- Modelled in Pyomo model
- Solved with GLPK

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

