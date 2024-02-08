from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import JsonResponse


from neo4j import GraphDatabase
from . import translator
# Create your views here.

def home(request):
    return(HttpResponse("Hello World"))

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # database_name = request.POST.get('database_name')

        try:
            uri = "bolt://localhost:7687"  # Update with your Neo4j database URI
            graph = GraphDatabase.driver(uri, auth=(username, password))
            with graph.session() as session:
                # Attempt to execute a simple query to ensure the connection is valid
                
                result = session.run("SHOW DATABASES;")
                databasesNames = list()
                for record in result:
                    databasesNames.append(record["name"])
                exit
                # result = session.run("RETURN 1")
            

            return render(request, 'success.html', {'username': username, "databases": databasesNames})

        except Exception as e:
            # Connection to Neo4j failed
            error_message = f"Error connecting to Neo4j: {str(e)}"

            return render(request, 'login.html', {'error': error_message})
        
    return render(request, 'login.html')

def serialize_node(node):
    # Convert Neo4j node to a dictionary
    return {
        'id': node.id,
        'labels': list(node.labels),
        'properties': dict(node),
    }
def serialize_rel(rel):
    # Convert Neo4j node to a dictionary
    return {
        'id': rel.element_id,
        "source":rel.nodes[0].element_id,
        "target":rel.nodes[1].element_id,
        'type': list(rel.type),
        'properties': dict(rel._properties),
    }
def show_graph(request, database_name):
    try:
        uri = "bolt://localhost:7687"  # Update with your Neo4j database URI
        username = "neo4j"  # Update with your Neo4j username
        password = "mimou17"  # Update with your Neo4j password


        with GraphDatabase.driver(uri, auth=(username, password)) as driver:

            records, summary, keys = driver.execute_query(
                "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 15",
                database_="neo4j",
                )
            serialized_nodes =[]
            unique_nodes =set()
            serialized_rels =[]
            
            for record in records:
                
                node_a = serialize_node(record[0])
                node_b = serialize_node(record[2])
                # Check if the ID is already in the set
                if node_a['id'] not in unique_nodes:
                    unique_nodes.add(node_a['id'])
                    serialized_nodes.append(node_a)

                if node_b['id'] not in unique_nodes:
                    unique_nodes.add(node_b['id'])
                    serialized_nodes.append(node_b)

                rel= serialize_rel(record[1])
                serialized_rels.append(rel)
                
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            records, summary, keys = driver.execute_query(
            "MATCH (n) RETURN distinct labels(n)",
            database_="neo4j")
            
            ### Get unique lables
            unique_labels = set()

            for record in records:
                unique_labels.update(record[0]) 
            

        # nodes = [record["n"] for record in result]
        return render(request, 'show_graph.html', {'database_name': database_name, 'nodes': serialized_nodes, 'rels': serialized_rels, "unique_labels":list(unique_labels)})

    except Exception as e:
        error_message = f"Error querying Neo4j: {str(e)}"
        return render(request, 'error.html', {'error': error_message})
    

def generate_cypher(request):
    translation = None
    database_name = request.POST.get('database_name', '')
    if request.method == 'POST':
        input_text = request.POST.get('long_text', '')
        model_name = request.POST.get('model', '')
        MY_API_KEY = request.POST.get('hugging_face_token', '')
        translation = translator.generate(input_text, model_name, MY_API_KEY, False)  # Your summarization code here
        # Return a partial HTML response
        return JsonResponse({'translation': translation, 'database_name': database_name})
    
    return render(request, "show_graph.html", context={'translation': translation, 'database_name': database_name})
    