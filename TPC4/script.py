import json
import random
from query import query_graphdb

endpoint = "https://dbpedia.org/sparql"
final = []

def get_random_filmes():
    query = f"""
    SELECT DISTINCT ?filme WHERE {{
        ?filme a dbo:Film .
        ?filme rdfs:label ?label .
        FILTER (lang(?label) = "en")
    }}
    ORDER BY RAND()
    LIMIT 20
    """
    
    try:
        result = query_graphdb(endpoint, query)
        bindings = result.get("results", {}).get("bindings", [])
        filmes = [item["filme"]["value"] for item in bindings]
        
        if filmes:
            return filmes
    except:
        print("ERRO: Método RAND() falhou")


def get_filme_info(uri):
    query = f"""
    SELECT DISTINCT ?titulo ?desc ?data ?pais ?realizador WHERE {{
        <{uri}> dbo:abstract ?desc ;
                rdfs:label ?titulo .
        OPTIONAL {{ <{uri}> dbo:releaseDate ?data. }}
        OPTIONAL {{ <{uri}> dbp:country ?pais. }}
        OPTIONAL {{ <{uri}> dbo:director ?realizador. }}
        FILTER (lang(?desc) = "en")
        FILTER (lang(?titulo) = "en")
    }}
    """
    
    try:
        result = query_graphdb(endpoint, query)
        binding = result.get('results', {}).get('bindings', [{}])[0]

        return {
            "titulo": binding.get('titulo', {}).get('value', 'Desconhecido'),
            "sinopse": binding.get('desc', {}).get('value', 'Sem sinopse'),
            "data_lancamento": binding.get('data', {}).get('value', 'Data desconhecida'),
            "pais_origem": binding.get('pais', {}).get('value', 'Desconhecido'),
            "realizador": binding.get('realizador', {}).get('value', 'Desconhecido'),
        }
    except Exception as e:

        return {
            "titulo": 'Erro ao carregar',
            "sinopse": 'Erro ao carregar',
            "data_lancamento": 'Erro ao carregar',
            "pais_origem": 'Erro ao carregar',
            "realizador": 'Erro ao carregar',
        }

def get_atores(uri):
    query = f"""
    SELECT DISTINCT ?ator ?nome ?data ?origem WHERE {{
        <{uri}> dbo:starring ?ator .
        ?ator a dbo:Person ;
              foaf:name ?nome .
        OPTIONAL {{ ?ator dbo:birthDate ?data. }}
        OPTIONAL {{ ?ator dbp:birthPlace ?origem. }}
    }}
    LIMIT 10
    """
    
    try:
        result = query_graphdb(endpoint, query)
        bindings = result.get('results', {}).get('bindings', [])

        return [
            {
                "id": a.get('ator', {}).get('value', 'Desconhecido'),
                "nome": a.get('nome', {}).get('value', 'Nome desconhecido'),
                "data_nascimento": a.get('data', {}).get('value', 'Desconhecido'),
                "local_nascimento": a.get('origem', {}).get('value', 'Desconhecido')
            }
            for a in bindings
        ]
    except Exception as e:
        return []

    
filmes = get_random_filmes()
    
for i, filme_uri in enumerate(filmes, 1):
    try:
        info = get_filme_info(filme_uri)
        atores = get_atores(filme_uri)

        final.append({
            "id": filme_uri,
            "titulo": info["titulo"],
            "sinopse": info["sinopse"],
            "data_lancamento": info["data_lancamento"],
            "pais_origem": info["pais_origem"],
            "realizador": info["realizador"],
            "elenco": atores
        })
    except Exception as e:
        continue
    
with open("movies.json", "w", encoding='utf-8') as file:
    json.dump(final, file, indent=2, ensure_ascii=False)
    
