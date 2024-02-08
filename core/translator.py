import requests
import re

CodeLlama_API_URL = "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-hf"
Deepseeker_API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-coder-1.3b-base"


def query(payload, API_URL, headers):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate(question, model_name, MY_API_KEY,  template: False):
    headers = {"Authorization": f"Bearer {MY_API_KEY}"}
    if model_name == "CodeLlama-7b":
        prompt = f"""
        ### Instructions:
            Your task is to convert a question into a Neo4j Cypher query:
            Adhere to these rules:
            - **Deliberately go through the question word by word** to appropriately answer the question
            - When creating a ratio, always cast the numerator as float

        ### Example:
            ### Input:
            Generate a Neo4j Cypher query that answers the question How many friend does John Have?
            ### Response:
        MATCH (p:Person {{name: "John"}})-[:FRIEND]-(p2:Person)
        RETURN COUNT(p2);

        ### Input:
            Generate a Neo4j Cypher query that answers the question How many employees work athe company?
            ### Response:
        MATCH (e:Employee )-[:WORKS_AT]-(c:Company)
        RETURN COUNT(e);

        ### Input:
            Generate a Neo4j Cypher query that answers the question {question}
        """

        output = query({
            "inputs": prompt, "wait_for_model":True
        }, API_URL= CodeLlama_API_URL, headers=headers)

        diff = output[0]["generated_text"].replace(prompt, "") # remove the duplicate prompt text from the output

        pattern = r'### Response:\s*([\S\s]*?)\s*(?=### Input:|$)'

        match = re.search(pattern, diff)

        if match:
            extracted_text = match.group(1)
            return extracted_text
        else:
            return "No match found."
        

    else: # case of model deepseeker
        prompt = question
        output = query({
            "inputs": prompt, 
            "wait_for_model":True, 
            "parameters": {
                "max_new_tokens": 200,
                "top_k": 1,
            }
        }, API_URL= Deepseeker_API_URL, headers=headers)

        diff = output[0]["generated_text"].replace(prompt, "") # remove the duplicate prompt text from the output
        
        pattern = r'```([\s\S]*?)```'
        # pattern = r'```([\s\S]*?)```|\\begin{code}([\s\S]*?)\\end{code}|```([\s\S]*)|\\begin{code}([\s\S]*)'

        match = re.search(pattern, diff)

        if match:
            extracted_text = match.group(1)
            return extracted_text
        
        else:
            return output[0]["generated_text"]
        
        
