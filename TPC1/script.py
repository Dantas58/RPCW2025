import json

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def generate_ttl_start():
    return """
@prefix : <http://rpcw.di.uminho.pt/2025/EMD/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2025/EMD/> .

<http://rpcw.di.uminho.pt/2025/EMD> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2025/EMD#pratica
:pratica rdf:type owl:ObjectProperty ;
         owl:inverseOf :éPraticadaPor ;
         rdfs:domain :Pessoa ;
         rdfs:range :Modalidade .


###  http://rpcw.di.uminho.pt/2025/EMD#realiza
:realiza rdf:type owl:ObjectProperty ;
         owl:inverseOf :éRealizadoPor ;
         rdfs:domain :Pessoa ;
         rdfs:range :Exame .


###  http://rpcw.di.uminho.pt/2025/EMD#relativoA
:relativoA rdf:type owl:ObjectProperty ;
           owl:inverseOf :temExame ;
           rdfs:domain :Exame ;
           rdfs:range :Modalidade .


###  http://rpcw.di.uminho.pt/2025/EMD#temAtleta
:temAtleta rdf:type owl:ObjectProperty ;
           owl:inverseOf :éAtletaDe .


###  http://rpcw.di.uminho.pt/2025/EMD#temExame
:temExame rdf:type owl:ObjectProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#temModalidade
:temModalidade rdf:type owl:ObjectProperty ;
               owl:inverseOf :éPraticadaEm ;
               rdfs:domain :Clube ;
               rdfs:range :Modalidade .


###  http://rpcw.di.uminho.pt/2025/EMD#éAtletaDe
:éAtletaDe rdf:type owl:ObjectProperty ;
           rdfs:domain :Pessoa ;
           rdfs:range :Clube .


###  http://rpcw.di.uminho.pt/2025/EMD#éPraticadaEm
:éPraticadaEm rdf:type owl:ObjectProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#éPraticadaPor
:éPraticadaPor rdf:type owl:ObjectProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#éRealizadoPor
:éRealizadoPor rdf:type owl:ObjectProperty .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2025/EMD#dataEMD
:dataEMD rdf:type owl:DatatypeProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#email
:email rdf:type owl:DatatypeProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#gênero
:gênero rdf:type owl:DatatypeProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#idade
:idade rdf:type owl:DatatypeProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#morada
:morada rdf:type owl:DatatypeProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#nome
:nome rdf:type owl:DatatypeProperty .


###  http://rpcw.di.uminho.pt/2025/EMD#resultado
:resultado rdf:type owl:DatatypeProperty .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2025/EMD#Clube
:Clube rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2025/EMD#Exame
:Exame rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2025/EMD#Modalidade
:Modalidade rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2025/EMD#Pessoa
:Pessoa rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################


"""

def create_pessoa(p, id_pessoa):
    return f"""
###  http://rpcw.di.uminho.pt/2025/EMD#{id_pessoa}
:{id_pessoa} rdf:type owl:NamedIndividual , 
            :Pessoa ;
    :nome "{p['nome']['primeiro']} {p['nome']['último']}" ;
    :email "{p['email']}" ;
    :género "{p['género']}" ;
    :idade {p['idade']} ;
    :morada "{p['morada']}" .
"""

def create_clube(clube_nome, id_clube, id_pessoa):
    return f"""
###  http://rpcw.di.uminho.pt/2025/EMD#{id_clube}
:{id_clube} rdf:type owl:NamedIndividual , 
            :Clube ;
    :nome "{clube_nome}" ;
    :temAtleta :{id_pessoa} .
"""

def create_modalidade(mod_nome, id_modalidade, id_exame, id_clube, id_pessoa):
    return f"""
###  http://rpcw.di.uminho.pt/2025/EMD#{id_modalidade}
:{id_modalidade} rdf:type owl:NamedIndividual ,
            :Modalidade ;
    :nome "{mod_nome}" ;
    :temExame :{id_exame} ;
    :éPraticadaEm :{id_clube} ;
    :éPraticadaPor :{id_pessoa} .
"""

def create_exame(exame, id_exame, id_pessoa):
    return f"""
###  http://rpcw.di.uminho.pt/2025/EMD#{id_exame}
:{id_exame} rdf:type owl:NamedIndividual , 
            :Exame ;
    :dataEMD "{exame['dataEMD']}"^^xsd:date ;
    :resultado "{"true" if exame['resultado'] else "false"}"^^xsd:boolean ;
    :éRealizadoPor :{id_pessoa} .
"""

def generate_ttl(emds):
    ttl = generate_ttl_start()
    pessoas, clubes, modalidades = {}, {}, {}
    idx_pessoa = idx_clube = idx_mod = 0

    for i, exame in enumerate(emds):
        email = exame['email']
        clube = exame['clube']
        modalidade = exame['modalidade']

        if email not in pessoas:
            id_pessoa = f"P{idx_pessoa}"
            pessoas[email] = id_pessoa
            ttl += create_pessoa(exame, id_pessoa)
            idx_pessoa += 1
        else:
            id_pessoa = pessoas[email]

        if clube not in clubes:
            id_clube = f"C{idx_clube}"
            clubes[clube] = id_clube
            ttl += create_clube(clube, id_clube, id_pessoa)
            idx_clube += 1
        else:
            id_clube = clubes[clube]

        if modalidade not in modalidades:
            id_modalidade = f"M{idx_mod}"
            modalidades[modalidade] = id_modalidade
            ttl += create_modalidade(modalidade, id_modalidade, f"E{i}", id_clube, id_pessoa)
            idx_mod += 1
        else:
            id_modalidade = modalidades[modalidade]
            ttl += f"""
:{id_modalidade} :temExame :E{i} ;
                :éPraticadaEm :{id_clube} ;
                :éPraticadaPor :{id_pessoa} .
"""

        ttl += create_exame(exame, f"E{i}", id_pessoa)

    return ttl


emds = load_json_file("emd.json")
ttl_output = generate_ttl(emds)

with open("emd.ttl", "w", encoding="utf-8") as out:
    out.write(ttl_output)