/* the definition to check if X is a member of a List*/

member(X,[X|_]).
member(X,[_|Tail]):- member(X,Tail).

/* check if the given node is a goal node. Further explored nodes are named start recursively */

dfs(Start, VisitedList, [Direction]):- goal(Start, Direction).

/* if its not a goal, check the next connected node, See if the next node is not already in the visited List */
/* Add the current explored node (named start) to the visitedList */

dfs(Start, VisitedList, [StartDir|RestDir]):-
                           connected(Start, Next, StartDir),
                           not member(Next, VisitedList),
                           dfs(Next, [VisitedList|Start], RestDir).