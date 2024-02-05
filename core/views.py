from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from neo4j import GraphDatabase

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
                result = session.run("RETURN 1")
            

            return render(request, 'success.html', {'username': username})

        except Exception as e:
            # Connection to Neo4j failed
            error_message = f"Error connecting to Neo4j: {str(e)}"

            return render(request, 'login.html', {'error': error_message})
        
    return render(request, 'login.html')