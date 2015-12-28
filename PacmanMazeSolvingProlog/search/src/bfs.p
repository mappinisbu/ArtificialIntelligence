/* the definition to check if X is a member of a List*/

member(X,[X|_]).
member(X,[_|Tail]):- member(X,Tail).

/* definition of append. Result in L3 */
append([],L,L).
append([H|T],L2,[H|L3])  :-  append(T,L2,L3).


doBFS(Start, Direction) :- bfs([[Start]],Direction).

/* found a goal node in BFS. The goal node is always at head of queue. We are comparing the cell number*/
/* each node in queue(list) consists of <cell No, direction> */
bfs([[Cell|Node]|_], [Cell|Node]) :- goal(Cell,_).

bfs([FirstNode|RestNodes], Direction) :-

/* get the first node of queue and generate successors */
   findAll(FirstNode, Successors),

/* append the successors of this element to queue. the First node is removed from queue */
   append(RestNodes, Successors, Queue),

/* evaluate BFS recursively on this queue */
   bfs(Queue, Direction).

/* get the successors of a cell in that node and store in Successors that follows a template */
findAll([Cell|Node], Successors):-
                 setof([NextNode, Dir, Cell|Node],
			    (connected(Cell, NextNode, Dir), not(member(NextNode,[Cell|Node])) ),
			     Successors),
            !.

findAll(Node, []).