graph = {
  '1' : ['2','3','4'],
  '2' : ['5', '6'],
  '3' : [],
  '4' : ['7','8'],
  '5' :  ['9','10'],
  '6' : [],
  '7' : ['11','12'],
  '8' : [],
  '9' : [],
  '10' : [],
  '11' : [],
  '12' : []
  
}

visited = [] 
queue = []   

def bfs(visited, graph, node):
  visited.append(node)
  queue.append(node)

  while queue:         
    m = queue.pop(0) 
    print (m, end = " ") 

    for neighbour in graph[m]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)


print("BFS IS")
bfs(visited, graph, '1')   
